from fastapi import FastAPI, HTTPException, status, Depends
from app.database import *
from app.routes.users import user_router
from app.routes.todos import todo_router

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="TaskSync API", description="API for managing users and todos", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(todo_router, prefix="/todos", tags=["todos"])
