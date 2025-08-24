from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src import models, schemas, crud, auth, aws_utils
from src.config import get_db

app = FastAPI(title="VirtualCard API Service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/cards", response_model=schemas.Card)
async def create_card(card: schemas.CardCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    db_card = crud.create_card(db, card)
    aws_utils.log_to_s3(f"Card created: {db_card.id}")
    return db_card

@app.get("/cards/{card_id}", response_model=schemas.Card)
async def get_card(card_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    card = crud.get_card(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.post("/cards/{card_id}/transactions", response_model=schemas.Transaction)
async def create_transaction(card_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    db_transaction = crud.create_transaction(db, card_id, transaction)
    aws_utils.log_to_s3(f"Transaction created for card {card_id}: {db_transaction.id}")
    return db_transaction
