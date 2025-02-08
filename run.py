import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv,find_dotenv

from handlers.finance import finance
from handlers.statistic import statistic
from db.engine import create_db

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher()

dp.include_router(finance)
dp.include_router(statistic)


async def main():
    logging.basicConfig(level=logging.INFO)
    # await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
