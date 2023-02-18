from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from database.mysql import get_db
from exception.custom import InsertException, UpdateException, DeleteException, QueryException, UserPasswordException, \
    SecurityScopeException
from models import Customer
from schemas.common import Page
from schemas.customer import CustomerDto, CustomerOutDto, CustomerLoginDto
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


@router.post('/insert', response_model=Success, summary='注册顾客')
async def insert(data: CustomerOutDto):
    try:
        print(data)
        db.add(Customer(customer_name=data.customer_name, customer_account=data.customer_account,
                        customer_password=get_password_hash(data.customer_password), description=data.description))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='注册失败')
    return Success(message='注册成功')


@router.post('/login', response_model=Success[CustomerDto], summary='顾客登录')
async def add(data: CustomerLoginDto):
    print(data)
    customer = db.query(Customer).filter(Customer.customer_account == data.customer_account).first()
    if not verify_password(data.customer_password, customer.customer_password):
        raise UserPasswordException()
    if not bool(int(customer.is_status)):
        raise SecurityScopeException(code=403, message='当前用户未激活')
    return Success(data=customer, message='登录成功')


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


@router.put('/update/password', response_model=Success, summary='更新顾客密码')
async def update(data: CustomerOutDto):
    try:
        item = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
        item.customer_password = data.customer_password
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
        item.description = data.description
        db.commit()
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
    return Success(message='更新成功')
