from src.data_service import F1DataService

def test_available():
    s = F1DataService()
    assert s.available()
    assert 2024 in s.seasons()
