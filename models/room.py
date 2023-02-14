from sqlalchemy import Column, BigInteger, String, Enum, DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models import Base


class Room(Base):
    """ 客房表 """
    __table_args__ = ({"comment": "客房表"})

    room_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='客房ID')

    room_name = Column(String(200), nullable=False, comment='客房名称')

    room_type_id = Column(BigInteger, ForeignKey('room_type.room_type_id'), nullable=False, comment='客房类型')
    type = relationship('Room_Type', backref='room_type')

    room_price = Column(DECIMAL(6, 2), nullable=False, comment='客房价格')

    room_bed = Column(Integer, nullable=False, comment='客房床位')

    room_count = Column(Integer, nullable=False, comment='客房人数')

    is_status = Column(Enum('0', '1'), server_default='0', comment='客房状态')

    room_detail = Column(String(1000), server_default='无', comment='客房详情')
