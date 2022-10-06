from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import re

binarySearch = {
    "best": "O(1)",
    "average": "O(log n)",
    "worst": "O(log n)"
}

bubbleSort = {
    "best": "O(n)",
    "average": "O(n^2)",
    "worst": "O(n^2)"
}

insertSort = {
    "best": "O(n)",
    "average": "O(n^2)",
    "worst": "O(n^2)"
}

quickSort = {
    "best": "O(nlogn)",
    "average": "O(nlogn)",
    "worst": "O(n^2)"
}

selectionSort = {
    "best": "O(n^2)",
    "average": "O(n^2)",
    "worst": "O(n^2)"
}

class AlgorithmLogic(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        response = self.process(statement)
        return response.confidence == 1

    def process(self, statement, additional_response_selection_parameters=None):
        input_text = statement.text;
        response = Statement(text = input_text)
        response.confidence = 0

        if "sort" in input_text:
            if "bubble" in input_text:
                response = Statement(text = self.getRuntime(bubbleSort))
                response.confidence = 1
            if "quick" in input_text:
                response = Statement(text = self.getRuntime(quickSort))
                response.confidence = 1


        if "search" in input_text:
            if "binary" in input_text:
                response = Statement(text = self.getRuntime(binarySearch))
                response.confidence = 1

        bigO = re.findall("big o", input_text)
        runtime = re.findall("runtime", input_text)

        if len(bigO) != 0 or len(runtime) != 0:
            regex = "[a-zA-Z]\^[0-9]|[a-zA-Z]*log[a-zA-Z]|[0-9]+|[+/*-]"
            exp = re.findall(regex, input_text)
            parsed = ' '.join(exp)
            factors = re.findall("[a-zA-Z]\^[0-9]|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed)
            response = Statement(text = self.checkBigO(factors))
            if len(factors) != 0:
                response.confidence = 1

        return response

    def checkBigO(self, expression):
        ntime = "1"

        for exp in expression:
            if "^" in exp:
                ntime = exp
                break
            elif "log" in exp:
                ntime = exp

        return "The Big O runtime for this expression is O(N" + exp[-2:] + ")."

    def getRuntime(self, algo):
        return "The best case runtime is " + algo["best"] + ", the average case runtime is " + algo["average"] + ", and the worst case runtime is " + algo["worst"]