from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Sequence
from database import Todo
from dependencies import *
from security import *
from database import *

todo_router = APIRouter(
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

# dummy endpoint to get all todos for a user
@todo_router.get("/", response_model=List[TodoRead])
async def get_todos(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> List[TodoRead]:
    print(f"Token received: {token}")
    current_user = get_current_user(token, session)
    todos: Sequence[Todo] = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    return todos # type: ignore

@todo_router.post("/create", response_model=TodoCreateResponse)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
    ) -> TodoCreateResponse:
    new_todo  = Todo(title=todo.title, status=todo.status,user_id=current_user.id)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return TodoCreateResponse(message="Todo Created!")