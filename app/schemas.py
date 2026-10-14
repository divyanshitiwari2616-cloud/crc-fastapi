from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class ShipmentStatus(str, Enum):
    SHIPPEND="Shipped"
    DELIVERED="Delivered"
    PENDING="Pending"
    CANCEL="Cancel"
    PLACED="Placed"

class Response(BaseModel):
    id:int
    weight:float 
    content:str
    status:str

class Ship(BaseModel):
    weight:float=Field(gt=0, le=20, description ="weight must be in KGs")   
    content:str=Field(max_length=30, description="content length should be more than 30 characters"
    )
    destination:str
    expected_delivery:datetime
    status:ShipmentStatus

class ShipmentPatch(BaseModel):
    tracking_number: str | None = None
    weight: float|None=Field(default=None,gt=0,le=20)
    content:str|None=Field(default=None,max_length=30)
    destination:str|None=None
    expected_delivery:datetime|None=None

class updateshipment(Ship):
    pass

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class LogicResponse(BaseModel):
    message: str = "Login successful"
    id:int|None=None
    userid: int | None = None
    username:str|None=None
    email:EmailStr|None=None
    token: str | None = None
