from src.data_service import F1DataService

def verify():
    s = F1DataService()
    report = {
        "seasons_covered": s.seasons(),
        "fixture_path": "data/fixtures/f1_seasons.json",
        "data_categories": ["championships", "race_winners_sample", "standings_2024", "qualifying_notes", "sprint_notes"],
        "pdf_documents_discovered": 0,
        "vector_index_status": "not built" if not __import__("os").path.exists("chroma_db/index.json") else "built"
    }
    print(report)

if __name__ == "__main__":
    verify()
