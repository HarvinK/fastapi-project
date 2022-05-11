from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

#pydantic Schema for data validation
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


#shchema for creating post
class PostCreate(PostBase):
    pass


#Response model/schema for user
class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    #converts sqlalchemy model to Pydantic model (dict)
    class Config:
        orm_mode = True


#Response model/schema for posts (extends PostBase)
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    #converts sqlalchemy model to Pydantic model (dict)
    class Config:
        orm_mode = True

#Response model to return post data AND vote data (only implemented on get_posts and get_post)
class PostOUT(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

#schema for registering user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


#schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


#shcema for token
class Token(BaseModel):
    access_token: str
    token_type: str


#schema for token data in access_token
class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)