from enum import Enum
from typing import Optional, Union

from app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin
from app.models.user import UserPublic


class ColorType(str, Enum):
    solt_and_pepper = "SOLT & PEPPER"
    dark_grey = "DARK GREY"
    chocolate = "CHOCOLATE"


class HedgehogBase(CoreModel):
    name: Optional[str]
    description: Optional[str]
    age: Optional[float]
    color_type: Optional[ColorType]


class HedgehogCreate(HedgehogBase):
    name: str
    color_type: ColorType


class HedgehogUpdate(HedgehogBase):
    color_type: Optional[ColorType]


class HedgehogInDB(IDModelMixin, DateTimeModelMixin, HedgehogBase):
    name: str
    age: float
    color_type: ColorType
    owner: int


class HedgehogPublic(IDModelMixin, DateTimeModelMixin, HedgehogBase):
    owner: Union[int, UserPublic]
