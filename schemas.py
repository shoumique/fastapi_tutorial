from pydantic import BaseModel
from datetime import datetime

# This part handles User Data sending to us
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# This part handles Our Data sends back to user
class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True