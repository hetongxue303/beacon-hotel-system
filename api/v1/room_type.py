from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException, QueryException
from models import Room_Type
from schemas.common import Page
from schemas.result import Success
from schemas.room_type import RoomTypeDto

router = APIRouter()
db: Session = next(get_db())


@router.get('/list', response_model=Success[list[RoomTypeDto]], summary='获取类型(所有)')
async def get_all():
    try:
        return Success(data=db.query(Room_Type).all(), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/page/list', response_model=Success[Page[list[RoomTypeDto]]], summary='获取类型(分页)')
async def get(page: int, size: int, room_type_name: str = None):
    try:
        if room_type_name:
            total = db.query(Room_Type).filter(Room_Type.room_type_name.like('%{0}%'.format(room_type_name))).count()
            record = db.query(Room_Type).filter(Room_Type.room_type_name.like('%{0}%'.format(room_type_name))).limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        total = db.query(Room_Type).count()
        record = db.query(Room_Type).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='添加类型')
async def add(data: RoomTypeDto):
    try:
        db.add(Room_Type(room_type_name=data.room_type_name, description=data.description))
        db.commit()
        return Success(message='添加成功')
    except:
        db.rollback()
        raise InsertException(code=400, message='新增失败')


@router.delete('/delete/{id}', response_model=Success, summary='删除类型')
async def delete(id: int):
    try:
        db.delete(db.query(Room_Type).filter(Room_Type.room_type_id == id).first())
        db.commit()
        return Success(message='删除成功')
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')


@router.put('/update', response_model=Success, summary='更新类型')
async def update(data: RoomTypeDto):
    try:
        item = db.query(Room_Type).filter(Room_Type.room_type_id == data.room_type_id).first()
        item.room_type_name = data.room_type_name
        item.description = data.description
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
