# Libs
from sqlalchemy import Uuid, DateTime, ForeignKey  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship  # SQLAlchemy ORM
from datetime import datetime  # Datetime
import uuid  # UUID

# Application
from base.model import BaseModel  # Base Model


# Period
class Period(BaseModel):
    __tablename__ = "periods"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Foreign Keys
    counter_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("counters.id"),
        index=True,
        nullable=False,
    )

    # Relationships
    counter: Mapped["Counter"] = relationship(
        "Counter",
        back_populates="periods",
    )
