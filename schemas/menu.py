from pydantic import BaseModel
from datetime import datetime


class MenuDto(BaseModel):
    menu_id: int = None
    parent_id: int = None
    menu_title: str = None
    menu_type: str = None
    router_name: str = None
    router_path: str = None
    component: str = None
    sort: int = None
    icon: str = None
    permission: str = None
    sub_count: int = None
    is_show: bool = None
    is_sub: bool = None
    is_status: bool = None
    is_delete: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MenuTreeDto(MenuDto):
    children: list[MenuDto] = []
