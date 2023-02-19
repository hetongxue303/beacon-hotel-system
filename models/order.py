from sqlalchemy import Column, BigInteger, String, ForeignKey, Enum, DateTime, func, Integer
from sqlalchemy.orm import relationship

from models import Base


class Order(Base):
    """ 菜单表 """
    __table_args__ = ({"comment": "订单表"})

    order_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='订单ID')

    order_num = Column(String(200), nullable=False, comment='订单编号')

    customer_id = Column(BigInteger, ForeignKey('customer.customer_id'), nullable=False, comment='客户ID')
    customer = relationship('Customer', backref='customer')

    room_id = Column(BigInteger, ForeignKey('room.room_id'), nullable=False, comment='房间ID')
    room = relationship('Room', backref='room')

    is_status = Column(Enum('0', '1'), nullable=False, server_default='0', comment='订单状态(0-> 未处理 1->已处理)')

    count_num = Column(Integer(), nullable=False, comment='入住人数')

    start_date_time = Column(DateTime(timezone=True), nullable=False, comment='入住时间')

    leave_date_time = Column(DateTime(timezone=True), nullable=False, comment='离开时间')

    description = Column(String(1000), server_default='无', comment='订单备注')
