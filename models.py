from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Product(Base):
    __tablename__ = "products"
    pid = Column(Integer, primary_key=True, index=True)
    pname = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
