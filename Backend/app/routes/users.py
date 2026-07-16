from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from database import LoginResponse
from security import *
from database import *

#from dependencies import get_current_user # Our new dependency

# users touter
user_router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# this endpoint is for user registration
@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, session: Session = Depends(get_session)) -> dict[str, str]:
    # checking if the user is already existing
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User registered successfully"}

# this endpoint is for user login
@user_router.post("/login", response_model=LoginResponse)
async def login_user(user: UserLogin, session: Session = Depends(get_session)) -> LoginResponse:
    print(f"Attempting to log in user: {user.username} with email: {user.password}")  # Debugging line
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.email}) # creating the access token with the user's email as the subject
    login_response = LoginResponse(access_token=access_token, token_type="bearer", user=UserRead(id=db_user.id, username=db_user.username, email=db_user.email))
    return login_response # returning the login response with the access token and user details