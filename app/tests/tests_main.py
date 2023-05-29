from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_transaction_debit_success():
    response = client.post("/transaction", json={"amount": 100, "kind": 0})
    assert response.status_code == 200


def test_transaction_credit_success():
    response = client.post("/transaction", json={"amount": 100, "kind": 1})
    assert response.status_code == 200


def test_transaction_empty_body():
    response = client.post("/transaction", json={})
    assert response.status_code == 400


def test_transaction_wrong_amount():
    response = client.post("/transaction", json={"amount": -4, "kind": 1})
    assert response.status_code == 400


def test_transaction_wrong_transaction_type():
    response = client.post("/transaction", json={"amount": 100, "kind": 2})
    assert response.status_code == 400


def test_transaction_zero_amount():
    response = client.post("/transaction", json={"amount": 0, "kind": 1})
    assert response.status_code == 400


def test_transaction_list():
    response = client.post("/transactions")
    assert response.status_code == 200
