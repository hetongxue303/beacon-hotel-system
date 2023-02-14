from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.security import get_password_hash
from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException, QueryException
from models import User
from schemas.common import Page
from schemas.result import Success
from schemas.user import UserDto, UserOutDto

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[UserDto]]], summary='获取员工(分页)')
async def get(page: int, size: int, real_name: str = None, is_status: bool = None):
    try:
        if real_name and is_status is not None:
            is_status = int(is_status)
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name)),
                                          User.is_status == is_status.__str__()).count()
            record = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name)),
                                           User.is_status == is_status.__str__()).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if real_name:
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).count()
            record = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if is_status is not None:
            is_status = int(is_status)
            total = db.query(User).filter(User.is_status == is_status.__str__()).count()
            record = db.query(User).filter(User.is_status == is_status.__str__()).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        total = db.query(User).count()
        record = db.query(User).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='添加用户')
async def add(data: UserOutDto):
    if db.query(User).filter(User.username == data.username).first():
        raise InsertException(code=201, message='当前账户已存在')
    try:
        db.add(User(username=data.username, password=get_password_hash(data.password),
                    real_name=data.real_name, description=data.description, gender=data.gender))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')
    return Success(message='添加成功')


@router.delete('/delete/{id}', response_model=Success, summary='删除用户')
async def delete(id: int):
    try:
        db.delete(db.query(User).filter(User.user_id == id).first())
        db.commit()
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')
    return Success(message='删除成功')


@router.put('/update', response_model=Success, summary='更新用户')
async def update(data: UserDto):
    try:
        item = db.query(User).filter(User.user_id == data.user_id).first()
        item.real_name = data.real_name
        item.gender = data.gender
        item.description = data.description
        item.is_status = '1' if data.is_status else '0'
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')
