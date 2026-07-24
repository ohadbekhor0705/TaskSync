# app/database.py
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session
from enum import Enum
engine = create_engine("sqlite:///./database.db")

def get_session():
    with Session(engine) as session:
        yield session

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)

class UserCreate(UserBase):
    password: str

class UserLogin(SQLModel):
    username: str
    password: str

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str

    todos: list["Todo"] = Relationship(back_populates="user")

class UserRead(UserBase):
    id: int

class LoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: UserRead
    message: str

class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"

class TodoBase(SQLModel):
    title: str
    status: TodoStatus = Field(default=TodoStatus.PENDING)

class Todo(TodoBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="todos")

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    status: TodoStatus = TodoStatus.PENDING
class TodoCreateResponse(SQLModel):
    message: str

class TodoUpdate(SQLModel):
    status: TodoStatus
    id: int