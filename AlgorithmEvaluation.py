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
        supers_n = "⁰¹²³⁴⁵⁶⁷⁸⁹"
        supers_x = "ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ"
        input_text = statement.text;
        response = Statement(text = input_text)
        response.confidence = 0

        bigO = re.findall("big o|big O|Big o|Big O", input_text)
        
        runtime = re.findall("runtime", input_text)

        question = re.findall("what|What|how|How|work", input_text)

        if len(bigO) != 0:
            print("checking big o")
            regex = "[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+|[+/*-]"
            exp = re.findall(regex, input_text)
            parsed = ' '.join(exp)
            factors = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed)
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
            elif "sorting" in input_text and "algorithms" in input_text:
                response = Statement(text = "The sorting algorithms are <br>Selection Sort<br> Bubble Sort<br> Insertion Sort<br> Merge Sort<br> Quick Sort<br> Heap Sort<br> Counting Sort<br> Radix Sort<br> Bucket Sort")
                response.confidence = 1
            elif "office hours" in input_text or "Office hours" in input_text:
                response = Statement(text = "The professor for this course is Professor Chida and her office hours are --")
                response.confidence = 1
            elif ("TA" in input_text or "ta" in input_text) and ("information" in input_text or "Information" in input_text):
                response = Statement(text = "The TA for this course is Akshay Jha and their office hours are --")
                response.confidence = 1
            elif ("next" in input_text or "Next" in input_text) and "quiz" in input_text:
                response = Statement(text = "The next quiz for algorithms is Quiz X on --/--/----. The quiz is over ---")
                response.confidence = 1
            elif ("next" in input_text or "Next" in input_text) and "test" in input_text:
                response = Statement(text = "The next test is Test X on --/--/----. The test covers ---")
                response.confidence = 1
            elif ("dynamic" in input_text or "Dynamic" in input_text) and "programming" in input_text:
                response = Statement(text = "Dynamic Programming (DP) is an algorithmic technique for solving an optimization problem by breaking it down into simpler subproblems and utilizing the fact that the optimal solution to the overall problem depends upon the optimal solution to its subproblems.")
                response.confidence = 1
        elif ">=" in input_text or "==" in input_text or "<=" in input_text or "faster" in input_text or "quickly" in input_text or "slowly" in input_text or "slower" in input_text or "same" in input_text:
            regex = "[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+|[+/*-]"
            if ">=" in input_text or "faster" in input_text or "quickly" in input_text:
                if ">=" in input_text:
                    i = input_text.index(">")
                    exp1 = input_text[:i]
                    exp2 = input_text[i+2:]
                elif "faster" in input_text:
                    i = input_text.index("f")
                    exp1 = input_text[:i]
                    exp2 = input_text[i+6:]
                elif "quickly" in input_text:
                    i = input_text.index("q")
                    exp1 = input_text[:i]
                    exp2 = input_text[i+7:i]

                one = re.findall(regex, exp1)
                two = re.findall(regex, exp2)
                parsed1 = ' '.join(one)
                parsed2 = ' '.join(two)
                f1 = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed1)
                f2 = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed2)
                res = self.compareBigO(f1, f2)
                run1 = self.checkRuntime(f1)
                run2 = self.checkRuntime(f2)
                if ">=" == res:
                    response = Statement(text = "True, the running time for function 1 is " + run1 + " which grows at a faster rate than function 2's running time, " + run2)
                    response.confidence = 1
                elif "==" == res:
                    response = Statement(text = "False, the running time for function 1 is " + run1 + " which grows at the same rate as function 2's running time, " + run2)
                    response.confidence = 1
                elif "<=" == res:
                    response = Statement(text = "False, the running time for function 1 is " + run1 + " which does not grow faster than the running time for function 2, " + run2)
                    response.confidence = 1
            elif "==" in input_text or "same" in input_text:
                if "==" in input_text:
                    i = input_text.index("=")
                    exp1 = input_text[:i]
                    exp2 = input_text[i+2:]
                elif "same" in input_text:
                    i = input_text.index("s")
                    exp1 = input_text[:i]
                    exp2 = input_text[i+4:i]

                one = re.findall(regex, exp1)
                two = re.findall(regex, exp2)
                parsed1 = ' '.join(one)
                parsed2 = ' '.join(two)
                f1 = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed1)
                f2 = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed2)
                res = self.compareBigO(f1, f2)
                run1 = self.checkRuntime(f1)
                run2 = self.checkRuntime(f2)
                if ">=" == res:
                    response = Statement(text = "False, the running time for function 1 is " + run1 + " which does not grow at the same rate as function 2's running time, " + run2)
                    response.confidence = 1
                elif "==" == res:
                    response = Statement(text = "True, the running time for function 1 is " + run1 + " which grows at the same rate as function 2's running time, " + run2)
                    response.confidence = 1
                elif "<=" == res:
                    response = Statement(text = "False, the running time for function 1 is " + run1 + " which does not grow at the same rate as function 2's running time, " + run2)
                    response.confidence = 1
            elif "<=" in input_text or "slowly" in input_text or "slower" in input_text: 
                if "<=" in input_text:
                    i = input_text.index("<")
                    exp1 = input_text[:i]
                    exp2 = input_text[i+2:]
                elif "slowly" in input_text or "slower" in input_text:
                    i = input_text.index("s") #incorrect because it gets the s from does 
                    exp1 = input_text[:i]
                    exp2 = input_text[i+6:]

                one = re.findall(regex, exp1)
                two = re.findall(regex, exp2)
                parsed1 = ' '.join(one)
                parsed2 = ' '.join(two)
                f1 = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed1)
                f2 = re.findall("[a-zA-Z]!|[a-zA-Z0-9]+\^[a-zA-Z0-9]+|[a-zA-Z]*log[a-zA-Z]|[0-9]+", parsed2)
                res = self.compareBigO(f1, f2)
                run1 = self.checkRuntime(f1)
                run2 = self.checkRuntime(f2)
                if ">=" == res:
                    response = Statement(text = "False, the running time for function 1 is " + run1 + " which does not grow at a faster rate than function 2's running time, " + run2)
                    response.confidence = 1
                elif "==" == res:
                    response = Statement(text = "False, the running time for function 1 is " + run1 + " which is not equal to the running time for function 2, " + run2) 
                    response.confidence = 1
                elif "<=" == res:
                    response = Statement(text = "True, the running time for function 1 is " + run1 + " which grows at a slower rate than function 2's running time, " + run2)
                    response.confidence = 1

        return response

    def checkSorts(self, algo):
        if "sort" in algo:
            if "bubble" in algo or "Bubble" in algo:
                return self.getRuntime(bubbleSort)
            if "quick" in algo or "Quick" in algo:
                return self.getRuntime(quickSort)
            if "selection" in algo or "Selection" in algo:
                return self.getRuntime(selectionSort)
            if "insertion" in algo or "Insertion" in algo:
                return self.getRuntime(insertSort)

        if "search" in algo:
            if "binary" in algo or "Binary" in algo:
                print("binary") 
                return self.getRuntime(binarySearch)

    def checkBigO(self, expression):
        runtime = "1"
        curr = "1"
        fast = "1"
        print(expression)

        for exp in expression:
            if "!" in exp:
                fast = "!"
                curr = self.checkFaster(fast, curr)
                if curr == fast:
                    runtime = "N!"
            elif "^" in exp:
                i = exp.index("^")
                if exp[i+1:].isalpha():
                    fast = "^N"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = exp[:i + 1] + "N"
                else:
                    fast = "^X"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "N^" + exp[i + 1:]
            elif "log" in exp:
                i = exp.index("log")
                if i == 0:
                    fast = "logn"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "log N"
                else:
                    fast = "nlogn"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "N log N"

        return "The Big O runtime for this expression is O(" + runtime + ")."

    def checkFaster(self, fast, curr):
        print(fast + " " + curr)
        if fast == "!":
            return fast
        elif fast == "^N":
            if curr == "!":
                return curr
            else:
                return fast
        elif fast == "^X":
            if curr == "!" or curr == "^N":
                return curr
            else:
                return fast
        elif fast == "nlogn":
            if curr == "!" or curr == "^N" or curr == "^X":
                return curr
            else:
                return fast
        elif fast == "n":
            if curr == "!" or curr == "^N" or curr == "^X" or curr == "nlogn":
                return curr
            else:
                return fast
        elif fast == "logn":
            if curr == "!" or curr == "^N" or curr == "^X" or curr == "nlogn":
                return curr
            else:
                return fast
        else:
            return "1"

    def compareBigO(self, f1, f2):
        one = self.getBigO(f1)
        two = self.getBigO(f2)
        res = self.checkFaster(one, two)
        equality = ""

        if res == one and res == two:
            equality = "=="
        elif res == one:
            equality = ">="
        else:
            equality = "<="

        return equality


    def getBigO(self, expression):
        runtime = "1"
        curr = "1"
        fast = "1"
        print(expression)

        for exp in expression:
            if "!" in exp:
                fast = "!"
                curr = self.checkFaster(fast, curr)
                if curr == fast:
                    runtime = "!"
            elif "^" in exp:
                i = exp.index("^")
                if exp[i+1:].isalpha():
                    fast = "^N"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "^N"
                else:
                    fast = "^X"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "^X"
            elif "log" in exp:
                i = exp.index("log")
                if i == 0:
                    fast = "logn"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "logn"
                else:
                    fast = "nlogn"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "nlogn"
        
        return runtime

    def checkRuntime(self, expression):
        runtime = "1"
        curr = "1"
        fast = "1"
        print(expression)

        for exp in expression:
            if "!" in exp:
                fast = "!"
                curr = self.checkFaster(fast, curr)
                if curr == fast:
                    runtime = "N!"
            elif "^" in exp:
                i = exp.index("^")
                if exp[i+1:].isalpha():
                    fast = "^N"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = exp[:i + 1] + "N"
                else:
                    fast = "^X"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "N^" + exp[i + 1:]
            elif "log" in exp:
                i = exp.index("log")
                if i == 0:
                    fast = "logn"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "log N"
                else:
                    fast = "nlogn"
                    curr = self.checkFaster(fast, curr)
                    if curr == fast:
                        runtime = "N log N"

        return "O(" + runtime + ")"

    def getRuntime(self, algo):
        return "The best case runtime is " + algo["best"] + ", the average case runtime is " + algo["average"] + ", and the worst case runtime is " + algo["worst"]