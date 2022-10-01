from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(name = 'AlgoBot', read_only = True, logic_adapters = ['chatterbot.logic.MathematicalEvaluation', 'chatterbot.logic.BestMatch'])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

while True:
    try:
        bot_input = bot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break