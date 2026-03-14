from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
from sqlalchemy import func
from sqlmodel import Field, SQLModel, create_engine, Session, select


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
    quantity: int = Field(default=0)

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
    SKU: str = Field(index=True, foreign_key="stock.SKU")
    category: str
    quantity: int
    schedule_date: Optional[datetime] = None
    status: TransactionStatus = Field(default=TransactionStatus.Draft)
    from_location: str
    to_location: str

def create_db():
    db_path = Path(__file__).parent / "coreinv.db"
    db_exists = db_path.exists()

    engine = create_engine(f"sqlite:///{db_path}")

    if not db_exists:
        SQLModel.metadata.create_all(engine)

    return Session(engine)

if __name__ == "__main__":
    session = create_db()
    u1 = Users(LoginId="alice123", email="alice@example.com", password_hash="hash1")
    u2 = Users(LoginId="bob123456", email="bob@example.com", password_hash="hash2")
    u3 = Users(LoginId="charlie123456", email="charlie@example.com", password_hash="hash3")
    users = [u1, u2, u3]

    s1 = Stock(name="Laptop", SKU="SKU1001", category="Electronics", unit_of_measurement="pcs", quantity=25)
    s2 = Stock(name="Rice Bag", SKU="SKU1002", category="Food", unit_of_measurement="kg", quantity=100)
    s3 = Stock(name="T-Shirt", SKU="SKU1003", category="Clothing", unit_of_measurement="pcs", quantity=60)
    s4 = Stock(name="Trouser", SKU="SKU1004", category="Clothing", unit_of_measurement="pcs", quantity=80)
    s5 = Stock(name="Mobile", SKU="SKU1005", category="Electronics", unit_of_measurement="pcs", quantity=100)
    s6 = Stock(name="Milk", SKU="SKU1006", category="Food", unit_of_measurement="l", quantity=70)
    s7 = Stock(name="Bulb", SKU="SKU1007", category="Electronics", unit_of_measurement="pcs", quantity=50)
    s8 = Stock(name="Shoes", SKU="SKU1008", category="Clothing", unit_of_measurement="pcs", quantity=110)
    s9 = Stock(name="Refined Oil", SKU="SKU1009", category="Food", unit_of_measurement="l", quantity=80)
    s10 = Stock(name="Refrigerator", SKU="SKU10010", category="Electronics", unit_of_measurement="pcs", quantity=90)
    stocks = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

    t1 = Transaction(
        type=TransactionType.Receipt,
        SKU="SKU1001",
        category="Electronics",
        quantity=10,
        schedule_date=(datetime.now() + timedelta(days=14)),
        status=TransactionStatus.Ready,
        from_location="Supplier",
        to_location="Warehouse"
    )

    t2 = Transaction(
        type=TransactionType.Delivery,
        SKU="SKU1002",
        category="Food",
        quantity=20,
        schedule_date=datetime.now(),
        status=TransactionStatus.Completed,
        from_location="Warehouse",
        to_location="Store-A"
    )

    t3 = Transaction(
        type=TransactionType.Receipt,
        SKU="SKU1003",
        category="Clothing",
        quantity=30,
        schedule_date=datetime.now(),
        status=TransactionStatus.Draft,
        from_location="Factory",
        to_location="Warehouse"
    )
    trans = [t1, t2, t3]

    session.add_all(trans)
    session.add_all(users)
    session.add_all(stocks)
    session.commit()

    # statement = (
    #     select(Transaction.type, func.count(Transaction.id).label("count"))
    #     .group_by(Transaction.type)
    # )
    # results = session.exec(statement)
    # for x in results:
    #     print(x)

