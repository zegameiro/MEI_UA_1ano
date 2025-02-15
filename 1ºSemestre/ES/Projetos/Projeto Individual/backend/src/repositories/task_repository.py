from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import Task
from ..schemas import TaskCreate, TaskSchema

def create_task(task: TaskCreate, user_email: str, db_session: Session) -> Task:
    
    new_task = Task(
        title=task.title,
        description=task.description,
        user_email=user_email,
        priority=task.priority,
        deadline=task.deadline
    )

    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)

    return new_task

def update_task(task: TaskSchema, task_id: int, db_session: Session) -> Task:

    # Retrieve the task that needs to be updated
    task_to_update = db_session.query(Task).filter(Task.id == task_id).first()

    if task_to_update is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task's attributes
    task_to_update.title = task.title
    task_to_update.description = task.description
    task_to_update.is_completed = task.is_completed
    task_to_update.priority = task.priority
    task_to_update.deadline = task.deadline

    db_session.commit()
    db_session.refresh(task_to_update)
    

def get_tasks_from_user(user_email: str, sort_by: str, sort_order: str, filter_by: str, db_session: Session) -> list[Task]:

    found_tasks = db_session.query(Task).filter(Task.user_email == user_email).all()
    priority_order = {"low": 1, "medium": 2, "high": 3}

    match sort_by:

        case "creation":

            if sort_order == "asc":
                found_tasks.sort(key = lambda x: x.creation_date)

            else: 
                found_tasks.sort(key = lambda x: x.creation_date, reverse = True)

        case "deadline":

            if sort_order == "asc":
                found_tasks.sort(key = lambda x: x.deadline)

            else:
                found_tasks.sort(key = lambda x: x.deadline, reverse = True)

        case "priority":

            if sort_order == "asc":
                found_tasks.sort(key = lambda x: priority_order[x.priority])

            else:
                found_tasks.sort(key = lambda x: priority_order[x.priority], reverse = True)

        case "completed":

            if sort_order == "asc":
                found_tasks.sort(key = lambda x: x.is_completed, reverse = True)

            else:
                found_tasks.sort(key = lambda x: x.is_completed)

        case "title": 

            if sort_order == "asc":
                found_tasks.sort(key = lambda x: x.title)

            else:
                found_tasks.sort(key = lambda x: x.title, reverse = True)

        case _:
            found_tasks.sort(key=lambda x: x.id)

    match filter_by:

        case "completed":
            found_tasks = list(filter(lambda x: x.is_completed, found_tasks))

        case "not_completed":
            found_tasks = list(filter(lambda x: not x.is_completed, found_tasks))

        case "high_prio":
            found_tasks = list(filter(lambda x: x.priority == "high", found_tasks))

        case "medium_prio":
            found_tasks = list(filter(lambda x: x.priority == "medium", found_tasks))

        case "low_prio":
            found_tasks = list(filter(lambda x: x.priority == "low", found_tasks))

        case _:
            pass

    return found_tasks


def delete_task(task_id: int, db_session: Session) -> bool:
    task_to_delete = db_session.query(Task).filter(Task.id == task_id).first()

    if task_to_delete is None:
        return False

    db_session.delete(task_to_delete)
    db_session.commit()

    return True