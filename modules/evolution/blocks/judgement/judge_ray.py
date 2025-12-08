from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
import re
from typing import List

import numpy as np
import ray
import torch
from tqdm import tqdm
# from modules.evolution.blocks.call_model.llm import CallTGI
from modules.evolution.blocks.call_model.local.llm import LLM
from modules.evolution.blocks.judgement.task_informations.bbh.information_bbh import InformationBBH
# from modules.evolution.blocks.judgement.utils import ray_sub_judge

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

class ExperimentResult:
    """ return type of experiment
    """
    def __init__(self, dataset, dataset_correct, dataset_wrong, dataset_confusing):
        """
        Attribute
            dataset: list[dict]
            {
                "train_split":[
                    {
                        "question": str,
                        "answer": str
                    },
                    ...
                ],
                "dev_split":[
                    {
                        "question": str,
                        "answer": str
                    },
                    ...
                ]
            }
        """
        self.dataset = dataset
        self.dataset_correct = dataset_correct
        self.dataset_wrong = dataset_wrong
        self.dataset_confusing = dataset_confusing

    def score(self):
        return len(self.dataset_correct)

    def accuracy(self):
        """ In multi-class classification, micro-f1 = recall = precision = accuracy.
        """
        return self.score() / len(self.dataset)

@ray.remote
class SubJudge:
    def __init__(self, information_task: InformationBBH, llm: LLM):
        """
        Attribute

            information_task: object
                有關於這個 task 的所有資訊
                attribute:
                    dataset                     (required)
                    prompt_template (f-string)  (required)
                        keyword:
                            {os_prompt} 本次要測試的 os_prompt
                            {question}  本次要測試的 question
                            {shot}      本資料集本次測試用的 shot
                    shot_cot: str           (optional)
                    answer_candidate: list[str] (required)
                        available answer (只接受預處理後在範圍內的答案)

            llm: CallTGI
        """
        if DEBUGGER=="True": print("enter SubJudge.__init__")
        print(f"SubJudge.{torch.cuda.is_available()=}")
        if torch.cuda.is_available() is False:
            raise Exception("No GPU available.")
        self.llm = llm
        self.information_task = information_task
        if DEBUGGER=="True": print("leave SubJudge.__init__")

    def get_llm(self):
        return self.llm

    def method(self, question, os_prompt, num_shot):
        """
        Retrun
            reply: str
                llm 回應的文字
        """
        if DEBUGGER=="True": print("enter SubJudge.method")
        
        # create the prompt_4_exam by question
        prompt_4_exam = self.information_task.create_prompt_4_exam(question, os_prompt, num_shot)
        print(f"{prompt_4_exam=}")
        # call llm
        response = self.llm.chat(prompt_4_exam, temperature=None, max_new_tokens=500)
        reply = response.strip()

        if DEBUGGER=="True": print("leave SubJudge.method")
        return reply

    def method_chat_bbh(self, question, os_prompt, num_shot):
        """
        Retrun
            reply: str
                llm 回應的文字
        """
        if DEBUGGER=="True": print("enter SubJudge.method_chat_bbh")

        # create the messages by question
        messages = self.information_task.split_4_bbh_generate(question, os_prompt, num_shot)

        # call llm
        response = self.llm.generate_bbh_mistral(messages, temperature=None, max_new_tokens=500)
        reply = response.strip()

        if DEBUGGER=="True": print("leave SubJudge.method_chat_bbh")
        return reply

    def extract_answer(self, reply):
        """ select the label of which the keyword is represented in the reply
        """
        if DEBUGGER=="True": print("enter SubJudge.extract_answer")

        reply_lower = reply.lower()

        match_all = re.findall(r'<answer>(.*?)</answer>', reply_lower, re.DOTALL)
        if (match_all!=[]):
            answer_predict = match_all[-1].strip()
            if answer_predict not in self.information_task.answer_candidate:
                answer_predict = "unknown"
        else:
            answer_predict = "unknown"

        if DEBUGGER=="True": print("leave SubJudge.extract_answer")
        return answer_predict

    def judge(self, os_prompt, dataset, num_shot) -> ExperimentResult:
        """ 實驗
        Var
            os_prompt: str
                SAP 在練的 prompt
            
            dataset: list[dict]
                dict is of the form:
                    {
                        "question": str,
                        "answer": str
                    }
        Return
            score: int
            precision: float
                其實是 accuracy
            dataset_confusing: list[dict]
                無法判斷的資料
            dataset_wrong: list[dict]
        """
        if DEBUGGER=="True": print("enter SubJudge.judge")

        if dataset is None:
            dataset = deepcopy(self.information_task.dataset["train_split"])

        data_correct = []
        dataset_confusing = []
        dataset_wrong = []
        for data in tqdm(dataset):
            data = deepcopy(data)

            # get answer_predict
            question = data['question']
            # reply = self.method(question, os_prompt, num_shot)
            reply = self.method_chat_bbh(question, os_prompt, num_shot)
            while reply=="redo":
                # reply = self.method(question, os_prompt, num_shot)
                reply = self.method_chat_bbh(question, os_prompt, num_shot)

            answer_predict = self.extract_answer(reply)
            # print(f"{reply=}\n{answer_predict=}")

            # 對答案、計分數
            answer_label = data['answer'].lower()
            data["prediciton"] = answer_predict
            data["reply"] = reply
            if answer_predict==answer_label:    # 答對
                data_correct.append(data)
            else:
                if answer_predict=="unknown":   # 無法判斷
                    dataset_confusing.append(data)
                else:                           # 答錯
                    dataset_wrong.append(data)

        result = ExperimentResult(
            dataset=deepcopy(dataset),
            dataset_correct=data_correct,
            dataset_wrong=dataset_wrong,
            dataset_confusing=dataset_confusing
        )

        if DEBUGGER=="True": print("exit SubJudge.judge")
        return result

class Judge:
    def __init__(self, information_task: InformationBBH, ttl_llm: List[LLM]):
        if DEBUGGER=="True": print("enter Judge.__init__")
        self.information_task = information_task

        dataset_train = deepcopy(information_task.dataset["train_split"])
        size_chunck_train = len(dataset_train) // len(ttl_llm)
        ttl_chunck_train = np.array_split(dataset_train, size_chunck_train)

        dataset_dev = deepcopy(information_task.dataset["dev_split"])
        size_chunck_dev = len(dataset_dev) // len(ttl_llm)
        ttl_chunck_dev = np.array_split(dataset_dev, size_chunck_dev)

        ttl_sub_judge = []
        for llm, chunck_train, chunck_dev in zip(ttl_llm, ttl_chunck_train, ttl_chunck_dev):
            dataset = {
                "train_split": chunck_train,
                "dev_split": chunck_dev
            }
            sub_information_task = deepcopy(information_task)
            sub_information_task.dataset = dataset
            sub_judge = SubJudge(sub_information_task, llm)
            # sub_judge = SubJudge.remote(sub_information_task, llm)
            ttl_sub_judge.append(sub_judge)

        self.ttl_sub_judge = ttl_sub_judge
        if DEBUGGER=="True": print("leave Judge.__init__")

    def judge(self, os_prompt, num_shot) -> ExperimentResult:
        """ 實驗
        Var
            os_prompt: str
                SAP 在練的 prompt
        Return
            score: int
            precision: float
                其實是 accuracy
            dataset_confusing: list[dict]
                無法判斷的資料
            dataset_wrong: list[dict]
        """
        if DEBUGGER=="True": print("enter Judge.judge")

        print(f"Judge.judge.0.{torch.cuda.is_available()=}")
        if torch.cuda.is_available() is False:
            raise Exception("No GPU available.")

        # @ray.remote
        # def ray_sub_judge(sub_judge):
        #     if DEBUGGER=="True": print(f"enter ray_sub_judge")
        #     sub_result = sub_judge.judge(os_prompt, sub_judge.information_task.dataset["train_split"], num_shot)
        #     if DEBUGGER=="True": print(f"leave ray_sub_judge")
        #     return sub_result

        # ttl_future = [
        #         sub_judge.judge.remote(os_prompt, sub_judge.information_task.dataset["train_split"], num_shot)
        #         for sub_judge in self.ttl_sub_judge
        #     ]
        # ttl_sub_result = ray.get(ttl_future)

        score = 0
        dataset_confusing = []
        dataset_wrong = []
        dataset_correct = []
        for sub_result in ttl_sub_result:
            score += sub_result.score()
            dataset_confusing += sub_result.dataset_confusing
            dataset_wrong += sub_result.dataset_wrong
            dataset_correct += sub_result.dataset_correct

        result = ExperimentResult(
            dataset=deepcopy(self.information_task.dataset["train_split"]),
            dataset_correct=dataset_correct,
            dataset_wrong=dataset_wrong,
            dataset_confusing=dataset_confusing
        )

        if DEBUGGER=="True": print("leave Judge.judge")
        return result

    def get_result(self, os_prompt, num_shot):
        """ 評分
        """
        if DEBUGGER=="True": print("enter Judge.get_result")

        print(f"{os_prompt=}")

        result_train = self.judge(os_prompt, num_shot)

        pair = {
            "prompt": os_prompt,
            "train_score": result_train.score(),
            "precision": {
                "train": result_train.accuracy(),
            },
            "data_sick": {
                "train": {
                    "confusing": deepcopy(result_train.dataset_confusing),
                    "wrong": deepcopy(result_train.dataset_wrong),
                    "correct": deepcopy(result_train.dataset_correct)
                }
            }
        }

        if DEBUGGER=="True": print("leave Judge.get_result")
        return pair
