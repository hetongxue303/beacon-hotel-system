from fastapi import FastAPI

from core.logger import logger
from core.middleware import cors_middleware, http_middleware
from api.base import init_router
from database.mysql import init_db
from database.redis import init_redis_pool
from exception.globals import init_exception


def events_listen(app: FastAPI):
    """
    启动/关机 活动监听
    :param app: 主程序
    :return: none
    """

    @app.on_event('startup')
    async def startup():
        """
        应用程序启动之前执行
        :return: none
        """
        init_db()  # 初始化数据库
        cors_middleware(app)  # 配置跨域中间件
        http_middleware(app)  # 配置http中间件
        init_exception(app)  # 开启全局异常捕获
        init_router(app)  # 注册路由
        await init_redis_pool(app)  # 初始化redis
        logger.success('启动成功！！！')
        logger.success('访问文档: http://127.0.0.1:8000/docs')

    @app.on_event('shutdown')
    async def shutdown():
        """
        应用程序关闭之前执行
        :return:
        """
        await app.state.redis.close()
        logger.success('redis已关闭')
