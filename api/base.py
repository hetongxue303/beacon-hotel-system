from api.v1 import test, security, room_type, user, role, room, order, customer
from fastapi import APIRouter, FastAPI
from core.config import settings

router = APIRouter(prefix='/v1')

router.include_router(security.router, tags=['安全模块'])
router.include_router(room_type.router, tags=['客房类型'], prefix='/type')
router.include_router(user.router, tags=['员工管理'], prefix='/user')
router.include_router(role.router, tags=['角色管理'], prefix='/role')
router.include_router(room.router, tags=['客房管理'], prefix='/room')
router.include_router(order.router, tags=['订单管理'], prefix='/order')
router.include_router(customer.router, tags=['顾客管理'], prefix='/customer')
router.include_router(test.router, tags=['测试'], prefix='/test')


def init_router(app: FastAPI):
    app.include_router(router, prefix=settings.APP_API_PREFIX)
