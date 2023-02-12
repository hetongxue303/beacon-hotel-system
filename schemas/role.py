from datetime import datetime

from pydantic import BaseModel


class RoleDto(BaseModel):
    role_id: int = None
    role_name: str = None
    is_status: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
