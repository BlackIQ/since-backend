# Libs
from datetime import datetime  # Datetime
import uuid  # UUID

# Application
from base.schema import BaseSchema  # Base
from enums.visibility import VisibilityType  # Visibility Enum
from enums.status import StatusType  # Status Enum
from schemas.period import PeriodRead  # Schema Period


# Create Counter Schema
class CounterCreate(BaseSchema):
    title: str
    description: str

    started_at: datetime


# Update Counter Schema
class CounterUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None

    status: StatusType | None = None
    visibility: VisibilityType | None = None


# Read Counter Schema
class CounterRead(BaseSchema):
    id: uuid.UUID

    title: str
    description: str

    status: StatusType
    visibility: VisibilityType

    periods: list[PeriodRead]

    created_at: datetime
    updated_at: datetime


# Public Counter Schema
class PublicCounterRead(BaseSchema):
    id: uuid.UUID

    title: str
    description: str

    started_at: datetime
    ended_at: datetime | None

    status: StatusType
