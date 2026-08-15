# Libs
from sqlalchemy import Uuid  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship  # SQLAlchemy ORM
import uuid  # UUID

# Application
from base.model import BaseModel  # Base Model


# User
class User(BaseModel):
    __tablename__ = "users"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    display_name: Mapped[str] = mapped_column(
        nullable=False,
    )
    first_name: Mapped[str | None] = mapped_column(
        default="",
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        default="",
        nullable=True,
    )
    is_confirmed: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    # oauth_provider: Mapped[str | None] = mapped_column(
    #     nullable=True,
    # )
    # oauth_id: Mapped[str | None] = mapped_column(
    #     nullable=True,
    #     index=True,
    # )

    # Relationships
    counters: Mapped[list["Counter"]] = relationship(
        "Counter",
        back_populates="user",
    )
