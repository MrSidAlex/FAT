from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

class StatusEnum(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    deadline: datetime
    status: StatusEnum

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[StatusEnum] = None

class Task(TaskBase):
    id: int
    created_at: datetime