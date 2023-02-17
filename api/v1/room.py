from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import InsertException, DeleteException, UpdateException, QueryException
from models import Room, Room_Type
from schemas.common import Page
from schemas.result import Success
from schemas.room import RoomDto

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[RoomDto]]], summary='获取客房(分页)')
async def get(page: int, size: int, room_type_id: int = None, room_name: str = None, is_status: bool = None):
    try:
        if room_name and room_type_id is not None and is_status is not None:
            is_status = int(is_status)
            total = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                          Room.room_type_id == room_type_id,
                                          Room.is_status == is_status.__str__()).count()
            record = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                           Room.room_type_id == room_type_id,
                                           Room.is_status == is_status.__str__()).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if room_name and room_type_id is not None:
            total = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                          Room.room_type_id == room_type_id).count()
            record = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                           Room.room_type_id == room_type_id).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if room_name and is_status is not None:
            is_status = int(is_status)
            total = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                          Room.is_status == is_status.__str__()).count()
            record = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                           Room.is_status == is_status.__str__()).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if room_name:
            total = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name))).count()
            record = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name))).limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if room_type_id is not None:
            total = db.query(Room).filter(Room.room_type_id == room_type_id).count()
            record = db.query(Room).filter(Room.room_type_id == room_type_id).limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if is_status is not None:
            is_status = int(is_status)
            total = db.query(Room).filter(Room.is_status == is_status.__str__()).count()
            record = db.query(Room).filter(Room.is_status == is_status.__str__()).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        total = db.query(Room).count()
        record = db.query(Room).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/home/page/list', response_model=Success[Page[list[RoomDto]]], summary='获取客房(首页)')
async def get(page: int, size: int, room_type_id: int = None, room_name: str = None):
    try:

        if room_name and room_type_id is not None:
            total = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                          Room.is_status == '1', Room.room_type_id == room_type_id).count()
            record = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)),
                                           Room.is_status == '1', Room.room_type_id == room_type_id).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if room_name:
            total = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)), Room.is_status == '1').count()
            record = db.query(Room).filter(Room.room_name.like('%{0}%'.format(room_name)), Room.is_status == '1').limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if room_type_id is not None:
            total = db.query(Room).filter(Room.room_type_id == room_type_id, Room.is_status == '1').count()
            record = db.query(Room).filter(Room.room_type_id == room_type_id, Room.is_status == '1').limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        total = db.query(Room).filter(Room.is_status == '1').count()
        record = db.query(Room).filter(Room.is_status == '1').limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='添加客房')
async def add(data: RoomDto):
    try:
        db.add(Room(room_name=data.room_name, room_type_id=data.room_type_id, room_count=data.room_count,
                    room_price=data.room_price, room_bed=data.room_bed, room_detail=data.room_detail,
                    is_status='1' if data.is_status else '0'))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')
    return Success(message='添加成功')


@router.delete('/delete/{id}', response_model=Success, summary='删除客房')
async def delete(id: int):
    try:
        db.delete(db.query(Room).filter(Room.room_id == id).first())
        db.commit()
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')
    return Success(message='删除成功')


@router.put('/update/status', response_model=Success, summary='更新客房状态')
async def update_status(data: RoomDto):
    try:
        item = db.query(Room).filter(Room.room_id == data.room_id).first()
        item.is_status = '1' if data.is_status else '0'
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')


@router.put('/update', response_model=Success, summary='更新客房')
async def update(data: RoomDto):
    if not db.query(Room_Type).filter(Room_Type.room_type_id == data.room_type_id).first():
        raise UpdateException(code=400, message='当前客房类型不存在')
    try:
        item = db.query(Room).filter(Room.room_id == data.room_id).first()
        item.room_name = data.room_name
        item.room_price = data.room_price
        item.room_count = data.room_count
        item.room_bed = data.room_bed
        item.room_type_id = data.room_type_id
        item.is_status = '1' if data.is_status else '0'
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')
