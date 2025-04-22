# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TaskBase(BaseModel):
    title: str
    date: date
    required: bool = True

class TaskCreate(TaskBase):
    pass

class TaskShow(TaskBase):
    id: int
    expired: bool
    completed: bool
    proof: Optional[str] = None
    unfinished_reason: Optional[str] = None
    
    class Config:
        orm_mode = True

class TaskComplete(BaseModel):
    task_id: int
    proof: Optional[str] = None

class UnfinishedReason(BaseModel):
    task_id: int
    reason: str