from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

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
            'maximum_similarity_threshold': 0.0
        }
    ],
    preprocessors = [
        'chatterbot.preprocessors.clean_whitespace'
    ]
)

trainer = ChatterBotCorpusTrainer(algo_bot)
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations" 
)

@app.route("/")
def chatPage():
    return render_template("index.html")

@app.route("/get")
def get_response():
    userText = request.args.get('msg')
    return str(algo_bot.get_response(userText))


if __name__ == "__main__":
    app.run()
