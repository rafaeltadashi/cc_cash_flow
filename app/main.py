from databases import Database
from enum import Enum
from fastapi import FastAPI
from os import environ
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum as EnumSQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = FastAPI()
engine = create_engine(environ.get("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
database = Database(environ.get("DATABASE_URL"))
Base.metadata.create_all(engine)


class TransactionKind(Enum):
    DEBIT = 1
    CREDIT = 2


class TransactionModel(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(String, index=True)
    kind = Column(EnumSQL(TransactionKind))


class Transaction(BaseModel):
    amount: float
    kind: TransactionKind


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def create_transaction(t: Transaction):
    async with database.transaction():
        database_item = await database.execute(
            query=TransactionModel.__table__.insert(), 
            values=t.dict())
        return {"item": t, "database_item": database_item}


async def list_transactions():
    async with database.transaction():
        return await database.fetch_all()


@app.post("/transaction")
async def register(t: Transaction):
    if not t or t <= 0:
        return {"error": "Valor deve ser maior ou igual a zero"}
    await create_transaction(t)
    return {"message": "Registrado com sucesso"}


@app.get("/transactions")
async def list():
    await list_transactions()
    return {"message": "Registrado com sucesso"}
