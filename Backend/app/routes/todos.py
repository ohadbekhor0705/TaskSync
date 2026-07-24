from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from typing import List, Sequence

from database import Todo, User
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

@todo_router.delete("/delete/{todo_id}")
async def delete_todo(
    todo_id: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
    ) -> Response:
    current_user: User = get_current_user(token, session)
    query = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)

    todo_to_delete: Todo | None = session.exec(query).first()
    if not todo_to_delete:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    session.delete(todo_to_delete)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@todo_router.put("/update")
async def update_todo(
    updated_todo: TodoUpdate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
    ):
    current_user = get_current_user(token, session)
    query = select(Todo).where(Todo.id == updated_todo.id, Todo.user_id == current_user.id)

    current_todo = session.exec(query).first()
    if not current_todo:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    current_todo.status = updated_todo.status
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)