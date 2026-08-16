# Libs
from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI
from sqlalchemy.orm import Session  # SQLALchemy

# Application
from dependencies.database import get_db  # Dependency: Database
from dependencies.token import get_current_user  # Dependency: Token
from utils.password import hash_password, verify_password  # Utils: Password
from schemas.user import (
    UserProfileSchema,
    ChangeProfileSchema,
    ChangeEmailSchema,
    ChangePasswordSchema,
)  # Schema: User
from models.user import User  # Model: User

# Router
router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("/me", response_model=UserProfileSchema)
async def me(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_user = (
        db.query(User)
        .where(
            User.id == user.id,
        )
        .one_or_none()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return db_user


@router.patch("/change/profile", response_model=UserProfileSchema)
async def change_profile(
    data: ChangeProfileSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_user = (
        db.query(User)
        .where(
            User.id == user.id,
        )
        .one_or_none()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


@router.patch("/change/email", response_model=UserProfileSchema)
async def change_email(
    data: ChangeEmailSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_user = (
        db.query(User)
        .where(
            User.id == user.id,
        )
        .one_or_none()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    email_exists = db.query(User).where(User.email == data.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    user.email = data.email

    db.commit()
    db.refresh(db_user)

    return user


@router.patch("/change/password", response_model=UserProfileSchema)
async def change_password(
    data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_user = (
        db.query(User)
        .where(
            User.id == user.id,
        )
        .one_or_none()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not verify_password(user.password_hash, hash_password(data.current_password)):
        raise HTTPException(
            status_code=409,
            detail="Current password is not same",
        )

    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=409,
            detail="New password is not same as confirm",
        )

    user.password_hash = hash_password(data.new_password)

    db.commit()
    db.refresh(db_user)

    return user
