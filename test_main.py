from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_home():
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == "Hello World"

def test_return_405_error_for_send_message_without_parameters():
    resp = client.post('/')
    assert resp.status_code == 405

def test_return_error_without_message():
    resp = client.post(
        '/',
        headers={'Content-Type':'application/json'},
        json={'from_context': ''}
    )
    assert resp.status_code == 405

def test_message_success():
    resp = client.post(
        '/',
        headers={'Content-Type':'application/json'},
        json={'from_context': '','message':'hi'}
    )
    assert resp.status_code == 200