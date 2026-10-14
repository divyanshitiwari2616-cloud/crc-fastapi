
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from app.auth import logout_token
from app.database.model import Shipment, User
from app.database.session import create_db_and_table, get_session
from app.hash import generate_password, verify_password
from app.schemas import Ship


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class LoginResponse(BaseModel):
    message: str
    id: int
    username: str
    email: str


class ShipmentPatch(BaseModel):
    model_config = ConfigDict(extra="allow")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(lifespan=lifespan)
SESSION_DEPENDENCY = Depends(get_session)
LOGOUT_DEPENDENCY = Depends(logout_token)


@app.post("/create-user", response_model=UserResponse)
def create_new_user(data: UserCreate, session: Session = SESSION_DEPENDENCY):
    existing_user = session.exec(
        select(User).where((User.username == data.username) | (User.email == data.email))
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    hashed_password = generate_password(data.password)
    new_user = User(username=data.username, email=data.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get("/")
def home():
    return {"message": "hello db"}


@app.post("/login", response_model=LoginResponse)
def user_login(data: UserCreate, session: Session = SESSION_DEPENDENCY):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    password_correct = verify_password(data.password, user.hashed_password)

    if not password_correct:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return LoginResponse(message="Login successful", id=user.id, username=user.username, email=user.email)

    # token = create_access_token(user.id)
    # return LoginResponse(
    #     message="Login successful",
    #     userid=user.id,
    #     username=user.username,
    #     email=user.email,
    #     token=token
    # )

@app.post("/new_shipment")
def new_shipment(data:Ship,session:Session=SESSION_DEPENDENCY):
    shipment = Shipment.model_validate(data.model_dump())
    session.add(shipment)     
    session.commit()           
    session.refresh(shipment)  
    return shipment


@app.post("/logout")
def logout(
    result: dict = LOGOUT_DEPENDENCY,
):
    return result

@app.get("/get-shipment")
def get_shipment(session:Session=SESSION_DEPENDENCY):
    statement = select(Shipment)
    shipment= session.exec(statement).all()
    return shipment

@app.get("/profile")
def get_profile(user_id: int, session: Session = SESSION_DEPENDENCY):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/update-shipment/{shipment_id}")
def update_shipment(shipment_id:int, data:Ship, session:Session=SESSION_DEPENDENCY):
    shipment = session.get(Shipment, shipment_id)
    shipment.sqlmodel_update(data.model_dump())
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.patch("/shipments/{shipment_id}")
def shipment_patch(
    shipment_id: int,
    data: ShipmentPatch,
    session: Session = SESSION_DEPENDENCY):
    shipment = session.get(Shipment, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404,detail="Shipment not found")
    shipment.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int, session: Session = SESSION_DEPENDENCY):
    shipment = session.get(Shipment, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404,detail="Shipment not found")
    session.delete(shipment)
    session.commit()
    return {"message": "Shipment deleted successfully"}
