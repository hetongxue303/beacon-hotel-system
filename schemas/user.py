from pydantic import BaseModel


class LoginDto(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
