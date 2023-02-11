from sqlalchemy import BigInteger, Column, ForeignKey

from models.base import Base


class UserRole(Base):
    """ 用户角色表 """
    __table_args__ = ({"comment": "用户角色表"})

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')

    user_id = Column(BigInteger, ForeignKey('user.user_id'), comment='用户ID')

    role_id = Column(BigInteger, ForeignKey('role.role_id'), comment='角色ID')
