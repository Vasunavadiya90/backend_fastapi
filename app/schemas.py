from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field
from typing import Annotated
from pydantic import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

class PostCreate(PostBase):
    pass
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]