from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# tests/test_api.py
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
