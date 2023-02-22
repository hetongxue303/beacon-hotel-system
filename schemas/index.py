import typing

from pydantic import BaseModel

from schemas.room import RoomDto


class IndexDto(BaseModel):
    rooms: list[RoomDto | typing.Any] = None
    free_time: int = None
    booking: int = None
    stay: int = None
    maintenance: int = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
