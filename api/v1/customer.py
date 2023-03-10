import jsonpickle
from aioredis import Redis
from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from database.mysql import get_db
from database.redis import get_redis
from exception.custom import InsertException, UpdateException, DeleteException, QueryException, UserPasswordException, \
    SecurityScopeException, UserNotFoundException
from models import Customer
from schemas.common import Page
from schemas.customer import CustomerDto, CustomerOutDto, CustomerLoginDto, CustomerUpdatePasswordDto
from schemas.order import OrderDto
from schemas.result import Success

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[list[CustomerDto]]], summary='获取顾客(分页)')
async def get(page: int, size: int, customer_name: str = None):
    try:
        if customer_name:
            total = db.query(Customer).filter(Customer.customer_name.like('%{0}%'.format(customer_name))).count()
            record = db.query(Customer).filter(Customer.customer_name.like('%{0}%'.format(customer_name))).limit(
                size).offset((page - 1) * size).all()
            return Success(data=Page(total=total, record=record), message='查询成功')

        total = db.query(Customer).count()
        record = db.query(Customer).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total, record=record), message='查询成功')
    except:
        QueryException(code=400, message='查询失败')


@router.post('/insert', response_model=Success, summary='注册顾客')
async def insert(data: CustomerOutDto):
    try:
        db.add(Customer(customer_name=data.customer_name, customer_account=data.customer_account, id_card=data.id_card,
                        telephone=data.telephone, customer_password=get_password_hash(data.customer_password),
                        description=data.description))
        db.commit()
    except:
        db.rollback()
        raise InsertException(code=400, message='注册失败')
    return Success(message='注册成功')


@router.get('/customer_account', response_model=Success[CustomerDto], summary='客户信息通过账户名字获取')
async def customer_by_account(customer_account: str):
    try:
        return Success(data=db.query(Customer).filter(Customer.customer_account == customer_account).first(),
                       message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/id_card', response_model=Success[CustomerDto], summary='客户信息通过ID名字获取')
async def customer_by_account(id_card: str):
    try:
        return Success(data=db.query(Customer).filter(Customer.id_card == id_card).first(),
                       message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.post('/stay', response_model=Success, summary='顾客入住')
async def login(data: OrderDto):
    print(data)


@router.post('/login', response_model=Success[CustomerDto], summary='顾客登录')
async def login(data: CustomerLoginDto):
    customer = db.query(Customer).filter(Customer.customer_account == data.customer_account).first()
    if not customer:
        customer = db.query(Customer).filter(Customer.id_card == data.customer_account).first()
    if not customer:
        customer = db.query(Customer).filter(Customer.telephone == data.customer_account).first()
    if not customer or not verify_password(data.customer_password, customer.customer_password):
        raise UserPasswordException()
    if not bool(int(customer.is_status)):
        raise SecurityScopeException(code=403, message='当前用户未激活')
    redis: Redis = await get_redis()
    await redis.set(name='customer-info', value=jsonpickle.encode(customer))
    return Success(data=customer, message='登录成功')


@router.get('/logout', response_model=Success, summary='顾客注销')
async def logout():
    try:
        redis: Redis = await get_redis()
        keys: list[str] = ['customer-info']
        for key in keys:
            await redis.delete(key)
        return Success(message='注销成功')
    except:
        raise UpdateException(code=400, message='注销失败')


@router.delete('/delete/{id}', response_model=Success, summary='删除顾客')
async def delete(id: int):
    try:
        db.delete(db.query(Customer).filter(Customer.customer_id == id).first())
        db.commit()
        return Success(message='删除成功')
    except:
        db.rollback()
        raise DeleteException(code=400, message='删除失败')


@router.put('/update/status', response_model=Success, summary='更新顾客状态')
async def update_status(data: CustomerDto):
    try:
        item = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
        item.is_status = '1' if data.is_status else '0'
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')


@router.put('/update/password', response_model=Success, summary='更新顾客密码')
async def update(data: CustomerUpdatePasswordDto):
    item = db.query(Customer).filter(Customer.customer_account == data.account).first()
    if not item:
        raise UserNotFoundException(message='用户不存在')
    if not verify_password(data.old_pw, item.customer_password):
        raise UserPasswordException(message='原密码不正确')
    try:
        item.customer_password = get_password_hash(data.new_pw)
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')


@router.put('/update', response_model=Success, summary='更新顾客')
async def update(data: CustomerDto):
    try:
        item = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
        item.customer_name = data.customer_name
        item.id_card = data.id_card
        item.telephone = data.telephone
        item.description = data.description
        db.commit()
        return Success(message='更新成功')
    except:
        db.rollback()
        raise UpdateException(code=400, message='更新失败')
