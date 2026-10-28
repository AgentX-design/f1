from src.data_service import F1DataService

SAMPLE_GP_ALIASES = {
    "british grand prix": "British Grand Prix",
    "the british grand prix": "British Grand Prix",
    "bahrain grand prix": "Bahrain Grand Prix",
    "monaco grand prix": "Monaco Grand Prix",
    "hungary grand prix": "Hungary Grand Prix",
    "belgium grand prix": "Belgium Grand Prix",
}


class Chatbot:
    def __init__(self):
        self.data = F1DataService()

    @staticmethod
    def _year(msg: str) -> int | None:
        for y in [2021, 2022, 2023, 2024, 2025]:
            if str(y) in msg:
                return y
        return None

    def ask(self, message: str):
        msg = message.lower().strip()
        sources = [
            {
                "name": "Formula 1 Official Results",
                "url": "https://www.formula1.com/en/results/",
            },
            {"name": "FIA Official Documents", "url": "https://www.fia.com/"},
        ]

        # Season highlights / narrative summaries when year is asked generally
        y = self._year(msg)
        if y is not None and ("season" in msg or "history" in msg or "summary" in msg or "highlight" in msg):
            highlights = self.data.season_highlights(y)
            return {
                "answer": f"{y} season highlights: {highlights}",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [{"season": y, "category": "season_highlights"}],
            }

        # Standings
        if "standings" in msg:
            y = self._year(msg) or 2024
            if y == 2024:
                s = self.data.standings_2024()
                drivers = ", ".join(
                    [
                        f"{d['position']}. {d['driver']} ({d['points']})"
                        for d in s.get("drivers", [])
                    ]
                )
                constructors = ", ".join(
                    [
                        f"{d['position']}. {d['constructor']} ({d['points']})"
                        for d in s.get("constructors", [])
                    ]
                )
                return {
                    "answer": f"2024 Drivers': {drivers}. Constructors: {constructors}.",
                    "sources": sources,
                    "season": 2024,
                    "retrieval": "structured",
                    "retrieval_results": [{"season": 2024, "category": "standings"}],
                }
            # For other years, provide verified champions and note limitation
            summary = self.data.standings_summary(y)
            return {
                "answer": f"The {y} Drivers' champion was {summary['drivers_champion']}; constructor champion was {summary['constructor_champion']}. {summary.get('note', '')}",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [{"season": y, "category": "standings_summary"}],
            }

        # Drivers' Championship winner
        if ("champion" in msg or "championship" in msg) and (
            "driver" in msg or "drivers" in msg
        ):
            y = self._year(msg)
            if y is None:
                y = 2024
            return {
                "answer": f"The {y} Drivers' Championship was won by {self.data.driver_champion(y)}.",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [{"season": y, "category": "driver_champion"}],
            }

        # Constructors' Championship winner
        if ("champion" in msg or "championship" in msg) and "constructor" in msg:
            y = self._year(msg)
            if y is None:
                y = 2024
            return {
                "answer": f"The {y} Constructors' Championship was won by {self.data.constructor_champion(y)}.",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [
                    {"season": y, "category": "constructor_champion"}
                ],
            }

        # Sprint events
        if "sprint" in msg:
            y = self._year(msg) or 2024
            events = self.data.sprint_events(y)
            if events:
                return {
                    "answer": f"The {y} sprint races included: {', '.join(events)}.",
                    "sources": sources,
                    "season": y,
                    "retrieval": "structured",
                    "retrieval_results": [{"season": y, "category": "sprint_events"}],
                }
            return {
                "answer": f"{y} sprint events not fully loaded in fixtures.",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
            }

        # Qualifying / pole
        if ("qualifying" in msg or "pole" in msg or "grid" in msg) and y is not None:
            gp = "British Grand Prix"
            for alias, canonical in SAMPLE_GP_ALIASES.items():
                if alias in msg:
                    gp = canonical
                    break
            note = self.data.qualifying_note(y, gp)
            return {
                "answer": f"{y} qualifying note: {note}.",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [{"season": y, "gp": gp, "category": "qualifying_note"}],
            }


        # Race winners (specific GP)
        gp = None
        for alias, canonical in SAMPLE_GP_ALIASES.items():
            if alias in msg:
                gp = canonical
                break
        y = self._year(msg)
        if gp and y is not None:
            w = self.data.race_winner(y, gp)
            return {
                "answer": f"{y} {gp} winner: {w if w else 'not available'}.",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [{"season": y, "gp": gp, "category": "race_winner"}],
            }

        # Race winners (sample list when no GP specified)
        if y is not None and (
            "race" in msg or "winner" in msg or "grand prix" in msg
        ):
            sample = self.data.data.get("race_winners_sample", {}).get(str(y), {})
            if sample:
                items = ", ".join(
                    [f"{k}: {v}" for k, v in list(sample.items())[:4]]
                )
                return {
                    "answer": f"Sample {y} race winners: {items}.",
                    "sources": sources,
                    "season": y,
                    "retrieval": "structured",
                    "retrieval_results": [{"season": y, "category": "race_winners_sample"}],
                }

        # Fallback with distinct helpful text
        return {
            "answer": "I can answer factual F1 questions for 2021-2025 using structured fixtures. Try asking: Who won the 2021 Drivers' Championship? Who won the 2022 Constructors' Championship? Show 2024 Drivers' Championship standings. Which 2023 weekends had sprint races? Give the 2023 Monaco winner. Show 2022 season highlights.",
            "sources": [
                {
                    "name": "F1 History AI Chatbot documentation",
                    "url": "https://github.com/f1-history-ai-chatbot",
                }
            ],
            "retrieval": "fallback",
            "retrieval_results": [{"note":"No direct structured evidence matched; please refine your query."}],
        }
