from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from enum import Enum

app = FastAPI(title="College Lost & Found API")


# Status options
class Status(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"


# Item database model
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: Status


# Request model
class ItemCreate(SQLModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: Status


# SQLite database
sqlite_url = "sqlite:///lost_found.db"
engine = create_engine(sqlite_url)


# Create database table when application starts
@app.on_event("startup")
def create_db():
    SQLModel.metadata.create_all(engine)


# Home
@app.get("/")
def home():
    return {"message": "Lost & Found API is running"}


# Create new item
@app.post("/items", status_code=201)
def create_item(item: ItemCreate):

    if not item.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title must not be empty"
        )

    if len(item.description.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Description must contain meaningful text"
        )

    with Session(engine) as session:
        db_item = Item(**item.model_dump())

        session.add(db_item)
        session.commit()
        session.refresh(db_item)

        return db_item


# Get all items
@app.get("/items")
def get_items():

    with Session(engine) as session:
        items = session.exec(select(Item)).all()

        return items


# Get items by status
@app.get("/items/status/{status}")
def get_items_by_status(status: Status):

    with Session(engine) as session:
        statement = select(Item).where(Item.status == status)
        items = session.exec(statement).all()

        return items


# Get items by category
@app.get("/items/category/{category}")
def get_items_by_category(category: str):

    with Session(engine) as session:
        statement = select(Item).where(Item.category == category)
        items = session.exec(statement).all()

        return items


# Get item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):

    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item


# Update item
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: ItemCreate):

    if not updated_item.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title must not be empty"
        )

    if len(updated_item.description.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Description must contain meaningful text"
        )

    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        item.title = updated_item.title
        item.description = updated_item.description
        item.category = updated_item.category
        item.location = updated_item.location
        item.reported_by = updated_item.reported_by
        item.status = updated_item.status

        session.add(item)
        session.commit()
        session.refresh(item)

        return item


# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):

    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        session.delete(item)
        session.commit()

        return {
            "message": "Item deleted successfully"
        }