import os

from fastapi import Depends, HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from starlette import status

from . import utils
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .security import oauth2_scheme
from .schemas import User
from .crud import get_user
from dotenv import load_dotenv


def load_configuration():
    app_env = os.getenv('APP_ENV', 'development')
    if app_env == 'development':
        # Load .env file in development
        load_dotenv()

    required_env_vars = \
        ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE", "SECRET_KEY", "ALGORITHM"]
    for var in required_env_vars:
        if not os.getenv(var):
            logger.error(f"[Dependencies] Missing required environment variable: {var}")
            raise EnvironmentError(f"[Dependencies] Missing required environment variable: {var}")


load_configuration()


logger = logging.getLogger("uvicorn")

database_url = utils.get_database_url(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PASSWORD"),
                                      os.getenv("MYSQL_HOST"), os.getenv("MYSQL_PORT"),
                                      os.getenv("MYSQL_DATABASE"))

engine = create_engine(database_url)
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
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
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
