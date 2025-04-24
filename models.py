# models.py
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    due_datetime = Column(DateTime, index=True)
    title = Column(String)
    required = Column(Boolean, default=True)

    status = relationship("TaskStatus", back_populates="task")

class TaskStatus(Base):
    __tablename__ = "task_status"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    is_done = Column(Boolean, default=False)
    proof = Column(String, nullable=True)
    unfinished_reason = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="status")
