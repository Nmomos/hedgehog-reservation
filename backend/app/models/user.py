import string
from typing import Optional

from app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin
from pydantic import EmailStr, constr


def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "ユーザー名に無効な文字が含まれています。"
    assert len(username) >= 3, "ユーザー名は3文字以上で入力してください。"
    return username


class UserBase(CoreModel):
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: constr(min_length=3, regex="[a-zA-Z0-9_-]+$")  # noqa


class UserUpdate(CoreModel):
    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="[a-zA-Z0-9_-]+$")]  # noqa


class UserPasswordUpdate(CoreModel):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    pass
