# echo.py
from aiogram import types, Dispatcher


async def echo_handler (message: types.Message):
    if message.text.isdigit():
        number = int(message.text)
        await message.answer(f'Квадрат числа {number} равен {number ** 2}')
    else:
        await message.answer (message.text)


def register_echo (dp: Dispatcher):
    dp.register_message_handler(echo_handler)