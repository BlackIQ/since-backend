# Libs
from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI
from sqlalchemy.orm import Session  # SQLALchemy

# Application
from core.settings import settings  # Core: Settings
from dependencies.database import get_db  # Dependency: Database
from utils.password import hash_password, verify_password  # Utils: Password
from utils.token import (
    create_token,
    create_confirmation_token,
    verify_confirmation_token,
    create_reset_password_token,
    verify_reset_password_token,
)  # Utils: Token
from schemas.auth import (
    SigninSchema,
    SignupSchema,
    ResendConfirmationSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)  # Schema: Auth
from schemas.common import MessageSchema, TokenSchema  # Schema: Common
from models.user import User  # Model: User

# Router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup", response_model=MessageSchema)
async def signup(
    data: SignupSchema,
    db: Session = Depends(get_db),
):
    email_exists = db.query(User).where(User.email == data.email).first()
    if not email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    username_exists = db.query(User).where(User.username == data.username).first()
    if not username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        display_name=data.display_name,
        first_name=data.first_name,
        last_name=data.last_name,
        is_confirmed=False,
        is_active=True,
    )

    db.add(User)
    db.commit()

    token = create_confirmation_token(user.email)
    confirmation_url = f"{settings.frontend_url}/auth?token={token}"

    # TODO: Send Confirmation Email
    print(confirmation_url)

    return MessageSchema(
        message="Registration successful. Please check your email to confirm your account.",
    )


@router.post("/signin", response_model=TokenSchema)
async def signin(
    data: SigninSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).where(User.email == data.email).first()

    if user is None or user.password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is not confirmed. Please check your email.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive.",
        )

    access_token = create_token(user.id)

    # TODO: Send Security email

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/confirm-email", response_model=MessageSchema)
async def confirm_email(
    token: str,
    db: Session = Depends(get_db),
):
    email = verify_confirmation_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired confirmation token",
        )

    user = db.query(User).where(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_confirmed and user.is_active:
        return MessageSchema(
            message="Account is already confirmed. Please sign in.",
        )

    user.is_confirmed = True
    db.commit()

    # TODO: Send Welcome email

    return MessageSchema(
        message="Your email has been confirmed and account activated. Please sign in.",
    )


@router.post("/resend-confirmation", response_model=MessageSchema)
async def resend_confirmation(
    data: ResendConfirmationSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).where(User.email == data.email).first()

    generic_message = MessageSchema(
        message="If this email is registered and unconfirmed, a confirmation link has been sent.",
    )

    if not user:
        return generic_message

    if user.is_confirmed and user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account is already confirmed.",
        )

    token = create_confirmation_token(user.email)
    confirmation_url = f"{settings.frontend_url}/auth?token={token}"

    # TODO: Send Confirmation Email
    print(confirmation_url)

    return generic_message


@router.post("/forgot-password", response_model=MessageSchema)
async def forgot_password(
    data: ForgotPasswordSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).where(User.email == data.email).first()

    generic_message = MessageSchema(
        message="If this email is registered, password reset instructions have been sent.",
    )

    if not user:
        return generic_message

    token = create_reset_password_token(user.email)
    reset_url = f"{settings.frontend_url}/auth?reset_token={token}"

    # TODO: Send Reset Email
    print(reset_url)

    return generic_message


@router.post("/reset-password", response_model=MessageSchema)
async def reset_password(
    data: ResetPasswordSchema,
    db: Session = Depends(get_db),
):
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match.",
        )

    email = verify_reset_password_token(data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token.",
        )

    user = db.query(User).where(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.password_hash = hash_password(data.new_password)
    db.commit()

    # TODO: Send Change Password Email

    return MessageSchema(
        message="Password has been reset successfully. Please sign in with your new password.",
    )
