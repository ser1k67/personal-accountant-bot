from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db.engine import add_expense, add_income
from keyboards.keyboards import keyboard

# router
finance = Router()           
    

# расход или доход
@finance.message(Command("add"))
async def start(message: types.Message):
    await message.answer("Расход или Доход?", reply_markup=keyboard("расход", "доход", adj=(2,)))


# расход
class Expense(StatesGroup):
    many = State()
    who = State()
    reason = State()

@finance.message(StateFilter(None), F.text == "расход")
async def many(message: types.Message, state: FSMContext):
    await message.answer("сколько потратил?")
    await state.set_state(Expense.many)

@finance.message(Expense.many, F.text)
async def who(message: types.Message, state: FSMContext):
    await state.update_data(many = message.text)
    await message.answer("кто?", reply_markup=keyboard("папа", "мама", "куаныш", "назарали", adj=(2,2)))
    await state.set_state(Expense.who)

@finance.message(Expense.who, F.text)
async def reason(message: types.Message, state: FSMContext):
    await state.update_data(who = message.text)
    await message.answer("для чего?", reply_markup=keyboard("продукты", "работа", "транспорт", "развлечения", "неизвестно", adj=(2,2,1)))
    await state.set_state(Expense.reason)

@finance.message(Expense.reason, F.text)
async def end(message: types.Message, state: FSMContext):
    await state.update_data(reason = message.text)
    data = await state.get_data()
    await add_expense(data)
    await message.answer(f"Успешно сохранено\nкто: {data["who"]}\nсколько: {data["many"]}\nдля чего: {data["reason"]}")
    await state.clear()



# доход
class Income(StatesGroup):
    many = State()
    where_from = State()
    reason = State()

@finance.message(StateFilter(None), F.text == "доход")
async def many(message: types.Message, state: FSMContext):
    await message.answer("сколько получил?")
    await state.set_state(Income.many)

@finance.message(Income.many, F.text)
async def where_from(message: types.Message, state: FSMContext):
    await state.update_data(many = message.text)
    await message.answer("от кого?", reply_markup=keyboard("папа", "мама", "куаныш", "назарали", adj=(2,2)))
    await state.set_state(Income.where_from)

@finance.message(Income.where_from, F.text)
async def reason(message: types.Message, state: FSMContext):
    await state.update_data(where_from = message.text)
    await message.answer("причина дохода?")
    await state.set_state(Income.reason)

@finance.message(Income.reason, F.text)
async def end(message: types.Message, state: FSMContext):
    await state.update_data(reason = message.text)
    data = await state.get_data()
    await add_income(data)
    await message.answer(f"Успешно сохранено\nкто: {data["where_from"]}\nсколько: {data["many"]}\nпричина дохода: {data["reason"]}")
    await state.clear()
