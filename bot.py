import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

games = {}

def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Крестики-нолики", callback_data="game_ttt")],
        [InlineKeyboardButton(text="🎲 Кубик", callback_data="game_dice")]
    ])
    return kb

def create_board():
    return [" " for _ in range(9)]

def board_to_keyboard(board):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            index = i + j
            text = board[index] if board[index] != " " else "⬜"
            row.append(InlineKeyboardButton(text=text, callback_data=f"move_{index}"))
        kb.inline_keyboard.append(row)
    return kb

@dp.message()
async def start(message: types.Message):
    await message.answer("🎮 Выбери игру:", reply_markup=main_menu())

@dp.callback_query(lambda c: c.data == "game_ttt")
async def start_ttt(callback: types.CallbackQuery):
    game_id = callback.message.chat.id
    games[game_id] = {
        "board": create_board(),
        "turn": "❌"
    }

    await callback.message.edit_text(
        "Игра началась! Ход ❌",
        reply_markup=board_to_keyboard(games[game_id]["board"])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("move_"))
async def handle_move(callback: types.CallbackQuery):
    game_id = callback.message.chat.id
    game = games.get(game_id)

    if not game:
        return await callback.answer("Нет игры")

    index = int(callback.data.split("_")[1])

    if game["board"][index] != " ":
        return await callback.answer("Занято")

    game["board"][index] = game["turn"]
    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"

    await callback.message.edit_text(
        f"Ход {game['turn']}",
        reply_markup=board_to_keyboard(game["board"])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "game_dice")
async def dice(callback: types.CallbackQuery):
    import random
    num = random.randint(1, 6)
    await callback.message.edit_text(f"🎲 Выпало: {num}", reply_markup=main_menu())
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
