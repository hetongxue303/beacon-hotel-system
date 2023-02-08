from fastapi import APIRouter
from sqlalchemy.orm import Session
from database.mysql import get_db

router = APIRouter()
db: Session = next(get_db())


@router.post('/interface', summary='测试接口')
async def test() -> str:
    return 'test interface'
