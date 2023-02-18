from datetime import datetime

from pydantic import BaseModel


class CustomerDto(BaseModel):
    customer_id: int = None
    customer_name: str = None
    customer_account: str = None
    is_status: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CustomerOutDto(CustomerDto):
    customer_password: str = None


class CustomerLoginDto(BaseModel):
    customer_account: str = None
    customer_password: str = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
