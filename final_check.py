from src.chatbot import Chatbot
bot = Chatbot()
queries = [
    "Who won 2021 Drivers Championship?",
    "Who won 2022 Constructors Championship?",
    "Give 2023 Monaco Grand Prix winner",
    "Which 2024 weekends had sprint races",
    "Show 2024 Drivers Championship standings",
    "Show 2022 season highlights",
    "What was the qualifying note for 2024 British Grand Prix?",
    "Give 2023 race winners",
    "Unknown mystery 9999",
]
for q in queries:
    r = bot.ask(q)
    print(f"Q: {q}")
    print(f"  STATUS: {r['retrieval']} | SEASON: {r.get('season')} | ANSWER: {r['answer'][:90]}...")
