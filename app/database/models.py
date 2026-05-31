from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database.connection import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    issue = Column(Text, nullable=False)
    plan = Column(Text, default="")
    code = Column(Text, default="")
    review = Column(Text, default="")
    status = Column(String(20), default="pending")
    branch = Column(String(100), default="")
    pr_url = Column(String(200), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
