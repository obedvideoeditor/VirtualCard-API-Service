import pytest
from fastapi.testclient import TestClient
from src.main import app
from src import models, crud
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://user:password@localhost:5432/test_virtual_cards"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_create_card(client, db):
    crud.create_user(db, "testuser", "testpass")
    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]
    response = client.post(
        "/cards",
        json={"card_number": "1234567890123456", "expiry": "12/27", "cvv": "123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["card_number"] == "1234567890123456"
