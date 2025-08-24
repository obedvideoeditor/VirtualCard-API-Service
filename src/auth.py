from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.config import JWT_SECRET_KEY

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user
