# import json
#
# import jsonpickle
# from fastapi.encoders import jsonable_encoder
# from sqlalchemy.orm import Session
# from core.config import settings
# from core.security import verify_password, generate_token
# from database.mysql import get_db
# from models import User, Menu, User_Role, Role, Role_Menu
# from schemas.menu import MenuDto
# from schemas.token import Token
# from schemas.user import LoginDto
#
# db: Session = next(get_db())
#
# if __name__ == '__main__':
#     username = 'admin'
#     password = '74ce4a21f159e81638334cbe243cd2cf'
#     user = db.query(User).filter(User.username == username).first()
#     if not verify_password(password, user.password):
#         print('密码错误')
#     token: str = '515645s1d5a1ad85ad05a64'
#     menus = db.query(Menu).filter(Menu.menu_id.in_([i.menu_id for i in db.query(Role_Menu).filter(
#         Role_Menu.role_id == db.query(User_Role).filter(
#             User_Role.user_id == user.user_id).first().role_id).all()])).all()
#     userinfo = LoginDto(username=user.username, real_name=user.real_name, is_admin=user.is_admin,
#                         gender=user.gender,
#                         menus=menus)
#     print(jsonable_encoder(
#         Token(code=200, message='登陆成功', access_token=token, expired_time=settings.JWT_EXPIRE, user=userinfo)))
