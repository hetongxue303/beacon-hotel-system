import jsonpickle
from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import UpdateException, DeleteException, InsertException, QueryException
from models import Menu, User, User_Role, Role_Menu
from schemas.common import Page
from schemas.menu import MenuDto, MenuTreeDto
from schemas.result import Success

router = APIRouter()
db: Session = next(get_db())


@router.get('/list', response_model=Success[list[MenuDto]], summary='获取菜单(所有)')
async def get_all():
    try:
        return Success(data=db.query(Menu).all(), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/by_role_id/{role_id}', response_model=Success[list[MenuDto]], summary='获取菜单(所有)')
async def get_all(role_id: int):
    try:
        role_menus = db.query(Role_Menu).filter(Role_Menu.role_id == role_id).all()
        rms: list[int] = []
        for rm in role_menus:
            rms.append(rm.menu_id)
        return Success(data=db.query(Menu).filter(Menu.menu_id.in_(rms)).all(), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/page/list', response_model=Success[Page[list[MenuDto]]], summary='获取菜单(分页)')
async def get(page: int, size: int):
    try:
        total = db.query(Menu).count()
        record = db.query(Menu).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/tree', response_model=Success[list[MenuTreeDto]], summary='获取菜单(树)')
async def get_tree():
    try:
        return Success(data=filter_menu(data=db.query(Menu).all()), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/tree/{username}', response_model=Success[list[MenuDto]], summary='获取我的菜单')
async def get_my_tree(username: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            user_role = db.query(User_Role).filter(User_Role.user_id == user.user_id).first()
            role_menus = db.query(Role_Menu).filter(Role_Menu.role_id == user_role.role_id).all()
            rms: list[int] = []
            for rm in role_menus:
                rms.append(rm.menu_id)
            return Success(data=db.query(Menu).filter(Menu.menu_id.in_(rms)).all(), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


def filter_menu(data: list[Menu], parent_id: int = 0) -> list[MenuTreeDto]:
    tree_data: list[MenuTreeDto] = []
    for item in data:
        if item.parent_id == parent_id:
            temp: MenuTreeDto | Menu = item
            temp.children = filter_menu(data=data, parent_id=item.menu_id)
            tree_data.append(temp)
    return tree_data


@router.post('/add', response_model=Success, summary='新增菜单')
async def add(data: MenuDto):
    try:
        db.add(Menu(parent_id=data.parent_id, menu_title=data.menu_title, menu_type=data.menu_type,
                    router_name=data.router_name, router_path=data.router_path, component=data.component,
                    sort=data.sort, icon=data.icon, permission=data.permission, is_show='1' if data.is_show else '0',
                    is_sub='1' if data.is_sub else '0', is_status='1' if data.is_status else '0',
                    description=data.description, sub_count=data.sub_count if data.sub_count != 0 else 0))
        db.commit()
        return Success(message='添加成功')
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')


@router.delete('/delete/{id}', response_model=Success, summary='删除菜单')
async def delete(id: int):
    try:
        db.delete(db.query(Menu).filter(Menu.menu_id == id).first())
        db.commit()
        return Success(message='删除成功')
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')


@router.put('/update/status', response_model=Success, summary='更新菜单状态')
async def update_status(data: MenuDto):
    try:
        item = db.query(Menu).filter(Menu.menu_id == data.menu_id).first()
        item.is_status = '1' if data.is_status else '0'
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')


@router.put('/update/show', response_model=Success, summary='更新显示状态')
async def update_status(data: MenuDto):
    try:
        item = db.query(Menu).filter(Menu.menu_id == data.menu_id).first()
        item.is_show = '1' if data.is_show else '0'
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')


@router.put('/update', response_model=Success, summary='更新菜单')
async def update(data: MenuDto):
    try:
        item = db.query(Menu).filter(Menu.menu_id == data.menu_id).first()
        item.parent_id = data.parent_id
        item.menu_title = data.menu_title
        item.menu_type = data.menu_type
        item.router_name = data.router_name
        item.router_path = data.router_path
        item.component = data.component,
        item.sort = data.sort
        item.icon = data.icon
        item.sub_count = data.sub_count
        item.permission = data.permission
        item.is_sub = '1' if data.is_sub else '0'
        item.description = data.description
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
