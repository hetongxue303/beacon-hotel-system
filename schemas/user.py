from pydantic import BaseModel
from datetime import datetime

from schemas.menu import MenuDto


class LoginDto(BaseModel):
    username: str = None
    real_name: str = None
    is_admin: bool = None
    gender: str = None
    is_status: bool = None
    menus: list[MenuDto] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserDto(BaseModel):
    user_id: int = None
    username: str = None
    real_name: str = None
    gender: str = None
    is_admin: bool = None
    is_status: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserOutDto(UserDto):
    password: str = None
