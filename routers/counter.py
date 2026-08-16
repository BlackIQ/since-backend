# Libs
from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI
from sqlalchemy.orm import Session  # SQLALchemy
from datetime import datetime, timezone  # Datetime
import uuid  # UUID

# Application
from dependencies.database import get_db  # Dependency: Database
from dependencies.token import get_current_user  # Dependency: Token
from enums.status import StatusType  # Enum: Status
from enums.visibility import VisibilityType  # Enum: Visibility
from schemas.counter import (
    CounterCreate,
    CounterUpdate,
    CounterRead,
    PublicCounterRead,
)  # Schema: Counter
from models.user import User  # Model: User
from models.counter import Counter  # Model: Counter
from models.period import Period  # Model: Period

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
    db_counters = (
        db.query(Counter)
        .where(
            Counter.user_id == user.id,
            Counter.deleted_at == None,
        )
        .all()
    )

    return db_counters


@router.get("/{counter_id}", response_model=CounterRead)
async def get_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_counter = (
        db.query(Counter)
        .where(
            Counter.id == counter_id,
            Counter.user_id == user.id,
            Counter.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found",
        )

    return db_counter


@router.post("", response_model=CounterRead)
async def create_counter(
    counter_data: CounterCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_counter = Counter(
        title=counter_data.title,
        description=counter_data.description,
        user_id=user.id,
        status=StatusType.ACTIVE,
        visibility=VisibilityType.PRIVATE,
    )

    db.add(db_counter)
    db.flush()

    db_period = Period(
        counter_id=db_counter.id,
        started_at=counter_data.started_at,
    )

    db.add(db_period)
    db.commit()

    db.refresh(db_counter)
    db.refresh(db_period)

    return db_counter


@router.patch("/{counter_id}", response_model=CounterRead)
async def update_counter(
    counter_id: uuid.UUID,
    counter_data: CounterUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_counter = (
        db.query(Counter)
        .where(
            Counter.id == counter_id,
            Counter.user_id == user.id,
            Counter.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found",
        )

    for key, value in counter_data.model_dump(exclude_unset=True).items():
        setattr(db_counter, key, value)

    db.commit()
    db.refresh(db_counter)

    return db_counter


@router.delete("/{counter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_counter = (
        db.query(Counter)
        .where(
            Counter.id == counter_id,
            Counter.user_id == user.id,
            Counter.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found",
        )

    db_counter.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_counter)

    return None


@router.post("/{counter_id}/restart", response_model=CounterRead)
async def restart_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_counter = (
        db.query(Counter)
        .where(
            Counter.id == counter_id,
            Counter.user_id == user.id,
            Counter.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found",
        )

    db_period = (
        db.query(Period)
        .where(
            Period.counter_id == counter_id,
            Period.ended_at == None,
            Period.deleted_at == None,
        )
        .one_or_none()
    )

    if db_period:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Counter is already active",
        )

    db_period = Period(
        counter_id=db_counter.id,
        started_at=datetime.now(timezone.utc),
    )

    db_counter.status = StatusType.ACTIVE

    db.add(db_period)
    db.commit()
    db.refresh(db_counter)

    return db_counter


@router.post("/{counter_id}/complete", response_model=CounterRead)
async def complete_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_counter = (
        db.query(Counter)
        .where(
            Counter.id == counter_id,
            Counter.user_id == user.id,
            Counter.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found",
        )

    db_period = (
        db.query(Period)
        .where(
            Period.counter_id == counter_id,
            Period.ended_at == None,
            Period.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_period:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Counter has no active period",
        )

    db_period.ended_at = datetime.now(timezone.utc)
    db_counter.status = StatusType.COMPLETED

    db.commit()
    db.refresh(db_counter)

    return db_counter


@router.get("/{counter_id}/public", response_model=PublicCounterRead)
async def public_counter(
    counter_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    db_counter = (
        db.query(Counter)
        .where(
            Counter.id == counter_id,
            Counter.visibility == VisibilityType.PUBLIC,
            Counter.deleted_at == None,
        )
        .one_or_none()
    )

    if not db_counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found",
        )

    db_period = (
        db.query(Period)
        .where(
            Period.counter_id == db_counter.id,
            Period.deleted_at == None,
        )
        .order_by(Period.started_at.desc())
        .first()
    )

    return PublicCounterRead(
        id=db_counter.id,
        title=db_counter.title,
        description=db_counter.description,
        started_at=db_period.started_at,
        ended_at=db_period.ended_at,
        status=db_counter.status,
    )
