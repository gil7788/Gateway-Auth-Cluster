from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import user_table
from .security import verify_password
import logging

logger = logging.getLogger("uvicorn")


def get_user(db: Session, username: str):
    logger.info("[CRUD] User request for user: %s", username)
    return db.query(user_table).filter(user_table.c.username == username).first()


def authenticate_user(db, username: str, password: str):
    logger.info("[CRUD] Token request for user: %s", username)
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user
