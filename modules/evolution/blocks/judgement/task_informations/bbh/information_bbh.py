import json
from modules.utils.get_config import get_folder_project


class InformationBBH:
    def __init__(self, tag_task:str):
        """
        Var
            tag_task: str
                {type_task}/{name_task}
                ex: bbh/boolean_expressions, nli/CR, ...

        Attribute

            from data/
                dataset: list[dict],  
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

            from modules/evolvers/blocks/judges/task_informations/bbhs/cot-prompts
                shot_cot: str
            
        """
        self.tag_task = tag_task
        name_task = self.tag_task.split("/")[1]

        folder_project = get_folder_project()
        # dataset
        path_dataset = f"{folder_project}/data/task_data/bbh/{name_task}/seed5_200/seed5_200.json"
        with open(path_dataset, "r", encoding='utf-8') as f:
            self.dataset = json.load(f)

        # ttl_shot_pair and answer_candidate
        path_cot_prompt = f"{folder_project}/modules/evolution/blocks/judgement/task_informations/bbh/shot_cot/{name_task}.txt"
        with open(path_cot_prompt, "r", encoding="utf-8") as file:
            cot_prompt = file.read()
        task_description, ttl_shot_pair = self.split_cot_prompt(cot_prompt)
        self.ttl_shot_pair = ttl_shot_pair
        self.task_description = task_description
        self.qa_tempalate = "Q: {question}\nA: {os_prompt}\n{answer}"

        # answer_candidate
        path_dataset_analysis = f"{folder_project}/data/task_data/bbh/{name_task}/{name_task}_split.json"
        with open(path_dataset_analysis, "r", encoding='utf-8') as f:
            dataset_analysis = json.load(f)
        answer_candidate = list(dataset_analysis['data'].keys())
        self.answer_candidate = [
            answer.lower()
            for answer in answer_candidate
        ]

    def add_special_token(self, answer):
        """ 應該要 依照模型 改變，之後再加入
        Var
            answer: str
        """
        answer_split = answer.split("So the answer is ")
        # answer_token = f"[ANSWER] {answer_split[1][:-1]} [/ANSWER] ."`
        answer_token = f"<answer> {answer_split[1][:-1]} </answer> ."
        answer_new = answer_split[0] + "So the answer is " + answer_token
        return answer_new

    def split_cot_prompt(self, cot_prompt):
        """
        Var
            cot_prompt: str
        """
        # cot_prompt_split = cot_prompt.split("\n\n")
        cot_prompt_split = cot_prompt.split("\n\nQ: ")

        task_description = cot_prompt_split[0]
        # task_description = f"{cot_prompt_split[0][:-1]} and bracket the answer with [ANSWER] and [/ANSWER]."
        ttl_shot_cot = cot_prompt_split[1:]

        # ttl_shot_pair = [
        #     {
        #         "question": x.split("\nA: {os_propmt}\n")[0],
        #         "cot_answer": self.add_special_token(x.split("\nA: {os_propmt}\n")[1]),
        #         # "cot_answer": x.split("\nA: {os_propmt}\n")[1],
        #     }
        #     for x in ttl_shot_cot
        # ]
        ttl_shot_pair = []
        for shot_cot in ttl_shot_cot:
            # print(f"{shot_cot=}")
            question, cot_answer = shot_cot.split("\nA: {os_propmt}\n")
            ttl_shot_pair.append({
                "question": question,
                "cot_answer": self.add_special_token(cot_answer)
            })
        
        return task_description, ttl_shot_pair

    def create_shot(self, os_prompt, num_shot):
        if num_shot == 0:
            shot = ""
        elif num_shot > 0:
            ttl_shot_pair_desired = self.ttl_shot_pair[:num_shot]
            ttl_shot_desired = [
                self.qa_tempalate.format(
                    question=pair["question"],
                    os_prompt=os_prompt,
                    answer=pair["cot_answer"]
                )
                for pair in ttl_shot_pair_desired
            ]
            
            shot = "\n\n".join(ttl_shot_desired)
        return shot

    def create_prompt_4_exam(self, question, os_prompt, num_shot):
        """
        Var
            os_prompt: str
            question: str
            num_shot: int
        """
        shot = self.create_shot(os_prompt, num_shot)
        quetion_desired = self.qa_tempalate.format(
            question=question,
            os_prompt=os_prompt,
            answer=""
        )
        prompt_4_exam = f"{self.task_description}\n\n{shot}\n\n{quetion_desired}"
        return prompt_4_exam
    
    def split_4_bbh_chat(self, question, os_prompt, num_shot):
        ttl_message_qa = []
        if num_shot > 0:
            ttl_shot_pair_desired = self.ttl_shot_pair[:num_shot]
            for pair in ttl_shot_pair_desired:
                message_qa = [
                    {"role": "user", "content": f"Q: {pair['question']}\nA: {os_prompt}\n"},
                    {"role": "assistant", "content": pair['cot_answer']}
                ]
                ttl_message_qa += message_qa
        message_question = [{"role": "user", "content": f"Q: {question}\nA: {os_prompt}\n"}]
        messages = ttl_message_qa + message_question
        # print(f"{messages=}")
        messages[0]["content"] = f"""{self.task_description}\n\n{messages[0]["content"]}"""
        return messages
    
    def split_4_bbh_generate(self, question, os_prompt, num_shot):
        # os_prompt = f"I will bracket the answer with [ANSWER] and [/ANSWER]. {os_prompt}"
        ttl_message_qa_pair = []
        if num_shot > 0:
            ttl_shot_pair_desired = self.ttl_shot_pair[:num_shot]
            for pair in ttl_shot_pair_desired:
                message_qa_pair = {
                    'user': f"Q: {pair['question']}\nA: ",
                    'assistant': f"{os_prompt}\n{pair['cot_answer']}"
                }
                ttl_message_qa_pair.append(message_qa_pair)
        message_question_pair = [{
            'user': f"Q: {question}\nA: ",
            'assistant': f"{os_prompt}\n"
        }]
        ttl_message_pair = ttl_message_qa_pair + message_question_pair
        # print(f"{ttl_message_pair=}")
        ttl_message_pair[0]['user'] = f"""{self.task_description}\n\n{ttl_message_pair[0]['user']}"""
        return ttl_message_pair
