from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
import util
from authentication import password_hasher
from database import db_session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserIn, db: Session = Depends(db_session)):
    user.password = password_hasher(user.password)
    user.role = user.role.value
    user = util.create_item(user.model_dump(), models.Users, db)
    user_dict = util.sql_obj_to_pydantic(user, models.Users)
    user_dict.update(
        {"message": "Your account is created successfully. Kindly login to continue."}
    )
    return user_dict

