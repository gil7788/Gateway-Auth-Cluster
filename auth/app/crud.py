from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import user_table
from .security import verify_password


def get_user(db: Session, username: str):
    return db.query(user_table).filter(user_table.c.username == username).first()


# Add other CRUD operations here
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user
