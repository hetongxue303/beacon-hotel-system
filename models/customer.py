from sqlalchemy import Column, BigInteger, String, Enum

from models import Base


class Customer(Base):
    """ 菜单表 """
    __table_args__ = ({"comment": "顾客表"})

    customer_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='顾客ID')

    customer_name = Column(String(200), nullable=False, comment='顾客姓名')

    customer_account = Column(String(200), nullable=False, comment='顾客账户')

    customer_password = Column(String(200), nullable=False, comment='顾客密码')

    id_card = Column(String(18), nullable=False, comment='身份证号')

    telephone = Column(String(11), nullable=False, comment='手机号')

    is_status = Column(Enum('0', '1'), server_default='1', comment='顾客状态')

    description = Column(String(500), server_default='无', comment='顾客备注')
