from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# This part handles User Data sending to us
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    is_ai_generated: Optional[bool] = False

# Response for UserCreate Model
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# This part handles Our Data sends back to user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    is_ai_generated: bool

    class Config:
        orm_mode = True


# USER FUNCTIONALITIES
class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserGet(UserOut):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
