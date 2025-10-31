import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from mistralai import Mistral

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токены из переменных окружения
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

# Инициализируем клиент Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

# Включаем логирование
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализируем бота и диспетчер
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    start_text = "Welcome to @direcode"
    await bot.send_message(message.chat.id, start_text)

# Обработчик ИИ запроса
@dp.message()
async def message_handler(msg: Message):
    try:
        chat_response = client.chat.complete(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": msg.text,
                },
            ]
        )
        await bot.send_message(
            msg.chat.id,
            chat_response.choices[0].message.content,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await bot.send_message(
            msg.chat.id,
            "Извините, произошла ошибка при обработке запроса. Попробуйте позже."
        )

# Запуск процесса поллинга новых апдейтов
async def main():
    logger.info("Starting bot...")
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())