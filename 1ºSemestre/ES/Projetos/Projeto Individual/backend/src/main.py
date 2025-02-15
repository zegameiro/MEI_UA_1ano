
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Base
from .database import engine
from .endpoints import task_endpoint

Base.metadata.create_all(bind=engine)

description = """
<strong>
The TaskFlow API is a simple and lightweight task management system.
It allows users to:
  - Create a new task
  - Get all the tasks associated to a user with filtering and sorting options
  - Update a specific task that a user created
  - Delete a task that a user previously created
</strong>
"""

app = FastAPI(
    title = "Task Flow API",
    version = "1.0.0",
    description = description,
    license_info = {"name": "MIT License", "url": "https://opensource.org/licenses/MIT"}
)

origins = ["http://localhost:3000", "https://es-ua.ddns.net"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(task_endpoint.router, tags=["Tasks"], prefix="/task")

@app.get("/")
def root():
    return {"message": "I want something good to die for. To make it beautiful to live"}


    
