from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException
from models import Role
from schemas.common import Page
from schemas.result import Success
from schemas.role import RoleDto

router = APIRouter()
db: Session = next(get_db())


@router.get('/list', response_model=Success[Page[list[RoleDto]]], summary='获取角色(分页)')
async def get(page: int, size: int, role_name: str = None, is_status: bool = None):
    if role_name and is_status is not None:
        is_status = int(is_status)
        total = db.query(Role).filter(Role.role_name.like('%{0}%'.format(role_name)),
                                      Role.is_status == is_status.__str__()).count()
        record = db.query(Role).filter(Role.role_name.like('%{0}%'.format(role_name)),
                                       Role.is_status == is_status.__str__()).limit(size).offset(
            (page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')

    if role_name:
        total = db.query(Role).filter(Role.role_name.like('%{0}%'.format(role_name))).count()
        record = db.query(Role).filter(Role.role_name.like('%{0}%'.format(role_name))).limit(
            size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')

    if is_status is not None:
        is_status = int(is_status)
        total = db.query(Role).filter(Role.is_status == is_status.__str__()).count()
        record = db.query(Role).filter(Role.is_status == is_status.__str__()).limit(size).offset(
            (page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')

    total = db.query(Role).count()
    record = db.query(Role).limit(size).offset((page - 1) * size).all()
    return Success(data=Page(total=total, record=record), message='查询成功')


@router.post('/add', response_model=Success, summary='添加角色')
async def add(data: RoleDto):
    if db.query(Role).filter(Role.role_name == data.role_name).first():
        raise InsertException(code=201, message='当前角色已存在')
    try:
        db.add(Role(role_name=data.role_name, description=data.description, is_status='1' if data.is_status else '0'))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')
    return Success(message='添加成功')


@router.delete('/delete/{id}', response_model=Success, summary='删除角色')
async def delete(id: int):
    try:
        db.delete(db.query(Role).filter(Role.role_id == id).first())
        db.commit()
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')
    return Success(message='删除成功')


@router.put('/update', response_model=Success, summary='更新角色')
async def update(data: RoleDto):
    try:
        item = db.query(Role).filter(Role.role_id == data.role_id).first()
        item.role_name = data.role_name
        item.description = data.description
        item.is_status = '1' if data.is_status else '0'
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')
