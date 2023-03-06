from datetime import timedelta

import jsonpickle
from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.const import Const
from core.security import authenticate, generate_token, logout_redis
from database.mysql import get_db
from database.redis import get_redis
from models import User_Role, Role_Menu, Menu
from schemas.menu import MenuDto
from schemas.result import Success
from schemas.token import Token
from schemas.user import LoginDto

router = APIRouter()
db: Session = next(get_db())


@router.post('/login', response_model=Token, summary='登录认证')
async def login(data: OAuth2PasswordRequestForm = Depends()):
    redis: Redis = await get_redis()
    user = await authenticate(data.username, data.password)
    token: str = await generate_token({'id': user.user_id, 'sub': user.username, 'scopes': []})
    menus: list[MenuDto | Menu] = db.query(Menu).filter(Menu.menu_id.in_([i.menu_id for i in db.query(Role_Menu).filter(
        Role_Menu.role_id == db.query(User_Role).filter(
            User_Role.user_id == user.user_id).first().role_id).all()])).all()
    userinfo = LoginDto(username=user.username, real_name=user.real_name, is_admin=user.is_admin, gender=user.gender,
                        is_status=True if user.is_status == '1' else False,
                        menus=menus)
    await redis.setex(name=Const.TOKEN, value=token, time=timedelta(milliseconds=settings.JWT_EXPIRE))
    await redis.set(name='current-user', value=jsonpickle.encode(userinfo))
    return Token(code=200, message='登陆成功', access_token=token, expired_time=settings.JWT_EXPIRE, login=userinfo)


@router.get('/logout', response_model=Success, summary='用户注销')
async def logout():
    await logout_redis()
    return Success(code=200, message='注销成功')
