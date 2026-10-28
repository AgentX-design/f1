from src.chatbot import Chatbot

def test_ask_champion():
    bot = Chatbot()
    r = bot.ask("Who won the 2021 Drivers' Championship?")
    assert "Verstappen" in r['answer']
