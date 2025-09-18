import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppData
from aiogram.filters import Command

# Токен из переменной окружения (без hardcoded)
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN environment variable not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply(
        "Welcome to Annoying Pixel!\nClick the button to play.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Play Game", web_app=types.WebAppInfo(url="YOUR_GAME_URL_HERE"))]
        ])
    )

@dp.message(Command('play'))
async def play(message: types.Message):
    await message.reply(
        "Let's play!",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Start", web_app=types.WebAppInfo(url="YOUR_GAME_URL_HERE"))]
        ])
    )

@dp.web_app_data()
async def handle_web_app_data(web_app_data: WebAppData):
    # Получаем данные от WebApp
    data = json.loads(web_app_data.data)
    win = data.get('win', False)
    cleared = data.get('cleared', '0')
    time_left = data.get('timeLeft', 0)
    
    # Формируем сообщение
    if win:
        text = f"🎉 {web_app_data.from_user.first_name} won! Cleared {cleared}% in {time_left // 60}:{time_left % 60:02d}!"
    else:
        text = f"😞 {web_app_data.from_user.first_name} lost. Cleared {cleared}%."
    
    # Отправляем в чат
    await bot.send_message(chat_id=web_app_data.from_user.id, text=text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
