from datetime import datetime

from pydantic import BaseModel


class CustomerDto(BaseModel):
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
