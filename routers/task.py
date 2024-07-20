from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import models, schemas
import util
from database import db_session
from authentication import get_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[schemas.TaskOut])
def get_all_tasks(
    user_class: schemas.Payload = Depends(get_user), db: Session = Depends(db_session)
):
    user_id = user_class.user_id
    all_tasks = util.get_all_items(QueryClass=models.Tasks, user_id=user_id, db=db)
    return all_tasks


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    *,
    user_class: schemas.Payload = Depends(get_user),
    task_id: int,
    db: Session = Depends(db_session),
):
    user_id = user_class.user_id
    task = util.get_item_by_id(
        item_id=task_id, user_id=user_id, QueryClass=models.Tasks, db=db
    )
    return task


@router.post("/", response_model=schemas.TaskOut, status_code=201)
def create_task(
    *,
    user_class: schemas.Payload = Depends(get_user),
    task: schemas.Task,
    db: Session = Depends(db_session),
):
    user_id = user_class.user_id
    task_dict = task.model_dump()
    task_dict.update({"user_id": user_id})
    task = util.create_item(task_dict, models.Tasks, db)
    return task


@router.put("/{task_id}", response_model=schemas.TaskOut, status_code=201)
def update_task(
    *,
    task_id: int,
    user_class: schemas.Payload = Depends(get_user),
    update_task: schemas.TaskUpdate,
    db: Session = Depends(db_session),
):
    user_id = user_class.user_id
    update_dict = update_task.model_dump()
    new_task = util.update_item(task_id, user_id, update_dict, models.Tasks, db)
    return new_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    user_class: schemas.Payload = Depends(get_user),
    db: Session = Depends(db_session),
):
    user_id = user_class.user_id
    util.delete_item(task_id, user_id, models.Tasks, db)
    return Response(status_code=204)
