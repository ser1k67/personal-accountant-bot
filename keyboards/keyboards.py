from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


def keyboard(*args: str, adj: tuple[int]):
    keyboard = ReplyKeyboardBuilder()

    for i in args:
        keyboard.add(KeyboardButton(text=i))

    return keyboard.adjust(*adj).as_markup(resize_keyboard=True, one_time_keyboard = True)