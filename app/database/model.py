from sqlmodel import SQLModel, Field  # noqa: I001
from enum import Enum
from datetime import datetime


class ShipmentStatus(str, Enum):
    PLACED="placed"
    IN_TRANSIT="in_transit"
    DELIVERED="delivered"
    CANCELLED="cancelled"


class Shipment(SQLModel, table=True):
    __tablename__="ships"
    id:int | None= Field (default=None,primary_key=True)  # noqa: F821, RUF100
    content:str
    weight:float
    status:str
    destination:str
    expected_delivery:datetime  # type: ignore  # noqa: F821, RUF100


class User(SQLModel, table=True):
    __tablename__="users"
    id:int | None= Field (default=None,primary_key=True)  # noqa: F821, RUF100
    username:str=Field (index=True,unique=True)  # noqa: F821, RUF100
    email:str=Field (index=True,unique=True)  # noqa: F821, RUF100
    hashed_password:str