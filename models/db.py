from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session


class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)

    LoginId: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

class Stock(SQLModel, table=True):
    __tablename__ = "stock"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    SKU: str = Field(unique=True, index=True)
    category: str
    unit_of_measurement: str
    quantity: float = Field(default=0)

class TransactionStatus(str, Enum):
    Ready = "Ready"
    Completed = "Completed"
    Draft = "Draft"

class TransactionType(str, Enum):
    Receipt = "Receipt"
    Delivery = "Delivery"


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: TransactionType
    SKU: str = Field(index=True)
    category: str
    quantity: float
    schedule_date: Optional[datetime] = None
    status: TransactionStatus = Field(default=TransactionStatus.Draft)
    from_location: str
    to_location: str

def create_db():
    engine = create_engine("sqlite:///coreinv.db")
    SQLModel.metadata.create_all(engine)

    return Session(engine)

if __name__ == "__main__":
    session = create_db()