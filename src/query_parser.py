import re

class QueryParser:
    def parse(self, text: str) -> dict:
        text = text.lower()
        season = None
        for y in [2021, 2022, 2023, 2024, 2025]:
            if str(y) in text:
                season = y
                break
        return {"raw": text, "season": season, "intent": "history"}
