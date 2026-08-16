# Libs
from datetime import datetime  # Datetime
import uuid  # UUID

# Application
from base.schema import BaseSchema  # Base


# Read Period Schema
class PeriodRead(BaseSchema):
    id: uuid.UUID

    started_at: datetime
    ended_at: datetime | None

    created_at: datetime
    updated_at: datetime
