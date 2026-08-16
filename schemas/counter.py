# Libs
from datetime import datetime  # Datetime
import uuid  # UUID

# Application
from base.schema import BaseSchema  # Base
from enums.visibility import VisibilityType  # Visibility Enum
from enums.status import StatusType  # Status Enum


# Create Counter Schema
class CounterCreate(BaseSchema):
    title: str
    description: str

    started_at: datetime


# Update Counter Schema
class CounterUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None

    status: StatusType
    visibility: VisibilityType


# Read Counter Schema
class CounterRead(CounterCreate):
    id: uuid.UUID

    status: StatusType
    visibility: VisibilityType

    started_at: datetime
    ended_at: datetime | None

    created_at: datetime
    updated_at: datetime
