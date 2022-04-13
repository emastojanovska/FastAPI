from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models

app = FastAPI()

class Item(BaseModel): #serializer
    id:int
    name:str
    description:str
    price:int
    on_offer:bool
    owner_id: int

    class Config:
        orm_mode=True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

db=SessionLocal()

#Items 
@app.get('/items', response_model=List[Item], status_code=200)
def get_all_items():
    items=db.query(models.Item).all()
    return items

@app.get('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def get_an_iem(item_id:int):
    item=db.query(models.Item).filter(models.Item.id==item.id).first()
    return item

@app.post('items',response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    db_item=db.query(models.Item).filter(models.Item.name==item.name).first()
    if db_item is not None :
        raise HTTPException(status_code=400,detail="Item already exists")

    new_item=models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer,
        owner_id=item.owner_id
    )
    db.add(new_item)
    db.commit()

    return new_item

@app.delete('/item/{item_id}')
def delete_item(item_id:int):
    item_to_delete=db.query(models.Item).filter(models.Item.id==item_id).first()
    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource not found")
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete

@app.put('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_item(item_id:int,item:Item):
    item_to_update=db.query(models.Item).filter(models.Item.id==item.id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.description=item.description
    item_to_update.on_offer=item.on_offer

    db.commit()
    return item_to_update

    #Users
def get_user(user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
