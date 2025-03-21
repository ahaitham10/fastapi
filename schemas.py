from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    pname: str
    description: str
    price: float
    stock: int

class ProductResponse(ProductCreate):
    pid: int

    class Config:
        from_attributes = True
