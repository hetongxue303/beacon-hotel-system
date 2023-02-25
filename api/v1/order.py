from datetime import timedelta

import jsonpickle
from aioredis import Redis
from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from database.redis import get_redis
from exception.custom import InsertException, UpdateException, DeleteException, QueryException
from models import Customer, Room
from models.order import Order
from schemas.common import Page
from schemas.customer import CustomerDto
from schemas.order import OrderDto
from schemas.result import Success
from utils.order import get_uuid

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[OrderDto]]], summary='获取订单(分页)')
async def get(page: int, size: int, customer_id: int = None, order_num: str = None, is_handler: str = None,
              is_status: bool = None):
    try:
        if is_status is not None and customer_id is not None:
            status = '1' if is_status else '0'
            total = db.query(Order).filter(Order.is_status == status, Order.customer_id == customer_id).count()
            record = db.query(Order).filter(Order.is_status == status, Order.customer_id == customer_id).limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if order_num and is_handler:
            total = db.query(Order).filter(Order.order_num.like('%{0}%'.format(order_num)),
                                           Order.is_handler == is_handler).count()
            record = db.query(Order).filter(Order.order_num.like('%{0}%'.format(order_num)),
                                            Order.is_handler == is_handler).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if is_handler:
            total = db.query(Order).filter(Order.is_handler == is_handler).count()
            record = db.query(Order).filter(Order.is_handler == is_handler).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        if order_num:
            total = db.query(Order).filter(Order.order_num.like('%{0}%'.format(order_num))).count()
            record = db.query(Order).filter(Order.order_num.like('%{0}%'.format(order_num))).limit(size).offset(
                (page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        total = db.query(Order).count()
        record = db.query(Order).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='新增预约')
async def add(data: OrderDto):
    try:
        redis: Redis = await get_redis()
        customer: CustomerDto = jsonpickle.decode(await redis.get('customer-info'))
        room = db.query(Room).filter(Room.room_id == data.room_id).first()
        room.is_state = '1'
        db.add(Order(order_num=get_uuid(), customer_id=customer.customer_id, room_id=data.room_id,
                     is_status='1' if data.is_status else '0', description=data.description, count_num=data.count_num,
                     start_date_time=data.start_date_time + timedelta(hours=8),
                     leave_date_time=data.leave_date_time + timedelta(hours=8)))
        db.commit()
        return Success(message='新增成功')
    except:
        db.rollback()
        raise InsertException(code=400, message='新增失败')


@router.post('/booking', response_model=Success, summary='添加预约')
async def booking(data: OrderDto):
    try:
        redis: Redis = await get_redis()
        customer: CustomerDto = jsonpickle.decode(await redis.get('customer-info'))
        room = db.query(Room).filter(Room.room_id == data.room_id).first()
        room.is_state = '1'
        db.add(Order(order_num=get_uuid(), customer_id=customer.customer_id, room_id=data.room_id, is_handler='1',
                     is_status='1' if data.is_status else '0', description=data.description, count_num=data.count_num,
                     start_date_time=data.start_date_time + timedelta(hours=8),
                     leave_date_time=data.leave_date_time + timedelta(hours=8)))
        db.commit()
        return Success(message='预约成功')
    except:
        db.rollback()
        raise InsertException(code=400, message='预约失败')


@router.delete('/delete/{id}', response_model=Success, summary='删除订单')
async def delete(id: int):
    try:
        order = db.query(Order).filter(Order.order_id == id).first()
        if order.is_handler == '1' or order.is_handler == '2':
            room = db.query(Room).filter(Room.room_id == order.room_id).first()
            room.is_state = '0'
        db.delete(order)
        db.commit()
        return Success(message='删除成功')
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')


@router.put('/update/status', response_model=Success, summary='更新订单状态')
async def update_status(data: OrderDto):
    try:
        item = db.query(Order).filter(Order.order_id == data.order_id).first()
        item.is_status = '1' if data.is_status else '0'
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')


@router.put('/update', response_model=Success, summary='更新订单')
async def update(data: OrderDto):
    try:
        item = db.query(Order).filter(Order.order_id == data.order_id).first()
        item.room_id = data.room_id
        item.customer_id = data.customer_id
        item.description = data.description
        item.is_status = '1' if data.is_status else '0'
        item.count_num = data.count_num
        item.start_date_time = data.start_date_time if data.start_date_time else item.start_date_time
        item.leave_date_time = data.leave_date_time if data.leave_date_time else item.leave_date_time
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
