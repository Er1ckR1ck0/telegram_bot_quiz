import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.enums.content_type import ContentType
import commands
import start_quiz
bot = Bot(token="7010982662:AAFvp2zIp4Zra4C5orCN0ahS0Kww87ADJQk")

async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router, start_quiz.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
    