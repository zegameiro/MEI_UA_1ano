from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..schemas import TaskCreate, TaskSchema
from ..utils import authenticated, validate_credential
from ..repositories.task_repository import (
    create_task,
    get_tasks_from_user,
    update_task, 
    delete_task
)

router = APIRouter()

@router.post(
    '', 
    description="Add a new task and associate it with a user. Its required to send the access token in the headers.",
    name="Add a new Task"
)
@authenticated()
def add_new_task(request: Request, task: TaskCreate, db_session: Session = Depends(get_db)):

    # Get the access token from the cookie in the request
    credential = request.headers.get('Credential')

    # Validate the access token
    idinfo = validate_credential(credential)

    # Create a new task associated with the user
    create_task(task=task, user_email=idinfo.get("email"), db_session=db_session)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Task created successfully",
        }
    )

@router.get(
    '',
    description="Get tasks associated with a user. Its required to be authenticated. It also includes sort and filter parameters",
    name="Get tasks from user"
)
@authenticated()
def get_tasks(request: Request, filter_by: Optional[str] = None, sort_by: Optional[str] = None, sort_order: Optional[str] = None, db_session: Session = Depends(get_db)):

    # Get the access token from the cookie in the request
    credential = request.headers.get('Credential')

    # Validate the access token
    idinfo = validate_credential(credential)

    # Get tasks associated with the user
    tasks = get_tasks_from_user(
        user_email=idinfo.get("email"), 
        filter_by=filter_by, 
        sort_by=sort_by, 
        sort_order=sort_order, 
        db_session=db_session
    )

    return tasks

@router.put(
    "",
    description="Update a specific task that a user created. Its required to be authenticated",
    name="Update a Task"
)
@authenticated()
def update_created_task(request: Request, task: TaskSchema, db_session: Session = Depends(get_db)):

    # Get the access token from the cookie in the request
    credential = request.headers.get('Credential')

    # Validate the access token
    idinfo = validate_credential(credential)

    # Update the task
    update_task(task=task, task_id=task.id, db_session=db_session)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Task updated successfully",
        }
    )

@router.delete(
    "",
    description="Delete a task that a user previously created, its required to send the jwtToken in the headers",
    name="Delete a Task"
)
@authenticated()
def delete_created_task(request: Request, task_id: int, db_session: Session = Depends(get_db)):

    # Get the access token from the cookie in the request
    credential = request.headers.get('Credential')

    # Validate the access token
    idinfo = validate_credential(credential)

    # Delete the task
    if delete_task(task_id=task_id, db_session=db_session):
        return JSONResponse(
            status_code=200,
            content={
                "message": "Task deleted successfully",
            }
        )
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Task not found"
            }
        )