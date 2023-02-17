from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException, QueryException
from models.order import Order
from schemas.common import Page
from schemas.order import OrderDto
from schemas.result import Success
from utils.order import get_uuid

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[OrderDto]]], summary='获取订单(分页)')
async def get(page: int, size: int):
    try:
        total = db.query(Order).count()
        record = db.query(Order).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='添加订单')
async def add(data: OrderDto):
    try:
        db.add(Order(order_num=get_uuid(), customer_id=data.customer_id, room_id=data.room_id,
                     is_status=data.is_status, description=data.description))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')
    return Success(message='添加成功')


@router.delete('/delete/{id}', response_model=Success, summary='删除订单')
async def delete(id: int):
    try:
        db.delete(db.query(Order).filter(Order.order_id == id).first())
        db.commit()
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')
    return Success(message='删除成功')


@router.put('/update/status', response_model=Success, summary='更新订单状态')
async def update_status(data: OrderDto):
    try:
        item = db.query(Order).filter(Order.order_id == data.order_id).first()
        item.is_status = data.is_status
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')


@router.put('/update', response_model=Success, summary='更新订单')
async def update(data: OrderDto):
    try:
        item = db.query(Order).filter(Order.order_id == data.order_id).first()
        item.room_id = data.room_id
        item.customer_id = data.customer_id
        item.description = data.description
        item.is_status = data.is_status
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')
