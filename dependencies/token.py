# Libs
from fastapi import Depends, HTTPException, status  # FastAPI
from fastapi.security import OAuth2PasswordBearer  # FastAPI Security
from sqlalchemy.orm import Session  # SQLAlchemy ORM
import uuid  # UUID
import jwt  # JWT
from jwt.exceptions import PyJWTError  # JWT Error

# Application
from core.settings import settings  # Core: Settings
from dependencies.database import get_db  # Depenency: Database
from models.user import User  # Model: User

# Secret and Algorithm
SECRET = settings.secret
ALGORITHM = settings.algorithm

# OAuth Schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

# 401 Execption
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


# Get Current User
def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except PyJWTError:
        raise credentials_exception

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception

    try:
        parsed_user_id = uuid.UUID(str(user_id))
    except ValueError:
        raise credentials_exception

    user = db.query(User).filter(User.id == parsed_user_id).one_or_none()

    if user is None:
        raise credentials_exception

    return user
