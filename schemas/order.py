from datetime import datetime

from pydantic import BaseModel

from schemas.customer import CustomerDto
from schemas.room import RoomDto


class OrderDto(BaseModel):
    order_id: int = None
    order_num: str = None
    customer_id: int = None
    customer: CustomerDto = None
    room_id: int = None
    room: RoomDto = None
    is_status: str = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
