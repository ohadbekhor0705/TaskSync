from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Sequence
from database import LoginResponse, Todo
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
