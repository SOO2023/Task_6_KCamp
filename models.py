from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Relationship, Mapped, mapped_column
from typing import List
from datetime import datetime


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    blogs: Mapped[List["Blogs"]] = Relationship(back_populates="user")
    tasks: Mapped[List["Tasks"]] = Relationship(back_populates="user")


class Blogs(Base):
    __tablename__ = "blogs"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)
    user: Mapped["Users"] = Relationship(back_populates="blogs")


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column()
    completed_status: Mapped[bool] = mapped_column(default=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)
    user: Mapped["Users"] = Relationship(back_populates="tasks")


class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(nullable=False)
    available_quantity: Mapped[int] = mapped_column(nullable=False)
    available: Mapped[bool] = mapped_column(default=True)


class Customers(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    contact: Mapped[str] = mapped_column(nullable=False)
    orders: Mapped[List["Orders"]] = Relationship(back_populates="customer")


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)
    order_date: Mapped[datetime] = mapped_column(default=datetime.now)
    customer: Mapped["Customers"] = Relationship(back_populates="orders")
