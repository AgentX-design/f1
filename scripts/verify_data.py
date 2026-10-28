"""Generate a data coverage report for the F1 fixtures."""
import json, os
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_service import F1DataService

def verify():
    s = F1DataService()
    with open(s.data.data.get("fixture_path", "data/fixtures/f1_seasons.json") if False else "data/fixtures/f1_seasons.json", encoding="utf-8") as f:
        fixture = json.load(f)
    report = {
        "project": "F1 History AI Chatbot",
        "fixture_path": "data/fixtures/f1_seasons.json",
        "seasons_covered": fixture.get("seasons", []),
        "download_attempts": {},
        "categories_available": {},
        "categories_missing": {},
        "records_per_season": {},
        "verified_notes": fixture.get("data_coverage_note", "No note."),
        "missing_data_disclosure": "Full race-by-race grids for every Grand Prix across all seasons are not fully loaded to prevent unverified statistics. Only verified champions, selected race winners, 2024 standings, sprint notes, and season highlights are included."
    }
    # Count race winners per season
    for season in fixture.get("seasons", []):
        race_winners = fixture.get("race_winners_sample", {}).get(str(season), {})
        sprints = fixture.get("sprint_notes", {}).get(str(season), [])
        report["records_per_season"][str(season)] = {
            "race_winners_sample": len(race_winners),
            "sprint_events": len(sprints),
            "championship_data": bool(fixture.get("championships", {}).get(str(season))),
            "standings_2024_full": season == 2024,
        }
    # Category availability
    for cat in ["championships", "race_winners_sample", "standings_2024", "standings_2022_summary", "standings_2023_summary", "qualifying_notes", "sprint_notes", "season_highlights"]:
        available = cat in fixture
        report["categories_available"][cat] = available
        if not available:
            report["categories_missing"][cat] = "Not present in fixture."
    # Download attempts
    if os.path.exists("data/raw/download_report.json"):
        with open("data/raw/download_report.json", encoding="utf-8") as f:
            dl = json.load(f)
        report["download_attempts"] = {a["name"]: a["status"] for a in dl.get("attempts", [])}
    else:
        report["download_attempts"] = "No download report found."
    # Vector index status
    report["vector_index_available"] = os.path.exists("chroma_db/index.json")
    # Print clearly
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    verify()
