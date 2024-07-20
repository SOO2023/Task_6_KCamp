from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
import util
from database import db_session
from authentication import get_user


router = APIRouter(prefix="/users/blogs", tags=["Blogs"])


@router.get("/", response_model=list[schemas.BlogOut])
def get_all_blogs(
    user_class: schemas.Payload = Depends(get_user), db: Session = Depends(db_session)
):
    util.verify_user_admin(user_class, "user")
    user_id = user_class.user_id
    all_posts = util.get_all_items(QueryClass=models.Blogs, user_id=user_id, db=db)
    return all_posts


@router.get("/{blog_id}", response_model=schemas.BlogOut)
def get_blog(
    *,
    user_class: schemas.Payload = Depends(get_user),
    blog_id: int,
    db: Session = Depends(db_session),
):
    util.verify_user_admin(user_class, "user")
    user_id = user_class.user_id
    blog = util.get_item_by_id(
        item_id=blog_id, user_id=user_id, QueryClass=models.Blogs, db=db
    )
    return blog


@router.post("/", response_model=schemas.BlogOut, status_code=201)
def create_blog(
    *,
    user_class: schemas.Payload = Depends(get_user),
    blog: schemas.Blog,
    db: Session = Depends(db_session),
):
    util.verify_user_admin(user_class, "user")
    user_id = user_class.user_id
    blog_dict = blog.model_dump()
    blog_dict.update({"user_id": user_id})
    blog = util.create_item(blog_dict, models.Blogs, db)
    return blog


@router.put("/{blog_id}", response_model=schemas.BlogOut, status_code=201)
def update_blog(
    *,
    blog_id: int,
    user_class: schemas.Payload = Depends(get_user),
    update_post: schemas.Blog,
    db: Session = Depends(db_session),
):
    util.verify_user_admin(user_class, "user")
    user_id = user_class.user_id
    update_dict = update_post.model_dump()
    new_item = util.update_item(blog_id, user_id, update_dict, models.Blogs, db)
    return new_item


@router.delete("/{blog_id}")
def delete_blog(
    blog_id: int,
    user_class: schemas.Payload = Depends(get_user),
    db: Session = Depends(db_session),
):
    util.verify_user_admin(user_class, "user")
    user_id = user_class.user_id
    util.delete_item(blog_id, user_id, models.Blogs, db)
    return Response(status_code=204)
