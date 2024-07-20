from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class Roles(Enum):
    admin = "admin"
    user = "user"


class Blog(BaseModel):
    content: str
    description: str
    author: str
    comment: str


class BlogOut(Blog):
    id: int
    user_id: int
    date_created: datetime

    class Config:
        orm_mode = True


class Task(BaseModel):
    title: str
    content: str


class TaskUpdate(Task):
    completed_status: bool


class TaskOut(Task):
    id: int
    user_id: int
    completed_status: bool
    date_created: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: EmailStr
    role: Roles


class UserIn(User):
    password: str


class UserOut(User):
    message: str

    class Config:
        orm_mode = True


class UserOutList(User):
    id: int

    class Config:
        orm_mode = True


class Payload(BaseModel):
    user_id: int
    role: str


class Customer(BaseModel):
    name: str
    address: str
    contact: str


class CustomerOut(Customer):
    id: int

    class Config:
        orm_mode = True


class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float


class OrderOut(Order):
    id: int
    order_date: datetime
    product_info: dict

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    name: str
    category: str
    unit_price: float
    available_quantity: int
    available: bool

    class Config:
        orm_mode = True
