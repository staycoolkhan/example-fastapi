from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint, ConfigDict
    
class PostBase(BaseModel):
    title:str 
    content: str
    published: bool = True
   
class PostCreate(PostBase):
    pass

# Response model   
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

# Response model
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config(ConfigDict):
         from_attributes = True

# Response model
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config(ConfigDict):
         from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=-1, le=1)
    