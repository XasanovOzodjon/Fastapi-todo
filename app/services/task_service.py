from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Task
from app.schemas.task import TaskCreate
from app.db.models import User


def create_task(session: Session, user: User, task_data: TaskCreate) -> Task:
    existing_task = session.query(Task).filter(Task.user_id==user.id, Task.name==task_data.name).first()
    if existing_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already exists.")
    
    task = Task(
        name=task_data.name, 
        description=task_data.description, 
        user_id=user.id,
        category=task_data.category,
        priority=task_data.priority
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

def update_task_status(session: Session, user: User, task_id: int) -> Task:
    task = session.query(Task).filter(Task.id==task_id, Task.user_id==user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task not found.")
    
    task.status = not task.status
    session.add(task)
    session.commit()

    return task

def delete_task(session: Session, user: User, task_id: int):
    task = session.query(Task).filter(Task.id==task_id, Task.user_id==user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task not found.")
    
    session.delete(task)
    session.commit()
