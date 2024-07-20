from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import schemas

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")


def password_hasher(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(password, hash_password)


def verify_user(email, password: str, ModelClass, db: Session):
    user = db.query(ModelClass).filter(ModelClass.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    hash_password = user.password
    if not verify_password(password, hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def jwt_encoder(payload: dict, exp: int) -> str:
    exp_date = datetime.now() + timedelta(minutes=exp)
    exp_stamp = datetime.timestamp(exp_date)
    payload.update({"exp": exp_stamp})
    encoded_str = jwt.encode(payload, SECRET, ALGORITHM)
    return encoded_str


def jwt_decoder(token: str):
    payload = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGORITHM])
    return payload


def get_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt_decoder(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        payload_class = schemas.Payload(
            user_id=payload.get("user_id"), role=payload.get("role")
        )
        return payload_class
