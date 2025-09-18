import asyncio
   import json
   import os
   from aiogram import Bot, Dispatcher, types
   from aiogram.dispatcher.filters import Command
   from aiogram.types import WebAppData

   # Токен из переменной окружения
   TOKEN = os.getenv('TOKEN')
   if not TOKEN:
       raise ValueError("TOKEN environment variable not set")

   bot = Bot(token=TOKEN)
   dp = Dispatcher(bot)

   @dp.message_handler(commands=['start'])
   async def start(message: types.Message):
       await message.reply(
           "Welcome to Annoying Pixel!\nClick the button to play.",
           reply_markup=types.InlineKeyboardMarkup().add(
               types.InlineKeyboardButton("Play Game", web_app=types.WebAppInfo(url="https://obscurusinf-lab.github.io/annoying_pixel/"))
           )
       )

   @dp.message_handler(commands=['play'])
   async def play(message: types.Message):
       await message.reply(
           "Let's play!",
           reply_markup=types.InlineKeyboardMarkup().add(
               types.InlineKeyboardButton("Start", web_app=types.WebAppInfo(url="https://obscurusinf-lab.github.io/annoying_pixel/"))
           )
       )

   @dp.web_app_data_handler()
   async def handle_web_app_data(web_app_data: WebAppData):
       data = json.loads(web_app_data.data)
       win = data.get('win', False)
       cleared = data.get('cleared', '0')
       time_left = data.get('timeLeft', 0)
       
       if win:
           text = f"🎉 {web_app_data.user.first_name} won! Cleared {cleared}% in {time_left // 60}:{time_left % 60:02d}!"
       else:
           text = f"😞 {web_app_data.user.first_name} lost. Cleared {cleared}%."
       
       await bot.send_message(chat_id=web_app_data.user.id, text=text)

   async def main():
       await dp.start_polling()

   if __name__ == '__main__':
       asyncio.run(main())
