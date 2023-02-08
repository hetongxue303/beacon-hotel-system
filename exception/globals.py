from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from core.logger import logger
from exception.custom import *
from schemas.result import error_json, success_json


def init_exception(app: FastAPI):
    logger.success('全局异常捕获已开启！！！')

    @app.exception_handler(Exception)
    async def http_exception(request: Request, e: Exception):
        return error_json(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")

    @app.exception_handler(UnauthorizedException)
    async def http_exception(request: Request, e: UnauthorizedException):
        logger.warning(e.message)
        return error_json(code=status.HTTP_401_UNAUTHORIZED, message=e.message)

    @app.exception_handler(SecurityScopeException)
    async def http_exception(request: Request, e: SecurityScopeException):
        logger.warning(e.message)
        return error_json(code=e.code, message=e.message, headers=e.headers)

    @app.exception_handler(UserNotFoundException)
    async def http_exception(request: Request, e: UserNotFoundException):
        logger.warning(e.message)
        return success_json(code=status.HTTP_400_BAD_REQUEST, message=e.message)

    @app.exception_handler(UserPasswordException)
    async def http_exception(request: Request, e: UserPasswordException):
        logger.warning(e.message)
        return success_json(code=status.HTTP_400_BAD_REQUEST, message=e.message)

    @app.exception_handler(CaptchaException)
    async def http_exception(request: Request, e: CaptchaException):
        logger.warning(e.message)
        return success_json(code=status.HTTP_400_BAD_REQUEST, message=e.message)

    @app.exception_handler(UpdateException)
    async def http_exception(request: Request, e: UpdateException):
        logger.warning(e.message)
        return success_json(code=e.code, message=e.message)
