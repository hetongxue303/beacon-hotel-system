from pydantic import BaseModel
from datetime import datetime


class LoginDto(BaseModel):
    username: str = None
    real_name: str = None
    is_admin: bool = None
    gender: str = None

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
