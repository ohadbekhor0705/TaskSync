from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import *
from routes.users import user_router
from routes.todos import todo_router
import uvicorn

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="TaskSync API", description="API for managing users and todos", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,        
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(todo_router, prefix="/todos", tags=["todos"])

@app.get("/")
async def root():
    return {"message": "Welcome to the TaskSync API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)