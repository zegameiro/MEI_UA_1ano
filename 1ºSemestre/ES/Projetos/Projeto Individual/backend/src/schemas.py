from pydantic import BaseModel
from typing import List, Optional

# ----------------------- TASK SCHEMAS -----------------------

class TaskBase(BaseModel):
    title: str
    description: str
    priority: Optional[str] = None
    deadline: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskSchema(TaskBase):
    id: int
    is_completed: bool = False
    creation_date: str
    user_email: str

    class Config:
        from_attributes = True

