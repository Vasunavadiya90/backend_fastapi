from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        
class Userlogin(BaseModel):
    email:EmailStr
    password:str
