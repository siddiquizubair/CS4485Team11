from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

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

        if "sort" in input_text:
            if "bubble" in input_text:
                response = Statement(text = bubbleSort)
                response.confidence = 1
            if "quick" in input_text:
                response = Statement(text = quickSort)
                response.confidence = 1


        if "search" in input_text:
            if "binary" in input_text:
                response = Statement(text = binarySearch)
                response.confidence = 1

        return response
