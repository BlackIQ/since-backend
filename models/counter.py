# Libs
from sqlalchemy import Uuid, Enum, ForeignKey  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship  # SQLAlchemy ORM
import uuid  # UUID

# Application
from base.model import BaseModel  # Base Model
from enums.visibility import VisibilityType  # Enum visibility
from enums.status import StatusType  # Enum status


# Counter
class Counter(BaseModel):
    __tablename__ = "counters"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        nullable=False,
    )
    visibility: Mapped[VisibilityType] = mapped_column(
        Enum(VisibilityType),
        default=VisibilityType.PRIVATE,
        nullable=False,
    )
    status: Mapped[StatusType] = mapped_column(
        Enum(StatusType),
        default=StatusType.ACTIVE,
        nullable=False,
    )

    # Foreign Keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="counters",
    )
    periods: Mapped[list["Period"]] = relationship(
        "Period",
        back_populates="counter",
    )
