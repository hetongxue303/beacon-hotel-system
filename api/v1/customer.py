from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException, QueryException
from models import Customer
from schemas.common import Page
from schemas.customer import CustomerDto
from schemas.result import Success

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[CustomerDto]]], summary='获取顾客(分页)')
async def get(page: int, size: int):
    try:
        total = db.query(Customer).count()
        record = db.query(Customer).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        QueryException(code=400, message='查询失败')


@router.post('/add', response_model=Success, summary='添加/注册顾客')
async def add(data: CustomerDto):
    try:
        db.add(Customer(customer_name=data.customer_name, customer_account=data.customer_account,
                        customer_password=data.customer_password, description=data.description))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='添加失败')
    return Success(message='添加成功')


@router.delete('/delete/{id}', response_model=Success, summary='删除顾客')
async def delete(id: int):
    try:
        db.delete(db.query(Customer).filter(Customer.customer_id == id).first())
        db.commit()
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')
    return Success(message='删除成功')


@router.put('/update/status', response_model=Success, summary='更新顾客状态')
async def update_status(data: CustomerDto):
    try:
        item = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
        item.is_status = data.is_status
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')


@router.put('/update', response_model=Success, summary='更新顾客')
async def update(data: CustomerDto):
    try:
        item = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
        item.is_status = data.is_status
        item.customer_name = data.customer_name
        item.customer_account = data.customer_account
        item.customer_password = data.customer_password
        item.description = data.description
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')
