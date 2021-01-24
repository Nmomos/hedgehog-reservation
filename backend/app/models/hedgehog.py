from enum import Enum
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class ColorType(str, Enum):
    solt_and_pepper = "SOLT & PEPPER"
    dark_grey = "DARK GREY"
    chocolate = "CHOCOLATE"


class HedgehogBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    name: Optional[str]
    description: Optional[str]
    age: Optional[float]
    color_type: Optional[ColorType]


class HedgehogCreate(HedgehogBase):
    name: str
    color_type: ColorType


class HedgehogUpdate(HedgehogBase):
    description: str
    age: float


class HedgehogInDB(IDModelMixin, HedgehogBase):
    name: str
    age: float
    color_type: ColorType


class HedgehogPublic(IDModelMixin, HedgehogBase):
    pass
