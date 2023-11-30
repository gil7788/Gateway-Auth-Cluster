from fastapi import Depends, HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from starlette import status

from .config import DATABASE_URL, SECRET_KEY, ALGORITHM
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .security import oauth2_scheme
from .schemas import User
from .crud import get_user

logger = logging.getLogger("uvicorn")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    logger.info("[DEPENDENCIES] Creating database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    logger.info("[DEPENDENCIES] Token request for user: %s", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(db, username)
        if user is None:
            raise credentials_exception
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[DEPENDENCIES] Token has expired")
    except JWTError:
        raise credentials_exception


# Define the function to get the current active user
def get_current_active_user(current_user: User = Depends(get_current_user)):
    logger.info("[DEPENDENCIES] User request for user: %s", current_user.username)
    return current_user