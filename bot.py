import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = '8600981350:AAHH7uZCzif1zCpCYhXsvRJfA0LH04ZU_zw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Бот работает.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Я отвечаю на /start и /help")

@dp.message(Command("ip"))
async def cmd_ip(message: types.Message):
    await message.answer("Тута шото про ИП")

@dp.message(Command("samozan"))
async def cmd_samozan(message: types.Message):
    await message.answer("Тута чота про самозанятость")

async def main():
    print("Бот запущен! Иди проверяй в телеге.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")