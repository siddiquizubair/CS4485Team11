from select import select
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import re

binarySearch = {
    "best": "O(1)",
    "average": "O(log n)",
    "worst": "O(log n)",
    "expl": "Binary search is a search algorithm that finds the position of a target value within a sorted array.<br>Binary search compares the target value to the middle element of the array. If they are not<br> equal, the half in which the target cannot lie is eliminated and the search continues on the remaining half,<br>again taking the middle element to compare to the target value, and repeating this until the target value is found.<br>If the search ends with the remaining half being empty, the target is not in the array."
}

bubbleSort = {
    "best": "O(n)",
    "average": "O(n^2)",
    "worst": "O(n^2)",
    "expl": "Bubble sort is a simple sorting algorithm that repeatedly steps through the input list element by element,<br>comparing the current element with the one after it, swapping their values if needed.These passes<br> through the list are repeated until no swaps had to be performed during a pass, meaning that the list<br> has become fully sorted."
}

insertSort = {
    "best": "O(n)",
    "average": "O(n^2)",
    "worst": "O(n^2)",
    "expl": "Insertion sort is a simple sorting algorithm that works similar to the way you sort<br> playing cards in your hands. The array is virtually split into a sorted and an unsorted part.<br> Values from the unsorted part are picked and placed at the correct position in the sorted part."
}

quickSort = {
    "best": "O(nlogn)",
    "average": "O(nlogn)",
    "worst": "O(n^2)",
    "expl": "Quicksort is a divide-and-conquer algorithm. It works by selecting a 'pivot' element from <br>the array and partitioning the other elements into two sub-arrays, according to whether they<br> are less than or greater than the pivot. For this reason, it is sometimes called partition-exchange sort.<br>The sub-arrays are then sorted recursively."
}

selectionSort = {
    "best": "O(n^2)",
    "average": "O(n^2)",
    "worst": "O(n^2)",
    "expl": "Selection sort divides the input list into two parts: a sorted sublist of items which is built up from left to <br>right at the front (left) of the list and a sublist of the remaining unsorted items that occupy the rest of<br> the list. Initially, the sorted sublist is empty and the unsorted sublist is the entire input list. The algorithm<br> proceeds by finding the smallest (or largest, depending on sorting order) element in the unsorted sublist, <br>exchanging (swapping) it with the leftmost unsorted element (putting it in sorted order), and moving the <br>sublist boundaries one element to the right."
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

        bigO = re.findall("big o|big O|Big o|Big O", input_text)
        
        runtime = re.findall("runtime", input_text)

        question = re.findall("what|What|how|How|work", input_text)

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
        elif len(question) != 0:
            if "sort" in input_text:
                if "bubble" in input_text or "Bubble" in input_text:
                    response = Statement(text = bubbleSort["expl"])
                    response.confidence = 1
                elif "quick" in input_text or "Quick" in input_text:
                    response = Statement(text = quickSort["expl"])
                    response.confidence = 1
                elif "selection" in input_text or "Selection" in input_text:
                    response = Statement(text = selectionSort["expl"])
                    response.confidence = 1
                elif "insertion" in input_text or "Insertion" in input_text:
                    response = Statement(text = insertSort["expl"])
                    response.confidence = 1
            elif "search" in input_text:
                if "binary" in input_text or "Binary" in input_text:
                    response = Statement(text = binarySearch["expl"])
                    response.confidence = 1

        return response

    def checkSorts(self, algo):
        if "sort" in algo:
            if "bubble" in algo:
                print("bubble")
                return self.getRuntime(bubbleSort)
            if "quick" in algo:
                return self.getRuntime(quickSort)
            if "selection" in algo:
                return self.getRuntime(selectionSort)


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