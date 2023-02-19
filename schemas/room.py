from datetime import datetime

from pydantic import BaseModel

from schemas.room_type import RoomTypeDto


class RoomDto(BaseModel):
    room_id: int = None
    room_name: str = None
    room_type_id: int = None
    type: RoomTypeDto = None
    room_price: float = None
    room_bed: int = None
    room_count: int = None
    is_status: bool = None
    is_state: str = None
    room_detail: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
