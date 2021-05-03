import datetime
from typing import Optional, Union, NoReturn, Any, Dict

from email_validator import validate_email
from pydantic import BaseModel, Field, validator

from services.db.models import SizeEnum


class User(BaseModel):
    first_name: str = Field(..., example="Gleb", title="Имя")
    last_name: str = Field(..., example="Garanin", title="Фамилия")
    phone_number: Optional[str] = Field(
        default=None,
        regex=r"^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$",
        min_length=10, max_length=15, title="Номер мобильного телефона",
        example="+7900232132"
    )
    email: Optional[str] = Field(default=None, title="Адрес электронной почты",
                                 example="glebgar567@gmail.com")
    balance: float
    id: Optional[int] = None

    @validator("email")
    def validate_em(cls, v: ...) -> Union[str, NoReturn]:
        if not validate_email(v):
            raise ValueError("bad email format")
        return v

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    unit_price: float
    size: SizeEnum
    description: str
    created_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Apple MacBook 15",
            "unit_price": 7000,
            "description": "Light and fast laptop",
        }
        keep_untouched = ()

    def dict(self, **kwargs) -> Dict[Any, Any]:
        dct = super().dict(**kwargs)
        dct.update(
            {"size": dct.get("size").name}
        )
        return dct


class DefaultResponse(BaseModel):
    error: str
    success: bool = False


class ObjectCount(BaseModel):
    count: int = Field(..., example=44)


class SimpleResponse(BaseModel):
    message: str = Field(...)


class TestResponse(BaseModel):
    success: bool = True
    user_agent: Optional[str] = Field(..., alias="User-Agent")
    value: int
