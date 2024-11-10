# buttons.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

a = False
cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=a)
cancel_button = KeyboardButton('Отмена')
cancel.add(cancel_button)