import os

from db import models

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())


# connect db & create sessionmaker & create tables method
DATABASE_URL = os.getenv("DB_URL")
engine = create_async_engine(DATABASE_URL, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# add expense
async def add_expense(data: dict):
    async with session_maker() as session:
        session.add(models.Expense_Base(many=int(data["many"]), who=data["who"], reason=data["reason"]))
        await session.commit()

# add income
async def add_income(data: dict):
    async with session_maker() as session:
        session.add(models.Income_Base(many=int(data["many"]), where_from=data["where_from"], reason=data["reason"]))
        await session.commit()

