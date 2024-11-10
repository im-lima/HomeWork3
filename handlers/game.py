# game.py
from aiogram import types, Dispatcher
import random
from config import bot


async def game_dice(message: types.Message):
    games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
    await bot.send_dice(chat_id=message.from_user.id, emoji=random.choice(games))

async def advanced_game_dice(message: types.Message):
    selected_dice = random.choice(['⚽', '🎰', '🎲'])
    bot_roll = await bot.send_dice(chat_id=message.from_user.id, emoji=selected_dice)
    player_roll = await bot.send_dice(chat_id=message.from_user.id, emoji=selected_dice)

    if bot_roll.dice.value > player_roll.dice.value:
        await bot.send_message(chat_id=message.from_user.id, text="Бот выиграл!")
    elif bot_roll.dice.value < player_roll.dice.value:
        await bot.send_message(chat_id=message.from_user.id, text="Вы выиграли!")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Ничья!")

def register_handler_game(dp: Dispatcher):
    dp.register_message_handler(game_dice, commands=['game'])
    dp.register_message_handler(advanced_game_dice, commands=['advanced_game'])