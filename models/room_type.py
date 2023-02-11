from models.base import Base
from sqlalchemy import Column, BigInteger, String


class RoomType(Base):
    """ 房间类型表 """
    __table_args__ = ({"comment": "房间类型表"})

    room_type_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='类型ID')

    room_type_name = Column(String(200), nullable=False, comment='房间类型')

    description = Column(String(500), server_default='', comment='备注')
