from models.base import Base
from sqlalchemy import Column, BigInteger, String, Enum


class Role(Base):
    """ 角色表 """
    __table_args__ = ({"comment": "角色表"})

    role_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='角色ID')

    role_name = Column(String(200), nullable=False, comment='名称')

    is_status = Column(Enum('0', '1'), server_default='0', comment='状态')

    description = Column(String(500), server_default='无', comment='备注')
