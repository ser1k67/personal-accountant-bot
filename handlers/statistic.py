import calendar
import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import func, select

from db.models import Expense_Base, Income_Base
from db.engine import session_maker
from keyboards.keyboards import keyboard


statistic = Router()
days = []


# get data from db 
async def add_stats_expense():
    async with session_maker() as session:
        values = await session.execute(select(Expense_Base).where(func.extract("day", Expense_Base.created).in_(days)))
        return values.scalars().all()
    
async def add_stats_incomes():
    async with session_maker() as session:
        values = await session.execute(select(Income_Base).where(func.extract("day", Income_Base.created).in_(days)))
        return values.scalars().all()


# write statistic function for handlers
async def stats_write(period):
    data_e = await add_stats_expense()
    data_i = await add_stats_incomes()
    all_ = 0

    # +incomes to users if day == today day
    naza_i = kuka_i = papa_i = mama_i = all_i = 0
    for i in data_i:
        if i.created.day in days:
            if i.where_from == "назарали":
                naza_i += i.many
            elif i.where_from == "куаныш":
                kuka_i += i.many
            elif i.where_from == "папа":
                papa_i += i.many
            elif i.where_from == "мама":
                mama_i += i.many
            all_i += i.many
            all_ += i.many

    # +expenses to users if day == today day
    naza_e = kuka_e = papa_e = mama_e = all_e = 0
    for i in data_e:
        if i.created.day in days:
            if i.who == "назарали":
                naza_e += i.many
            elif i.who == "куаныш":
                kuka_e += i.many
            elif i.who == "папа":
                papa_e += i.many
            elif i.who == "мама":
                mama_e += i.many
            all_e += i.many
            all_ -= i.many

    # answer today stats
    return  f"Статистика за {period}:\n\
            \nРАСХОДЫ:\nНазарали - {naza_e}\nКуаныш - {kuka_e}\nПапа - {papa_e}\nМама - {mama_e}\n\
            \nДОХОДЫ:\nНазарали - {naza_i}\nКуаныш - {kuka_i}\nПапа - {papa_i}\nМама - {mama_i}\n\
            \nОбщие расходы - {all_e}\nОбщие доходы - {all_i}\n\nБаланс - {all_}"


# check 
def add_days_for_stats(which_days: int):
    global days
    # today date & days after month
    today = datetime.datetime.now().date()
    _, days_in_month = calendar.monthrange(today.year, today.month-1)

    # list which days db import data 
    days = [today.day-i for i in range(which_days) if today.day-i > 0]
    # but if day > 0, work it's cycle while lengh of list == 7
    if len(days) < which_days:
        days.append(days_in_month)
        if len(days) < which_days:
            while len(days) < which_days:
                days.append(days_in_month-1)
                days_in_month -= 1


######################################### statistic ###########################################

# menu
@statistic.message(Command("statistic"))
async def stats(message: types.Message):
    await message.answer("какой период?", reply_markup=keyboard("сегодня", "3 дня", "7 дней", "30 дней", adj=(2,2)))


# today
@statistic.message(F.text == "сегодня")
async def one(message: types.Message):
    add_days_for_stats(1)
    stats = await stats_write("1 дней")
    await message.answer(f"{stats}")

    del days[:]

# 3 days
@statistic.message(F.text == "3 дня")
async def three(message: types.Message):
    add_days_for_stats(3)
    stats = await stats_write("3 дней")
    await message.answer(f"{stats}")

    del days[:]

# 7 days
@statistic.message(F.text == "7 дней")
async def three(message: types.Message):
    add_days_for_stats(7)
    stats = await stats_write("7 дней")
    await message.answer(f"{stats}")

    del days[:]

# 30 days
@statistic.message(F.text == "30 дней")
async def three(message: types.Message):
    add_days_for_stats(30)
    stats = await stats_write("30 дней")
    await message.answer(f"{stats}")

    del days[:]
