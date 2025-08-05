from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(String, index=True)
    comment = Column(Text)
