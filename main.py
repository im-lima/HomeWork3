from config import bot, dp
from aiogram import executor, types
import logging
from handlers import commands, quiz, fsm_reg, game, fsm_store


commands.register_commands(dp)
quiz.register_handler_quiz(dp)
fsm_reg.reg_handler_fsm_registration(dp)
game.register_handler_game(dp)
fsm_store.register_handler_store(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, allowed_updates=['callback'])