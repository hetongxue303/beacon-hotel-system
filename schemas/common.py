import typing

from pydantic.generics import GenericModel

ModelType = typing.TypeVar("ModelType")


class Page(GenericModel, typing.Generic[ModelType]):
    total: int = None
    record: typing.Optional[ModelType] | None = None


class ListDto(GenericModel, typing.Generic[ModelType]):
    ids: list[ModelType] = None
