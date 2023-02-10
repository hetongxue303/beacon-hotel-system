from models.base import Base
from sqlalchemy import Column, BigInteger, String, Enum


class User(Base):
    """ 用户表 """
    __table_args__ = ({"comment": "用户表"})

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')

    username = Column(String(200), nullable=False, comment='账户')

    password = Column(String(200), server_default='', comment='密码')

    real_name = Column(String(200), nullable=False, comment='姓名')

    gender = Column(Enum('1', '2'), nullable=False, comment='性别')

    is_status = Column(Enum('0', '1'), server_default='0', comment='状态')

    is_admin = Column(Enum('0', '1'), server_default='0', comment='是否管理员')

    description = Column(String(500), server_default='无', comment='备注')
