import typing

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic.generics import GenericModel
from starlette import status

T = typing.TypeVar("T")


class Success(GenericModel, typing.Generic[T]):
    code: typing.Optional[int] | None = status.HTTP_200_OK
    message: str | None = '请求成功'
    data: typing.Optional[T] | None = None


class Success_Page(GenericModel, typing.Generic[T]):
    code: typing.Optional[int] | None = status.HTTP_200_OK
    message: str | None = '请求成功'
    total: int
    data: typing.Optional[T] | None = None


class Error(GenericModel, typing.Generic[T]):
    code: typing.Optional[int] | None = status.HTTP_400_BAD_REQUEST
    message: str | None = '请求错误'
    data: typing.Optional[T] | None = None


def success_json(
        *,
        code: int = status.HTTP_200_OK,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        message: str = '请求成功',
        data: typing.Any | None = None
):
    return JSONResponse(status_code=code, headers=headers,
                        content={'code': code, 'message': message, 'data': jsonable_encoder(data)})


def error_json(
        *,
        code: int = status.HTTP_400_BAD_REQUEST,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        message: str = '请求错误',
        data: typing.Any | None = None
):
    return JSONResponse(status_code=code, headers=headers,
                        content={'code': code, 'message': message, 'data': jsonable_encoder(data)})
