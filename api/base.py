from api.v1 import test, security
from fastapi import APIRouter, FastAPI
from core.config import settings

router = APIRouter(prefix='/v1')

router.include_router(security.router, tags=['安全模块'])
router.include_router(test.router, tags=['测试模块'], prefix='/test')


def init_router(app: FastAPI):
    app.include_router(router, prefix=settings.APP_API_PREFIX)
