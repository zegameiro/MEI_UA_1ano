from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
import time

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String(150))
    is_completed = Column(Boolean, default = False)
    creation_date = Column(String(350))
    deadline = Column(String(350), default=None)
    priority = Column(String(10), default=None)
    user_email = Column(String(100))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_creation_date()
        
    def set_creation_date(self):
        self.creation_date = str(time.time())
