import json
import os
from typing import Any, Dict, List

from config import DATA_DIR

FIXTURES_PATH = os.path.join(DATA_DIR, "fixtures", "f1_seasons.json")


def load_fixture():
    with open(FIXTURES_PATH, encoding="utf-8") as f:
        return json.load(f)


class F1DataService:
    def __init__(self) -> None:
        self.data = load_fixture()

    def seasons(self):
        return self.data["seasons"]

    def driver_champion(self, season: int) -> str:
        d = self.data["championships"].get(str(season), {})
        return d.get("driver_champion", "") or "not available"

    def constructor_champion(self, season: int) -> str:
        d = self.data["championships"].get(str(season), {})
        return d.get("constructor_champion", "") or "not available"

    def race_winner(self, season: int, gp: str) -> str:
        winners = self.data["race_winners_sample"].get(str(season), {})
        return winners.get(gp, "") or "not available"

    def standings_2024(self) -> Dict[str, Any]:
        return self.data["standings_2024"]

    def qualifying_note(self, season: int, gp: str) -> str:
        q = self.data["qualifying_notes"].get(str(season), {})
        return q.get(gp, "") or "not available"

    def sprint_events(self, season: int) -> List[str]:
        notes = self.data.get("sprint_notes", {}).get(str(season), [])
        if isinstance(notes, list):
            return notes
        return []

    def standings_summary(self, season: int) -> Dict[str, Any]:
        key = f"standings_{season}_summary"
        if key in self.data:
            return self.data[key]
        return {
            "drivers_champion": self.driver_champion(season),
            "constructor_champion": self.constructor_champion(season),
            "note": "Full grid table not loaded for this season."
        }

    def season_highlights(self, season: int) -> str:
        return self.data.get("season_highlights", {}).get(str(season), "No summary available.")

    def available(self) -> bool:
        try:
            return os.path.exists(FIXTURES_PATH)
        except OSError:
            return False


__all__ = ["F1DataService", "load_fixture"]
