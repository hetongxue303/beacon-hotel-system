from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException
from models import Room
from schemas.common import Page
from schemas.index import IndexDto
from schemas.result import Success

router = APIRouter()
db: Session = next(get_db())


@router.get('/page/list', response_model=Success[Page[IndexDto]], summary='获取首页数据(分页)')
async def get(page: int, size: int):
    try:
        total = db.query(Room).count()
        free_time = db.query(Room).filter(Room.is_state == '0').count()
        booking = db.query(Room).filter(Room.is_state == '1').count()
        stay = db.query(Room).filter(Room.is_state == '2').count()
        maintenance = db.query(Room).filter(Room.is_state == '3').count()
        rooms = db.query(Room).limit(size).offset((page - 1) * size).all()
        return Success(data=Page(total=total,
                                 record=IndexDto(rooms=rooms, free_time=free_time, booking=booking, stay=stay,
                                                 maintenance=maintenance)), message='查询成功')
    except:
        QueryException(code=400, message='查询失败')
