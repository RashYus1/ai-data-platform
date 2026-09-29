from pydantic import BaseModel


class DataItemCreate(BaseModel):
    title: str
    content: str


class DataItemStatusUpdate(BaseModel):
    status: str