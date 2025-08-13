from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic import conint

# User response model 
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # class Config: # Pydantic: get data from database
    #     from_attribute = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

## response model
class Post(PostBase): # inherits from PostBase
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # type hint for relationship with User model
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attribute = True

## response model
class PostOut(BaseModel):
    post: Post
    votes: int
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attribute = True

# User schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# vote.request
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # pyright: ignore[reportInvalidTypeForm]
