import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from core.logger import logger
from core.config import settings


def cors_middleware(app: FastAPI):
    """
    跨域中间件
    :param app: 主程序
    :return: none
    """
    if settings.APP_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*'],
            allow_credentials=True
        )
        logger.success('跨域已开启！！！')


WHITE_LIST = {'/v1/login', '/v1/logout', '/v1/captchaImage'}


def http_middleware(app: FastAPI):
    """
    请求/响应拦截器
    :param app:
    :return:
    """

    @app.middleware("http")
    async def http_middleware_init(request: Request, call_next):
        """
        每次请求判断除白名单之外得所有请求是否携带有token
        有：放行
        无：抛异常并返回错误信息
        :param request:
        :param call_next:
        :return:
        """
        start_time = time.time()
        response = await call_next(request)
        # if request.url.path not in WHITE_LIST:
        #     try:
        #         token = request.headers.get('access_token')
        #         payload = jwt.decode(token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        #         redis: Redis = await get_redis(request)
        #         save_token: str = await redis.get(name=Const.TOKEN)
        #         # token不存在
        #         if not token:
        #             logger.warning('凭证不存在')
        #             return error_json(message='凭证不存在', code=401)
        #         # 与redis中的token不匹配
        #         if not save_token or save_token != token:
        #             logger.warning('无效凭证')
        #             return error_json(message='无效凭证', code=401)
        #     except ExpiredSignatureError:
        #         logger.warning('凭证过期')
        #         return error_json(message='凭证过期', code=401)
        #     except JWTError:
        #         logger.warning('凭证异常')
        #         return error_json(message='凭证异常', code=401)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 2))
        logger.debug('方法:{}  地址:{}  耗时:{} ms', request.method, request.url, str(round(process_time, 2)))
        return response
