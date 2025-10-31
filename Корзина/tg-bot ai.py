import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from mistralai import Mistral

api_key = "****" # НУЖНО ЗАМЕНИТЬ НА СВОЙ АПИ КЛЮЧ В ФОРМАТЕ: api_key = "ххххххххх"
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
bot = Bot(token="") # ⚠️ ИЗМЕНИТЬ ТОКЕН 
dp = Dispatcher()

# Хэндлер на команду /start ---------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    start_text = "Welcome to @direcode"
    await bot.send_message(message.chat.id, start_text)


# ОБРАБОТЧИК ИИ ЗАПРОСА
@dp.message()
async def message_handler(msg: Message):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": msg.text,
            },
        ]
    )
    # print(chat_response.choices[0].message.content)
    await bot.send_message(msg.chat.id, chat_response.choices[0].message.content, parse_mode = "Markdown")



# Запуск процесса поллинга новых апдейтов
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




