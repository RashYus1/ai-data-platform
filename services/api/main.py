from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database.connection import SessionLocal
from database.models import DataItem

from services.api.schemas import DataItemCreate


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "AI Data Pipeline & Annotation Platform API is running"
    }


@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    from sqlalchemy import text

    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }


@app.post("/data-items")
def create_data_item(
    item: DataItemCreate,
    db: Session = Depends(get_db),
):
    data_item = DataItem(
        title=item.title,
        content=item.content,
    )

    db.add(data_item)
    db.commit()
    db.refresh(data_item)

    return {
        "id": data_item.id,
        "title": data_item.title,
        "content": data_item.content,
        "status": data_item.status,
    }


@app.get("/data-items")
def get_data_items(db: Session = Depends(get_db)):
    data_items = db.query(DataItem).all()

    return [
        {
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "status": item.status,
        }
        for item in data_items
    ]