from pydantic import BaseModel,EmailStr
from datetime import datetime
class UserSignup(BaseModel):
    full_name:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    full_name:str
    email:str
    is_active:bool
    created_at:datetime
    class Config:
        from_attributes=True
        #deeni orm_mode=true ani kuda rastaru..actually idhi true set cheste mana pydantic andedhi ee paina attributes ni sarigga check cheyagalugutundii..

class Token(BaseModel):
    access_token:str
    token_type:str        
