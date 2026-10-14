from sqlalchemy import create_engine  # noqa: I001
from sqlmodel import SQLModel, Session
from app.database.model import Shipment,User  # noqa: F401


engine=create_engine(url="sqlite:///supply.db",echo=True, connect_args={"check_same_thread":False})

def create_db_and_table():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session