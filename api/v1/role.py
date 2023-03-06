from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException, QueryException
from models import Role, Role_Menu
from schemas.common import Page
from schemas.result import Success
from schemas.role import RoleDto, RoleInfoDto

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[RoleDto]]], summary='获取角色(分页)')
async def get(page: int, size: int, role_name: str = None, is_status: bool = None):
    try:
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
    except:
        raise QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='添加角色')
async def add(data: RoleInfoDto):
    role: RoleDto = data.role
    menu_ids: list[int] = data.menu_ids
    if db.query(Role).filter(Role.role_name == role.role_name).first():
        raise InsertException(code=201, message='当前角色已存在')
    try:
        info = Role(role_name=role.role_name,
                    description=None if role.description == '' or role.description is None else role.description,
                    is_status='1' if role.is_status else '0')
        db.add(info)
        db.commit()
        for id in menu_ids:
            db.add(Role_Menu(role_id=info.role_id, menu_id=id))
            db.commit()
        return Success(message='添加成功')
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')


@router.delete('/delete/{id}', response_model=Success, summary='删除角色')
async def delete(id: int):
    try:
        for item in db.query(Role_Menu).filter(Role_Menu.role_id == id).all():
            db.query(Role_Menu).filter(Role_Menu.role_id == id, Role_Menu.menu_id == item.menu_id).delete()
        db.delete(db.query(Role).filter(Role.role_id == id).first())
        db.commit()
        return Success(message='删除成功')
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')


@router.put('/delete/batch', response_model=Success, summary='批量删除角色')
async def delete_batch(data: list[int]):
    try:
        for item in db.query(Role_Menu).filter(Role_Menu.role_id.in_(data)).all():
            db.query(Role_Menu).filter(Role_Menu.role_id == item.role_id, Role_Menu.menu_id == item.menu_id).delete()
        db.query(Role).filter(Role.role_id.in_(data)).delete()
        db.commit()
        return Success(message='删除成功')
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')


@router.put('/update', response_model=Success, summary='更新角色')
async def update(data: RoleDto):
    try:
        item = db.query(Role).filter(Role.role_id == data.role_id).first()
        item.role_name = data.role_name
        item.description = data.description
        item.is_status = '1' if data.is_status else '0'
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')


@router.put('/update/info', response_model=Success, summary='更新角色信息')
async def update_info(data: RoleInfoDto):
    try:
        role: RoleDto = data.role
        item = db.query(Role).filter(Role.role_id == role.role_id).first()
        item.role_name = role.role_name
        item.description = role.description
        item.is_status = '1' if role.is_status else '0'

        ids = data.menu_ids
        ids_all = [i.menu_id for i in db.query(Role_Menu).filter(Role_Menu.role_id == role.role_id).all()]
        add_ids = [i for i in (ids + ids_all) if i not in ids_all]
        delete_ids = [i for i in ids_all if i not in [x for x in ids if x in ids_all]]
        if delete_ids:
            db.query(Role_Menu).filter(Role_Menu.menu_id.in_(delete_ids), Role_Menu.role_id == role.role_id).delete()
        for id in add_ids:
            db.add(Role_Menu(role_id=role.role_id, menu_id=id))
        if add_ids or delete_ids:
            item.update_time = func.now()
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
