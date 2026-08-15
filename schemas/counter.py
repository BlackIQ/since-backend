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
    visibility: VisibilityType
    status: StatusType


# Update Counter Schema
class CounterUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    visibility: VisibilityType
    status: StatusType


# Read Counter Schema
class CounterRead(CounterCreate):
    id: uuid.UUID

    created_at: datetime
    updated_at: datetime
