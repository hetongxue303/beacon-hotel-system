from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from models import RoomType
from schemas.common import Page
from schemas.result import Success
from schemas.room_type import RoomTypeDto

router = APIRouter()
db: Session = next(get_db())


@router.get('/list', response_model=Success[Page[list[RoomTypeDto]]], summary='获取类型(分页)')
async def get(page: int, size: int, room_type_name: str = None):
    if room_type_name:
        total = db.query(RoomType).filter(RoomType.room_type_name.like('%{0}%'.format(room_type_name))).count()
        record = db.query(RoomType).filter(RoomType.room_type_name.like('%{0}%'.format(room_type_name))).limit(
            size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    total = db.query(RoomType).count()
    record = db.query(RoomType).limit(size).offset((page - 1) * size).all()
    return Success(data=Page(total=total, record=record), message='查询成功')


@router.post('/add', response_model=Success, summary='添加类型')
async def add(data: RoomTypeDto):
    try:
        db.add(RoomType(room_type_name=data.room_type_name, description=data.description))
        db.commit()
    except:
        db.rollback()
    return Success(message='添加成功')


@router.delete('/delete/{id}', response_model=Success, summary='删除类型')
async def delete(id: int):
    try:
        db.delete(db.query(RoomType).filter(RoomType.room_type_id == id).first())
        db.commit()
    except:
        db.rollback()
    return Success(message='删除成功')


@router.put('/update', response_model=Success, summary='更新类型')
async def update(data: RoomTypeDto):
    try:
        item: RoomType = db.query(RoomType).filter(RoomType.room_type_id == data.room_type_id).first()
        item.room_type_name = data.room_type_name
        item.description = data.description
        db.commit()
    except:
        db.rollback()
    return Success(message='更新成功')
