from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskOut
from app.dependencies import get_db, get_current_user
from app.services.task_service import create_task, update_task_status, delete_task

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post('/', response_model=TaskOut)
def add_task(
    task: TaskCreate,
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[Session, Depends(get_current_user)],
):
    return create_task(session, user, task)


@router.patch('/{task_id}', response_model=TaskOut)
def update_status(
    task_id: int,
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[Session, Depends(get_current_user)]
):    
    return update_task_status(session, user, task_id)


@router.delete('/{task_id}')
def delete_task_endpoint(
    task_id: int,
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[Session, Depends(get_current_user)]
):    
    delete_task(session, user, task_id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
