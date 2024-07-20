from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy_to_pydantic import sqlalchemy_to_pydantic
import models


def sql_obj_to_pydantic(sql_obj, ModelClass) -> dict:
    PydanticObj = sqlalchemy_to_pydantic(ModelClass)
    pydantic_obj = PydanticObj.model_validate(sql_obj)
    return pydantic_obj.model_dump()


def get_all_items(*, QueryClass, user_id: int | None = None, db: Session):
    if user_id is None:
        all_items = db.query(QueryClass).all()
    else:
        all_items = db.query(QueryClass).filter(QueryClass.user_id == user_id).all()
    return all_items


def get_item_by_id(*, item_id, user_id: int | None = None, QueryClass, db: Session):
    if user_id is None:
        item = db.query(QueryClass).filter(QueryClass.id == item_id).first()
    else:
        item = (
            db.query(QueryClass)
            .filter((QueryClass.user_id == user_id) & (QueryClass.id == item_id))
            .first()
        )
    if not item:
        raise HTTPException(status_code=404, detail={"message": "Invalid item id."})
    return item


def create_item(item_dict: dict, ModelClass, db: Session):
    try:
        item = ModelClass(**item_dict)
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(e).split(":")[0], "full": str(e)},
        )
    else:
        return item


def update_item(item_id, user_id, update_dict: dict, QueryClass, db: Session):
    query_obj = db.query(QueryClass).filter(
        (QueryClass.user_id == user_id) & (QueryClass.id == item_id)
    )
    if not query_obj.first():
        raise HTTPException(status_code=404, detail={"message": "Invalid item id."})
    query_obj.update(update_dict)
    db.commit()
    return query_obj.first()


def delete_item(item_id, user_id, QueryClass, db: Session):
    query_obj = db.query(QueryClass).filter(
        (QueryClass.user_id == user_id) & (QueryClass.id == item_id)
    )
    if not query_obj.first():
        raise HTTPException(status_code=404, detail={"message": "Invalid item id."})
    query_obj.delete()
    db.commit()


def verify_user_admin(class_obj, role: str):
    if role == "user":
        if class_obj.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Only user can access this endpoint"},
            )
    else:
        if class_obj.role == "user":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Only admin can access this endpoint"},
            )


def verify_item(item_id, ModelClass, db: Session, name: str = "item"):
    item = db.query(ModelClass).filter(ModelClass.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"{name} id is invalid"},
        )


def verify_quantity(
    quantity,
    db: Session,
    create=True,
    order_id: int | None = None,
    product_id: int | None = None,
):
    if product_id and create:
        product = (
            db.query(models.Products).filter(models.Products.id == product_id).first()
        )
        if product.available == False:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"Product {product_id} is curently out of stock. Check back some other time",
                    "available": product.available,
                },
            )
        if quantity > product.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"The available quantity of product {product_id} is {product.available_quantity}",
                    "available_qty": product.available_quantity,
                    "quantity_ordered": quantity,
                },
            )
    else:
        order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
        product = (
            db.query(models.Products)
            .filter(models.Products.id == order.product_id)
            .first()
        )
        product.available_quantity += order.quantity
        db.commit()

    if product.available_quantity > 0:
        product.available_quantity = product.available_quantity - quantity
        db.commit()
    if product.available_quantity == 0:
        product.available = False
        db.commit()
    if product.available_quantity > 0 and product.available == False:
        product.available = True
        db.commit()
    if quantity > 0:
        return product


def order_out(order, product_id, db):
    order_dict = sql_obj_to_pydantic(order, models.Orders)
    prod_obj = get_item_by_id(item_id=product_id, QueryClass=models.Products, db=db)
    prod_dict = sql_obj_to_pydantic(prod_obj, models.Products)
    prod_dict_extracted = {
        "product_id": prod_dict["id"],
        "product_name": prod_dict["name"],
        "product_category": prod_dict["category"],
    }
    order_dict.update({"product_info": prod_dict_extracted})
    return order_dict
