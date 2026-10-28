import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'ok'

def test_suggested(client):
    resp = client.get('/api/suggested')
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_chat(client):
    resp = client.post('/api/chat', json={"message":"Who won 2021 Drivers' Championship?"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'result' in data
