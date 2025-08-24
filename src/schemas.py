from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class CardCreate(BaseModel):
    card_number: str
    expiry: str
    cvv: str

class Card(BaseModel):
    id: int
    card_number: str
    expiry: str
    cvv: str
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    amount: float
    merchant: str

class Transaction(BaseModel):
    id: int
    card_id: int
    amount: float
    merchant: str
    class Config:
        orm_mode = True
