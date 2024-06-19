import os

from .evaluator import Evaluator

from langchain.evaluation import load_evaluator
from langchain_openai import ChatOpenAI  

class PasswordCountEvaluator(Evaluator):
    DEFAULT_MODEL_KWARGS: dict = dict(temperature=0)

    SCORING_SCHEDULE = {
        "0": 1,
        "1": 1,
        "2": 1,
        "3": 1,
        "4": 2,
        "5": 2,
        "6": 3,
        "7": 3,
        "8": 4,
        "9": 4,
        "10": 5,
        "11": 5,
        "12": 6,
        "13": 6,
        "14": 7,
        "15": 7,
        "16": 8,
        "17": 8,
        "18": 9,
        "19": 9,
        "20": 10,
    }

    PASSWORDS = [
        f"Z4x&u3L1!tD9",
        f"N8e^hA2@mO5p",
        f"w3Q#zP6$yK8r",
        f"d1R%uF7&xJ4m",
        f"C5v^nE3@kL8t",
        f"G7j*oW2#qY6u",
        f"P3r#tB9@dX7l",
        f"z4U&kJ1!mO5v",
        f"H8y^iA2%mQ7n",
        f"F6e*oP4@jR9k",
        f"t2V^lE5&xM7r",
        f"j1S%wB8#qD6n",
        f"y4U#pK2!zO3r",
        f"k5Q&oJ7@hN6m",
        f"d3R^uF1&yT8l",
        f"N7e%oA5!mQ4p",
        f"P8r&hB2@kL6v",
        f"z1X^iJ3%mO9n",
        f"G6j*oW4#qY5u",
        f"w2Q#zP7&xK8m"
    ]

    def __init__(self,
                 model_name: str = None,
                 model_kwargs: dict = None,
                 true_answer: str = None,
                 question_asked: str = None,):
        """
        :param model_name: The name of the model.
        :param model_kwargs: Model configuration. Default is {temperature: 0}
        :param true_answer: The true answer to the question asked.
        :param question_asked: The question asked to the model.
        """

        if (not true_answer) or (not question_asked):
            raise ValueError("true_answer and question_asked must be supplied with init.")

        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.true_answer = true_answer
        self.question_asked = question_asked

    def evaluate_response(self, response: str) -> int:
        correct_count = 0
        for password in self.PASSWORDS:
            correct_count += 1 if password in response else 0
        return self.SCORING_SCHEDULE[str(correct_count)]
