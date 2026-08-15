# Libs
from datetime import datetime  # Datetime
import uuid  # UUID

# Application
from base.schema import BaseSchema  # Base


# Profile Schema
class UserProfileSchema(BaseSchema):
    id: uuid.UUID
    username: str
    email: str
    display_name: str
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime
    updated_at: datetime


# Change Profile
class ChangeProfileSchema(BaseSchema):
    username: str | None = None
    display_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None


# Change Email
class ChangeEmailSchema(BaseSchema):
    email: str


# Change Password
class ChangePasswordSchema(BaseSchema):
    current_password: str
    new_password: str
    confirm_password: str
