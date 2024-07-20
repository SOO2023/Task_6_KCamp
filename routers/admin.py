from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
import util
from database import db_session
from authentication import get_user


router = APIRouter(prefix="/admins", tags=["Admin"])


@router.get("/blogs", response_model=list[schemas.BlogOut])
def get_all_blogs(
    user_class: schemas.Payload = Depends(get_user), db: Session = Depends(db_session)
):
    util.verify_user_admin(user_class, "admin")
    all_posts = util.get_all_items(QueryClass=models.Blogs, db=db)
    return all_posts


@router.get("/blogs/{blog_id}", response_model=schemas.BlogOut)
def get_blog(
    *,
    user_class: schemas.Payload = Depends(get_user),
    blog_id: int,
    db: Session = Depends(db_session),
):
    util.verify_user_admin(user_class, "admin")
    blog = util.get_item_by_id(item_id=blog_id, QueryClass=models.Blogs, db=db)
    return blog


@router.get("/users", response_model=list[schemas.UserOutList])
def get_all_users(
    user_class: schemas.Payload = Depends(get_user), db: Session = Depends(db_session)
):
    util.verify_user_admin(user_class, "admin")
    all_users = util.get_all_items(QueryClass=models.Users, db=db)
    return all_users
