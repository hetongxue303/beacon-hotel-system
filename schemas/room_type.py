from datetime import datetime

from pydantic import BaseModel


class RoomTypeDto(BaseModel):
    room_type_id: int = None
    room_type_name: str = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
