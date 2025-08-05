from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    guest_id: str
    comment: str


class FeedbackOut(BaseModel):
    guest_id: str
    comment: str

    class Config:
        orm_mode = True
