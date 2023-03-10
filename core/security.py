from datetime import timedelta, datetime
from typing import List

import jsonpickle
from aioredis import Redis
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.const import Const
from core.config import settings
from database.mysql import get_db
from database.redis import get_redis
from exception.custom import *
from models import User
from schemas.token import TokenData

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oAuth2 = OAuth2PasswordBearer('/v1/login')


def verify_password(plain_password: str, hashed_password: str):
    """
    密码校验
    :param plain_password: 原密码
    :param hashed_password: 加密后的密码
    :return: 对比结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    密码加密
    :param password: 原密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


async def get_user(username: str, db: Session = next(get_db())) -> User:
    """
    查询用户
    :param username: 用户名
    :param db: 数据库
    :return: 账户信息
    """
    return db.query(User).filter(User.username == username).first()


# async def set_current_user_info(user_id: int, db: Session = next(get_db())):
#     """
#     设置当前用户信息
#     :param user_id: 用户ID
#     :param db: 数据库
#     """
#     redis: Redis = await get_redis()
#     role_ids: List[int] = []
#     menu_ids: List[int] = []
#     role_key: List[str] = []
#     for v in db.query(User_Role).filter(User_Role.user_id == user_id).all():
#         role_ids.append(v.role_id)
#     for v in db.query(Role_Menu).filter(Role_Menu.role_id.in_(role_ids)).all():
#         menu_ids.append(v.menu_id)
#     roles: List[Role] = db.query(Role).filter(Role.role_id.in_(role_ids)).all()
#     menus: List[Menu] = db.query(Menu).filter(Menu.menu_id.in_(menu_ids)).all()
#     if roles:
#         for v in roles:
#             role_key.append(v.role_key)
#     await redis.set(name='current-role-ids', value=jsonpickle.encode(role_ids))
#     await redis.set(name='current-role-keys', value=jsonpickle.encode(role_key))
#     await redis.set(name='current-role-data', value=jsonpickle.encode(roles))
#     await redis.set(name='current-menu-ids', value=jsonpickle.encode(menu_ids))
#     await redis.set(name='current-menu-data', value=jsonpickle.encode(menus))


async def generate_scopes():
    """
    生成作用域列表
    """
    # redis: Redis = await get_redis()
    # menu_data: List[Menu] = jsonpickle.decode(await redis.get('current-menu-data'))
    # scopes: List[str] = []
    # if menu_data:
    #     for v in menu_data:
    #         if v.per_key:
    #             scopes.append(v.per_key)
    # await redis.set(name='current-scopes', value=jsonpickle.encode(scopes))


async def logout_redis():
    """
    用户登出操作
    :return:
    """
    redis: Redis = await get_redis()
    redis_key: List[str] = ['authorization', 'current-user']
    for v in redis_key:
        await redis.delete(v)


async def authenticate(username: str, password: str) -> User:
    """
    登录认证
    :param username: 用户名
    :param password: 密码
    :return: 账户信息
    """
    user = await get_user(username)
    if not user:
        raise UserNotFoundException()
    if not verify_password(password, user.password):
        raise UserPasswordException()
    if not bool(int(user.is_status)):
        raise SecurityScopeException(code=403, message='当前用户未激活')
    return user


async def generate_token(data: dict, expires_time: int | None = None) -> str:
    """
    生成Token
    :param data:
    :param expires_time:
    :return: token
    """
    if not expires_time:
        expire = datetime.now() + timedelta(milliseconds=15 * 60 * 1000)
    else:
        expire = datetime.now() + timedelta(milliseconds=expires_time)
    data.update({'exp': expire})
    return jwt.encode(claims=data,
                      key=settings.JWT_SECRET_KEY,
                      algorithm=settings.JWT_ALGORITHM)


async def captcha_check(code: str) -> bool:
    """
    校验验证码
    :param code: 用户输入的验证码
    :return: 比对结果
    """
    redis: Redis = await get_redis()
    save_code: str = await redis.get(name=Const.CAPTCHA)
    if not save_code:
        raise CaptchaException(message='验证码过期')
    if save_code.lower() != code.lower():
        await redis.delete(Const.CAPTCHA)
        raise CaptchaException(message='验证码错误')
    await redis.delete(Const.CAPTCHA)
    return True


async def check_token(token: str = Depends(oAuth2)):
    """
    校验token
    :param token: token
    :return: payload
    """
    try:
        redis: Redis = await  get_redis()
        authorization: str = await redis.get('authorization')
        if authorization != token:
            raise SecurityScopeException(code=401, message='凭证异常', headers={"WWW-Authenticate": 'Bearer '})
        payload = jwt.decode(token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if not payload:
            raise JwtVerifyException(message='无效凭证')
        return payload
    except ExpiredSignatureError:
        raise JwtVerifyException('凭证过期')
    except JWTError:
        raise JwtVerifyException('凭证解析失败')


async def check_permissions(security_scopes: SecurityScopes, token: str = Depends(oAuth2)):
    """
    权限校验
    :param security_scopes:
    :param token:
    :return: 账户信息
    """
    redis: Redis = await  get_redis()
    authorization: str = await redis.get('authorization')
    if authorization != token:
        raise SecurityScopeException(code=401, message='凭证异常', headers={"WWW-Authenticate": 'Bearer '})
    payload = await check_token(token)
    if not payload:
        raise JwtVerifyException(message='无效凭证')
    token_data = TokenData(username=payload.get('sub', None),
                           scopes=jsonpickle.decode(await redis.get('current-scopes')))
    user = get_user(token_data.username)
    if security_scopes.scopes:
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise SecurityScopeException(code=403,
                                             message='权限不足，联系管理员！',
                                             headers={"WWW-Authenticate": 'Bearer '})
    elif user is None:
        raise SecurityScopeException(code=401, message='凭证异常', headers={"WWW-Authenticate": 'Bearer '})
