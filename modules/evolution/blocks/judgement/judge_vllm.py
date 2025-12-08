from copy import deepcopy
import re

from tqdm import tqdm
from modules.evolution.blocks.call_model.vllm.llm import vLLM
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

class Judge_vLLM:
    def __init__(self, information_task: InformationBBH, llm: vLLM):
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

    def method_chat_bbh(self, question, os_prompt, num_shot):
        """
        Retrun
            reply: str
                llm 回應的文字
        """

        # create the ttl_message_pair by question
        ttl_message_pair = self.information_task.split_4_bbh_generate(question, os_prompt, num_shot)

        # call llm
        response = self.llm.generate_bbh_mistral(ttl_message_pair, temperature=0, max_new_tokens=500)
        reply = response.strip()

        return reply

    def extract_answer(self, reply):
        """ select the label of which the keyword is represented in the reply
        """
        reply_lower = reply.lower()

        # w/ special token
        match_all = re.findall(r'<answer>(.*?)</answer>', reply_lower, re.DOTALL)
        if (match_all!=[]):
            answer_predict = match_all[-1].strip()
            if answer_predict not in self.information_task.answer_candidate:
                answer_predict = "unknown"
        else:
            answer_predict = "unknown"

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
            reply = self.method_chat_bbh(question, os_prompt, num_shot)
            while reply=="redo":
                reply = self.method_chat_bbh(question, os_prompt, num_shot)

            answer_predict = self.extract_answer(reply)

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

    def data_2_message_pair(self, dataset, os_prompt, num_shot):
        dataset = deepcopy(dataset)

        all_ttl_message_pair = []
        for data in dataset:
            question = data['question']
            ttl_message_pair = self.information_task.split_4_bbh_generate(question, os_prompt, num_shot)
            all_ttl_message_pair.append(ttl_message_pair)
        return all_ttl_message_pair

    def judge2(self, os_prompt, dataset, num_shot):
        all_ttl_message_pair = self.data_2_message_pair(dataset, os_prompt, num_shot)
        all_response = self.llm.generate_bbh_mistral(all_ttl_message_pair, temperature=0, max_new_tokens=500)
        all_reply = [response.strip() for response in all_response]

        data_correct = []
        dataset_confusing = []
        dataset_wrong = []
        for data, ttl_message_pair, reply in zip(dataset, all_ttl_message_pair, all_reply):

            answer_predict = self.extract_answer(reply)

            # 對答案、計分數
            answer_label = data['answer'].lower()
            data["prediciton"] = answer_predict
            generation_record = {
                "instruction": ttl_message_pair,
                "reply": reply
            }
            data["generation"] = generation_record
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
        result_train = self.judge2(os_prompt, self.information_task.dataset["train_split"], num_shot)
        result_dev = self.judge2(os_prompt, self.information_task.dataset["dev_split"], num_shot)

        pair = {
            "prompt": os_prompt,
            "train_score": result_train.score(),
            "dev_score": result_dev.score(),
            "precision": {
                "train": result_train.accuracy(),
                "dev": result_dev.accuracy()
            },
            "data_sick": {
                "train": {
                    "confusing": deepcopy(result_train.dataset_confusing),
                    "wrong": deepcopy(result_train.dataset_wrong),
                    "correct": deepcopy(result_train.dataset_correct)
                },
                "dev": {
                    "confusing": deepcopy(result_dev.dataset_confusing),
                    "wrong": deepcopy(result_dev.dataset_wrong),
                    "correct": deepcopy(result_dev.dataset_correct)
                }
            }
        }

        return pair
