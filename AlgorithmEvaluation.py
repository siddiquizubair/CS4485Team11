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

        bigO = re.findall("big o|big O|Big O|Big o", input_text)
        
        runtime = re.findall("runtime", input_text)

        if len(bigO) != 0:
            print("checking big o")
            regex = "[a-zA-Z]\^[0-9]|[a-zA-Z]*log[a-zA-Z]|[0-9]+|[+/*-]"
            exp = re.findall(regex, input_text)
            parsed = ' '.join(exp)
            factors = re.findall("[a-zA-Z]\^[0-9]|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed)
            response = Statement(text = self.checkBigO(factors))
            if len(factors) != 0:
                response.confidence = 1
        elif len(runtime) != 0:
            print("checking runtime")
            response = Statement(text = self.checkSorts(input_text))
            if response is not None:
                response.confidence = 1

        return response

    def checkSorts(self, algo):
        if "sort" in algo:
            if "bubble" in algo:
                print("bubble")
                return self.getRuntime(bubbleSort)
            if "quick" in algo:
                return self.getRuntime(quickSort)


        if "search" in algo:
            if "binary" in algo:
                print("binary")
                return self.getRuntime(binarySearch)

    def checkBigO(self, expression):
        ntime = "1"
        runtime = "1"

        for exp in expression:
            if "^" in exp:
                ntime = exp
                runtime = "N" + exp[-2:]
                break
            elif "log" in exp:
                ntime = exp
                runtime = "logN"

        return "The Big O runtime for this expression is O(" + runtime + ")."

    def getRuntime(self, algo):
        return "The best case runtime is " + algo["best"] + ", the average case runtime is " + algo["average"] + ", and the worst case runtime is " + algo["worst"]