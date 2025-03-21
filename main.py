from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db
from auth import get_current_user, create_access_token, verify_password, hash_password
from models import User, Product
from schemas import UserCreate, UserResponse, ProductCreate, ProductResponse
from datetime import timedelta

app = FastAPI()

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(name=user.name, username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=10))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Product).all()
