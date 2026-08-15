# Libs
from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI
from sqlalchemy.orm import Session  # SQLALchemy
from datetime import datetime, timezone  # Datetime
import uuid  # UUID

# Application
from dependencies.database import get_db  # Dependency: Database
from dependencies.token import get_current_user  # Dependency: Token
from schemas.counter import CounterCreate, CounterUpdate, CounterRead  # Schema: Counter
from models.user import User  # Model: User
from models.counter import Counter  # Model: Counter

# Router
router = APIRouter(
    prefix="/counters",
    tags=["Counter"],
)


@router.get("", response_model=list[CounterRead])
async def list_counters(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.get("/{counter_id}", response_model=CounterRead)
async def get_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.post("", response_model=CounterRead)
async def create_counter(
    counter_data: CounterCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.patch("/{counter_id}", response_model=CounterRead)
async def update_counter(
    counter_id: uuid.UUID,
    counter_data: CounterUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.delete("/{counter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return None
