import pytest
from app import app
from src.data_service import F1DataService

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    assert client.get('/').status_code == 200

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'ok'

def test_suggested(client):
    list_ = client.get('/api/suggested')
    assert isinstance(list_.get_json(), list)
    # At least one suggestion per season category
    joined = " ".join([s.lower() for s in list_.get_json()])
    for season in [2021, 2022, 2023, 2024, 2025]:
        for keyword in [str(season)]:
            assert keyword in joined

def test_seasons_endpoint(client):
    r = client.get('/api/seasons')
    data = r.get_json()
    assert r.status_code == 200
    for s in [2021, 2022, 2023, 2024, 2025]:
        assert s in data['seasons']

def test_sources(client):
    data = client.get('/api/sources').get_json()
    assert data['sources']

def test_chat_missing_message(client):
    body = client.post('/api/chat', json={}).get_json()
    assert body.get('error') == 'message required'
    assert body.get('error') == 'message required'  # first key
    assert not body.get('result', False) or 'result' not in body

def test_chat_invalid_json(client):
    body = client.post('/api/chat', data="not json", content_type="application/json").get_json()
    # get_json returns None when invalid -> treated as {}
    assert body is None or (isinstance(body, dict) and ('result' in body or 'error' in body))

def test_chat_structured_all_seasons(client):
    bot = F1DataService()
    for season in [2021, 2022, 2023, 2024, 2025]:
        ans = client.post('/api/chat', json={'message': f'Who won the {season} Drivers Championship?'}).get_json()['result']['answer']
        assert f"{season}" in ans and "won by" in ans
        assert bot.driver_champion(season) in ans

def test_chat_constructors_all_seasons(client):
    bot = F1DataService()
    for season in [2021, 2022, 2023, 2024, 2025]:
        ans = client.post('/api/chat', json={'message': f'Who won the {season} Constructors Championship?'}).get_json()['result']['answer']
        assert f"{season}" in ans and "won by" in ans
        assert bot.constructor_champion(season) in ans

def test_chat_standings_2024_full(client):
    r = client.post('/api/chat', json={'message':'Show 2024 Drivers Championship standings'})
    ans = r.get_json()['result']['answer']
    assert 'McLaren' in ans
    assert 'Red Bull' in ans
    assert 'Max Verstappen' in ans

def test_chat_standings_other_season_summary(client):
    r = client.post('/api/chat', json={'message':'Show 2022 standings'})
    ans = r.get_json()['result']['answer']
    assert 'Verstappen' in ans
    assert 'Red Bull' in ans
    # Should mention limitation about full grid
    assert 'grid table' in ans.lower()

def test_chat_sprint_events_2024(client):
    r = client.post('/api/chat', json={'message':'Which 2024 weekends had sprint races'})
    ans = r.get_json()['result']['answer']
    assert 'Chinese Grand Prix' in ans

def test_chat_sprint_events_2023(client):
    r = client.post('/api/chat', json={'message':'Which 2023 weekends had sprint races'})
    ans = r.get_json()['result']['answer']
    assert 'Bahrain Grand Prix' in ans

def test_chat_race_winners_monaco_2023(client):
    r = client.post('/api/chat', json={'message':'Give the 2023 Monaco Grand Prix winner'})
    ans = r.get_json()['result']['answer']
    assert 'Verstappen' in ans

def test_chat_race_winners_2021(client):
    r = client.post('/api/chat', json={'message':'Give the 2021 Abu Dhabi Grand Prix winner'})
    ans = r.get_json()['result']['answer']
    assert 'Verstappen' in ans

def test_chat_highlights_2022(client):
    r = client.post('/api/chat', json={'message':'Show 2022 season highlights'})
    ans = r.get_json()['result']['answer']
    assert 'highlights' in ans.lower()

def test_chat_qualifying_note(client):
    r = client.post('/api/chat', json={'message':'What was the qualifying note for 2024 British Grand Prix?'})
    ans = r.get_json()['result']['answer']
    assert 'George Russell on pole' in ans

def test_chat_distinct_answers(client):
    r1 = client.post("/api/chat", json={"message":"Who won 2024 Drivers Championship?"})
    r2 = client.post("/api/chat", json={"message":"Show 2023 season highlights"})
    r3 = client.post("/api/chat", json={"message":"Who won 2022 Constructors Championship?"})
    a = r1.get_json()["result"]["answer"]
    b = r2.get_json()["result"]["answer"]
    c = r3.get_json()["result"]["answer"]
    assert a != b and b != c

def test_chat_unknown_gives_fallback(client):
    r = client.post('/api/chat', json={'message':'What happened in 2019 in Formula 1?'})
    ans = r.get_json()['result']['answer']
    assert 'try asking' in ans.lower() or 'limited' in ans.lower() or 'unavailable' in ans.lower()

def test_index_has_sections(client):
    html = client.get('/').data.decode('utf-8').lower()
    for section in ['f1 history intelligence', 'season explorer', 'what you can explore', 'ask ai']:
        assert section in html
