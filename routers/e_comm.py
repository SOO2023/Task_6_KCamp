from fastapi import APIRouter, Depends, Response, HTTPException, status, Form
from sqlalchemy.orm import Session
import models, schemas
import util
from database import db_session


router = APIRouter()


@router.get(
    "/products", response_model=list[schemas.Product], tags=["E-comms/Products"]
)
def get_all_products(db: Session = Depends(db_session)):
    products = util.get_all_items(QueryClass=models.Products, db=db)
    return products


@router.get(
    "/customers/{customer_id}",
    response_model=schemas.CustomerOut,
    tags=["E-comms/Customer"],
)
def get_customer(customer_id: int, db: Session = Depends(db_session)):
    customer = util.get_item_by_id(
        item_id=customer_id, QueryClass=models.Customers, db=db
    )
    return customer


@router.get(
    "/customers", response_model=list[schemas.CustomerOut], tags=["E-comms/Customer"]
)
def get_all_customers(db: Session = Depends(db_session)):
    customers = util.get_all_items(QueryClass=models.Customers, db=db)
    return customers


@router.post(
    "/customers",
    response_model=schemas.CustomerOut,
    status_code=status.HTTP_201_CREATED,
    tags=["E-comms/Customer"],
)
def create_customer(user: schemas.Customer, db: Session = Depends(db_session)):
    user_dict = user.model_dump()
    user = util.create_item(user_dict, models.Customers, db)
    return user


@router.post(
    "/orders/{customer_id}/products/{product_id}",
    response_model=schemas.OrderOut,
    status_code=status.HTTP_201_CREATED,
    tags=["E-comms/Orders"],
)
def order_product(
    customer_id: int,
    product_id: int,
    quantity: int = Form(default=1, ge=1),
    db: Session = Depends(db_session),
):
    util.verify_item(
        item_id=customer_id, ModelClass=models.Customers, db=db, name="customer"
    )
    util.verify_item(
        item_id=product_id, ModelClass=models.Products, db=db, name="product"
    )
    product = util.verify_quantity(product_id=product_id, quantity=quantity, db=db)
    unit_price = product.unit_price
    total_price = unit_price * quantity
    order = schemas.Order(
        user_id=customer_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
    )
    order = util.create_item(
        item_dict=order.model_dump(), ModelClass=models.Orders, db=db
    )
    order_dict = util.order_out(order, product_id, db)

    return order_dict


@router.get(
    "/customers/{customer_id}/orders/{order_id}",
    response_model=schemas.OrderOut,
    tags=["E-comms/Orders"],
)
def get_customer_order(
    customer_id: int, order_id: int, db: Session = Depends(db_session)
):
    util.verify_item(
        item_id=customer_id, ModelClass=models.Customers, db=db, name="customer"
    )
    order = util.get_item_by_id(
        item_id=order_id, user_id=customer_id, QueryClass=models.Orders, db=db
    )
    order_dict = util.order_out(order, order.product_id, db)
    return order_dict


@router.get(
    "/customers/{customer_id}/orders",
    response_model=list[schemas.OrderOut],
    tags=["E-comms/Orders"],
)
def get_all_customer_orders(customer_id: int, db: Session = Depends(db_session)):
    util.verify_item(
        item_id=customer_id, ModelClass=models.Customers, db=db, name="customer"
    )
    orders = util.get_all_items(QueryClass=models.Orders, user_id=customer_id, db=db)
    orders_dict = [util.order_out(order, order.product_id, db) for order in orders]
    return orders_dict


@router.put(
    "/customers/{customer_id}/orders/{order_id}",
    response_model=schemas.OrderOut,
    status_code=status.HTTP_201_CREATED,
    tags=["E-comms/Orders"],
)
def update_order(
    customer_id: int,
    order_id: int,
    quantity: int = Form(default=1, ge=1),
    db: Session = Depends(db_session),
):
    util.verify_item(
        item_id=customer_id, ModelClass=models.Customers, db=db, name="customer"
    )
    util.verify_item(item_id=order_id, ModelClass=models.Orders, db=db, name="order")
    product = util.verify_quantity(
        order_id=order_id, quantity=quantity, db=db, create=False
    )
    unit_price = product.unit_price
    total_price = unit_price * quantity
    order = schemas.Order(
        user_id=customer_id,
        product_id=product.id,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
    )
    order = util.update_item(
        order_id, customer_id, order.model_dump(), models.Orders, db
    )
    order_dict = util.order_out(order, order.product_id, db)
    return order_dict


@router.delete(
    "/customers/{customer_id}/orders/{order_id}",
    tags=["E-comms/Orders"],
)
def delete_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(db_session),
):
    util.verify_item(
        item_id=customer_id, ModelClass=models.Customers, db=db, name="customer"
    )
    util.verify_item(item_id=order_id, ModelClass=models.Orders, db=db, name="order")
    util.verify_quantity(order_id=order_id, quantity=0, db=db, create=False)
    util.delete_item(order_id, customer_id, models.Orders, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
