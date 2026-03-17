import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = '8600981350:AAHH7uZCzif1zCpCYhXsvRJfA0LH04ZU_zw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Бот работает.")

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer("Бот был создан Моисеевой Екатериной с помощью искусственного интеллекта и некоторых знаний в сфере кода.

Зайдя в Python, кинула базу с ИИ - чтобы не сидеть три часа над одной скобкой. Когда код ожил, закинула репозиторий на GitHub, дабы не потерять плоды своих трудов.
Понятно, что держать ноут включенным 24/7 - это бред, так что я просто закинула всё на bothost.ru. Привязала репозиторий, тыкнула кнопку, и бот сразу залетел в онлайн. Теперь он работает 24/7 сам.")

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