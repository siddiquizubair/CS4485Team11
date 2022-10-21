from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

app = Flask(__name__)

algo_bot = ChatBot(
    "Algo-Bot", 
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters = [
        'chatterbot.logic.MathematicalEvaluation',
        {
            'import_path': 'AlgorithmEvaluation.AlgorithmLogic',
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I\'m sorry, but I don\'t understand your question. Please refer to your course on eLearning or contact Professor Chida.',
            'maximum_similarity_threshold': 0.8
        }
    ],
    preprocessors = [
        'chatterbot.preprocessors.clean_whitespace'
    ]
)

trainer = ChatterBotCorpusTrainer(algo_bot)
listTrainer = ListTrainer(algo_bot)
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

listTrainer.train([
    "I have a question about algorithms",
    "I'm happy to help with any questions you might ask."
    "I have some questions about runtime",
    "I can tell you the runtime and Big O of any expression you enter."
])

listTrainer.train([
    "I need help with my homework",
    "I can help you through it!"
])

listTrainer.train([
    "I need help",
    "I can try to help (with algorithms)." 
])

listTrainer.train([
    "Selection sort",
    "Would you like to learn more about selection sort?",
    "I would",
    "Selection sort divides the input list into two parts: a sorted sublist of items which is built up from left to <br>right at the front (left) of the list and a sublist of the remaining unsorted items that occupy the rest of<br> the list. Initially, the sorted sublist is empty and the unsorted sublist is the entire input list. The algorithm<br> proceeds by finding the smallest (or largest, depending on sorting order) element in the unsorted sublist, <br>exchanging (swapping) it with the leftmost unsorted element (putting it in sorted order), and moving the <br>sublist boundaries one element to the right."
])

listTrainer.train([
    "Bubble sort",
    "Would you like to learn more about bubble sort?",
    "I would",
    "Bubble sort is a simple sorting algorithm that repeatedly steps through the input list element by element,<br>comparing the current element with the one after it, swapping their values if needed.These passes<br> through the list are repeated until no swaps had to be performed during a pass, meaning that the list<br> has become fully sorted."
])

listTrainer.train([
    "Quicksort",
    "Would you like to learn more about quicksort?",
    "I would",
    "Quicksort is a divide-and-conquer algorithm. It works by selecting a 'pivot' element from <br>the array and partitioning the other elements into two sub-arrays, according to whether they<br> are less than or greater than the pivot. For this reason, it is sometimes called partition-exchange sort.<br>The sub-arrays are then sorted recursively."
])

@app.route("/")
def chatPage():
    return render_template("index.html")

@app.route("/get")
def get_response():
    userText = request.args.get('msg')
    return str(algo_bot.get_response(userText))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
