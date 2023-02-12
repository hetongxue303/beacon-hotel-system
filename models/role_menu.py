"""
角色菜单表
@Author:何同学
"""
from sqlalchemy import BigInteger, Column, ForeignKey

from models.base import Base


class Role_Menu(Base):
    """ 角色菜单表 """
    __table_args__ = ({"comment": "角色菜单表"})

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')

    role_id = Column(BigInteger, ForeignKey('role.role_id'), comment='角色ID')

    menu_id = Column(BigInteger, ForeignKey('menu.menu_id'), comment='菜单ID')
