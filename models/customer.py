from sqlalchemy import Column, BigInteger, String

from models import Base


class Customer(Base):
    """ 菜单表 """
    __table_args__ = ({"comment": "顾客表"})

    customer_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='顾客ID')

    customer_name = Column(String(200), nullable=False, comment='顾客姓名')
