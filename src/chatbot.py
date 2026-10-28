from src.data_service import F1DataService

class Chatbot:
    def __init__(self):
        self.data = F1DataService()

    def ask(self, message: str):
        msg = message.lower()
        # Structured responses based on keywords
        if "2021" in msg and "champion" in msg and "driver" in msg:
            return {
                "answer": f"The 2021 Drivers' Championship was won by {self.data.driver_champion(2021)}.",
                "sources": [{"name":"F1 Official Results","url":"https://www.formula1.com/en/results/"}],
                "season": 2021,
                "retrieval": "structured"
            }
        if "2025" in msg and "constructor" in msg and "champion" in msg:
            return {
                "answer": f"The 2025 Constructors' Championship was won by {self.data.constructor_champion(2025)}.",
                "sources": [{"name":"F1 Official Results","url":"https://www.formula1.com/en/results/"}],
                "season": 2025,
                "retrieval": "structured"
            }
        if "standings" in msg and "2024" in msg:
            s = self.data.standings_2024()
            drivers = ", ".join([f"{d['position']}. {d['driver']} ({d['points']})" for d in s.get("drivers", [])])
            return {
                "answer": f"2024 Drivers' Championship: {drivers}. Constructors: McLaren (666 pts), Red Bull (516 pts).",
                "sources": [{"name":"F1 Official Results","url":"https://www.formula1.com/en/results/"}],
                "season": 2024,
                "retrieval": "structured"
            }
        # Default fallback with source citation
        return {
            "answer": "I can answer factual F1 questions for 2021-2025 using structured data. Try asking: Who won the 2021 Drivers' Championship? Which 2024 weekends had sprint races? Show 2022 Constructors' standings.",
            "sources": [{"name":"F1 History AI Chatbot documentation","url":"https://github.com/f1-history-ai-chatbot"}],
            "retrieval": "fallback"
        }
