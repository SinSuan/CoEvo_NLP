from copy import deepcopy
import re

from tqdm import tqdm
from modules.evolution.blocks.call_model.local.llm import LLM
from modules.evolution.blocks.judgement.task_informations.bbh.information_bbh import InformationBBH
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
        return self.score() / len(self.dataset)

class Judge:
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
        self.llm = llm
        self.information_task = information_task

    def method(self, question, os_prompt, num_shot):
        """
        Retrun
            reply: str
                llm 回應的文字
        """
        
        # create the prompt_4_exam by question
        prompt_4_exam = self.information_task.create_prompt_4_exam(question, os_prompt, num_shot)
        print(f"{prompt_4_exam=}")
        # call llm
        response = self.llm.chat(prompt_4_exam, temperature=None, max_new_tokens=500)
        reply = response.strip()

        return reply

    def method_chat_bbh(self, question, os_prompt, num_shot):
        """
        Retrun
            reply: str
                llm 回應的文字
        """
        
        # create the messages by question
        # messages = self.information_task.split_4_bbh_chat(question, os_prompt, num_shot)
        messages = self.information_task.split_4_bbh_generate(question, os_prompt, num_shot)
        # call llm
        # response = self.llm.chat_bbh(messages, temperature=None, max_new_tokens=500)
        response = self.llm.generate_bbh_mistral(messages, temperature=None, max_new_tokens=500)
        # response = self.llm.generate_stream(messages, temperature=None, max_new_tokens=500)
        reply = response.strip()

        return reply

    def extract_answer(self, reply):
        """ select the label of which the keyword is represented in the reply
        """
        reply_lower = reply.lower()

        # w/ special token
        match_all = re.findall(r'<answer>(.*?)</answer>', reply_lower, re.DOTALL)
        # match_all = re.findall(r'\[answer\](.*?)\[/answer\]', reply_lower, re.DOTALL)
        # match_all = re.findall(r'so the answer is (.*?)\.', reply_lower, re.DOTALL)
        if (match_all!=[]):
            answer_predict = match_all[-1].strip()
            if answer_predict not in self.information_task.answer_candidate:
                answer_predict = "unknown"
        else:
            answer_predict = "unknown"

        # # w/o special token
        # answer_predict = reply_lower.split("so the answer is ")[-1].split(".")[0]

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
        if DEBUGGER=="True": print("enter Evaluator.experiment")
        dataset = deepcopy(dataset)

        data_correct = []
        dataset_confusing = []
        dataset_wrong = []
        for data in tqdm(dataset):

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

        if DEBUGGER=="True": print("exit Evaluator.experiment")
        return result

    def get_result(self, os_prompt, num_shot):
        """ 評分
        """
        print(f"{os_prompt=}")
        result_train = self.judge(os_prompt, self.information_task.dataset["train_split"], num_shot)

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

        return pair
