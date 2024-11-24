# main.py
import logging
from aiogram import executor
from config import bot, dp, Admins
from db import db_main
from handlers import commands, quiz, fsm_reg, game, fsm_store, echo, send_products, send_and_delete_products

async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот включен!')
    await db_main.sql_create()

async def on_shutdown(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот выключен!')

commands.register_commands(dp)
quiz.register_handler_quiz(dp)
fsm_reg.reg_handler_fsm_registration(dp)
game.register_handler_game(dp)
fsm_store.reg_handler_fsm_store(dp)
send_products.register_handlers(dp)
send_and_delete_products.register_handlers(dp)
echo.register_echo(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, allowed_updates=['callback'],
                           on_startup=on_startup, on_shutdown=on_shutdown)