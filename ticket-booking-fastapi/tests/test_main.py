import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app, tickets

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tickets():
    tickets.clear()
    yield
    tickets.clear()


def test_index():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Welcome to the Ticket Booking System"}


def test_add_and_get_tickets():
    ticket = {
        "id": 1,
        "flight_name": "Test Flight",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    }
    r = client.post("/ticket", json=ticket)
    assert r.status_code == 201
    assert r.json() == ticket

    r = client.get("/ticket")
    assert r.status_code == 200
    assert r.json() == [ticket]


def test_update_ticket():
    ticket = {
        "id": 1,
        "flight_name": "Test Flight",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    }
    client.post("/ticket", json=ticket)

    updated = ticket.copy()
    updated["destination"] = "Chittagong"
    r = client.put("/ticket/1", json=updated)
    assert r.status_code == 200
    assert r.json()["destination"] == "Chittagong"


def test_delete_ticket():
    ticket = {
        "id": 1,
        "flight_name": "Test Flight",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    }
    client.post("/ticket", json=ticket)

    r = client.delete("/ticket/1")
    assert r.status_code == 200
    assert r.json() == ticket

    r2 = client.get("/ticket")
    assert r2.json() == []
