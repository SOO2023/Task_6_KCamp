from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import db_session
import models
from authentication import verify_user, jwt_encoder


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)
):
    user = verify_user(form_data.username, form_data.password, models.Users, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credientials.")
    payload = {"user_id": user.id, "role": user.role}
    encoded = jwt_encoder(payload, 10)
    return {"access_token": encoded, "token_type": "Bearer"}
