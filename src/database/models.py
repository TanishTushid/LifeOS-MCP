
from pydantic import BaseModel, Field
from typing import Literal


TaskPriority = Literal["low", "medium", "high"]
TaskStatus = Literal["pending", "completed"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    due_date: str = ""
    priority: TaskPriority = "medium"


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    due_date: str = ""
    priority: TaskPriority = "medium"


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: str
    priority: TaskPriority
    status: TaskStatus
    created_at: str
