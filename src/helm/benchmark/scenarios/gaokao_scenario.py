import csv
import os
from typing import Dict, List
import json
from helm.common.general import ensure_file_downloaded
from helm.common.hierarchical_logger import hlog
from .scenario import Scenario, Instance, Reference, TRAIN_SPLIT, VALID_SPLIT, TEST_SPLIT, CORRECT_TAG, Input, Output
import re


mcq_prompt = {
    "examples": [
        {
            "type": "single_choice",
            "subject": "Math",
            "keyword": "2010-2022_Math_II_MCQs",
            "prefix_prompt": "请你做一道数学选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下：",
            "comment": ""
        },
        {
            "type": "single_choice",
            "subject": "Math",
            "keyword": "2010-2022_Math_I_MCQs",
            "prefix_prompt": "请你做一道数学选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下：",
            "comment": ""
        },
        {
            "type": "single_choice",
            "subject": "History",
            "keyword": "2010-2022_History_MCQs",
            "prefix_prompt": "请你做一道历史选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："
        },
        {
            "type": "single_choice",
            "subject": "Biology",
            "keyword": "2010-2022_Biology_MCQs",
            "prefix_prompt": "请你做一道生物选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："
        },
        {
            "type": "single_choice",
            "subject": "Political_Science",
            "keyword": "2010-2022_Political_Science_MCQs",
            "prefix_prompt": "请你做一道政治选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："
        },
        {
            "type": "multi_choice",
            "subject": "Physics",
            "keyword": "2010-2022_Physics_MCQs",
            "prefix_prompt": "请你做一道物理选择题。\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出所有符合题意的答案，并写在【答案】和<eoa>之间。\n例如：【答案】 AB <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】... <eoa>\n请你严格按照上述格式作答。\n"
        },
        {
            "type": "single_choice",
            "subject": "Chemistry",
            "keyword": "2010-2022_Chemistry_MCQs",
            "prefix_prompt": "请你做一道化学选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："
        },
        {
            "type": "single_choice",
            "subject": "English",
            "keyword": "2010-2013_English_MCQs",
            "prefix_prompt": "请你做一道英语选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："
        },
        {
            "type": "multi_question_choice",
            "subject": "Chinese",
            "keyword": "2010-2022_Chinese_Modern_Lit",
            "prefix_prompt": "请你做一道语文阅读理解题，其中包含三个小题。\n请你一步一步思考。每一题你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：（1）【答案】 A <eoa>\n（2）【答案】 B <eoa>\n请你严格按照上述格式作答。\n"
        },
        {
            "type": "multi_question_choice",
            "subject": "English",
            "keyword": "2010-2022_English_Fill_in_Blanks",
            "prefix_prompt": "请你做一道英语完形填空题,其中包含二十个小题。\n请你一步一步思考。每一题你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：（1）【答案】 A <eoa>\n（2）【答案】 B <eoa>\n请你严格按照上述格式作答。\n"
        },
        {
            "type": "five_out_of_seven",
            "subject": "English",
            "keyword": "2012-2022_English_Cloze_Test",
            "prefix_prompt": "请回答下面的问题，将符合题意的五个选项的字母写在【答案】和<eoa>之间，例如“【答案】 A B C D E <eoa>\n请严格按照上述格式作答。\n"
        },
        {
            "type": "multi_question_choice",
            "subject": "Geography",
            "keyword": "2010-2022_Geography_MCQs",
            "prefix_prompt": "请你做一道地理选择题，其中包含两到三个小题。\n请你一步一步思考。每一题你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：（1）【答案】 A <eoa>\n（2）【答案】 B <eoa>\n请你严格按照上述格式作答。\n"
        },
        {
            "type": "multi_question_choice",
            "subject": "English",
            "keyword": "2010-2022_English_Reading_Comp",
            "prefix_prompt": "请你做一道英语阅读理解题，其中包含三到五个小题。\n请你一步一步思考。每一题你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：（1）【答案】 A <eoa>\n（2）【答案】 B <eoa>\n请你严格按照上述格式作答。\n"
        },
        {
            "type": "multi_question_choice",
            "subject": "English",
            "keyword": "2010-2022_Chinese_Lang_and_Usage_MCQs",
            "prefix_prompt": "请你做一道语文选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n（1）【解析】 ... <eoe>\n【答案】 ... <eoa>\n（2）【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。如果不止一道题，请分别作答\n题目如下："
        }
    ]
}


class GaoKaoScenario(Scenario):
    """
    The Massive Multitask Language Understanding benchmark from this paper:

    - https://arxiv.org/pdf/2009.03300.pdf

    Code is adapted from:

    - https://github.com/hendrycks/test/blob/master/evaluate.py
    - https://github.com/EleutherAI/lm-evaluation-harness/blob/master/lm_eval/tasks/hendrycks_test.py

    We prompt models using the following format

        <input>                  # train
        A. <reference>
        B. <reference>
        C. <reference>
        D. <reference>
        Answer: <A/B/C/D>

        x N (N-shot)

        <input>                  # test
        A. <reference1>
        B. <reference2>
        C. <reference3>
        D. <reference4>
        Answer:

    For example (from mmlu:anatomy), we have:

        The pleura
        A. have no sensory innervation.
        B. are separated by a 2 mm space.
        C. extend into the neck.
        D. are composed of respiratory epithelium.
        Answer: C

        Which of the following terms describes the body's ability to maintain its normal state?
        A. Anabolism
        B. Catabolism
        C. Tolerance
        D. Homeostasis
        Answer:

    Target: D
    """

    name = "gaokao"
    description = "GaoKao Bench"
    tags = ["knowledge", "multiple_choice", "Chinese"]

    def __init__(
            self,
            category: str = "Multiple-choice_Questions",
            subject: str = "all",
            # directory: str = ""
        ):
        super().__init__()
        # self.category: str = category
        if category in ["MCQ", "multiple choice questions", "multiple-choice questions", "Multiple-choice_Questions"]:
            self.category = "Multiple-choice_Questions"
            self.question_types = ["multi_choice", "single_choice", "multi_question_choice"]
        elif category in ["multi_choice", "single_choice", "multi_question_choice"]:
            self.category = "Multiple-choice_Questions"
            self.question_types = [category]
            # "Multiple-choice_Questions"
        else:
            raise Exception("Category {} is not supported in Gaokao Scenario".format(category))

        existing_subjects = [
                "Math",
                "Chinese",
                "English",
                "History",
                "Political_Science",
                "Chemistry",
                "Physics",
                "Geography",
                "Biology",
            ]
        if subject == "all":
            self.subjects = existing_subjects
        else:
            assert subject in existing_subjects
            self.subjects = [subject]

    @staticmethod
    def process_question(question):
        chars = ["A", "B", "C", "D", "E"]
        char_to_idx = {}

        for n, char in enumerate(chars[:-1]):
            positions = [val.start() for val in re.finditer("{}.".format(char), question)] + \
                        [val.start() for val in re.finditer("{}、".format(char), question)]
            char_to_idx[chars[n]] = positions[-1]
        char_to_idx[chars[-1]] = len(question) + 1

        answers_dict = {}
        answers = []
        for n, char in enumerate(chars[:-1]):
            start_idx = char_to_idx[chars[n]]
            end_idx = char_to_idx[chars[n+1]]
            answer = question[(start_idx+2): end_idx]
            answer = answer.strip()
            answers_dict[chars[n]] = answer
            answers.append(answer)

        question = question[:char_to_idx["A"]]
        question = question.strip()
        return question, answers

    def get_instances(self) -> List[Instance]:
        # Download the raw data
        data_path: str = os.path.join(self.output_path)
        assert os.path.exists(data_path)

        # Read all the instances
        instances: List[Instance] = []

        cases = mcq_prompt["examples"]

        for i in range(len(cases)):

            keyword = cases[i]['keyword']
            subject = cases[i]['subject']
            question_type = cases[i]['type']
            zero_shot_prompt_text = cases[i]['prefix_prompt']

            if question_type in self.question_types and subject in self.subjects:

                filepath = os.path.join(self.output_path, self.category, keyword+".json")
                with open(filepath, 'r') as fr:
                    data = json.load(fr) # , cls=LazyDecoder)
                fr.close()

                examples = data["example"]

                for example in examples:

                    question = example["question"]
                    question, answers = self.process_question(question)
                    answers_dict = dict(zip(["A", "B", "C", "D"], answers))
                    # print("answer: {}. answers_dict: {}".format(example["answer"], answers_dict))
                    correct_answer: list = [answers_dict[ans] for ans in example["answer"]]

                    def answer_to_reference(answer: str) -> Reference:
                        return Reference(Output(text=answer), tags=[CORRECT_TAG] if answer in correct_answer else [])

                    instance = Instance(
                        input=Input(text=question),
                        references=list(map(answer_to_reference, answers)),
                        split="test",
                    )
                    # print("reference: ", list(map(answer_to_reference, answers)),)
                    instances.append(instance)
        # print("instances: ", len(instances))
        return instances


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)
