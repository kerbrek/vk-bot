# pylint: disable=too-few-public-methods
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from .database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    category_id = Column(ForeignKey('category.id'), nullable=False)

    __mapper_args__ = {"eager_defaults": True}
