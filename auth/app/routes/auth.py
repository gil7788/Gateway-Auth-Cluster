from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_db, get_current_active_user
from ..crud import authenticate_user
from ..schemas import User, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..security import create_access_token

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Auth Service is active"}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
