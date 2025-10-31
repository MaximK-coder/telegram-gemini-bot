import asyncio
import inspect
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.utils.exceptions import CantParseEntities
from aiogram.utils.markdown import escape_md

from dotenv import load_dotenv
import google.generativeai as genai

# Загружаем .env рядом со скриптом
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Настройка логирования
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO),
                    format="%(asctime)s %(levelname)s: %(message)s")

# Проверка версии aiogram — скрипт рассчитан на aiogram 2.x
try:
    import aiogram as _aiogram_pkg
    _aiogram_ver = getattr(_aiogram_pkg, "__version__", None)
    if not _aiogram_ver or not _aiogram_ver.startswith("2."):
        logging.error("Detected aiogram version %s; this script requires aiogram 2.x.", _aiogram_ver)
        logging.error("To fix: python -m pip install 'aiogram==2.25.1'")
        raise RuntimeError(f"Unsupported aiogram version: {_aiogram_ver}. Please install aiogram==2.25.1")
except ImportError:
    logging.error("aiogram is not installed. Install with: python -m pip install 'aiogram==2.25.1'")
    raise RuntimeError("aiogram is not installed")

# Глобальные клиенты (будут инициализированы в init_clients)
model = None
bot = None
dp = None

# Проверка доступных моделей
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

def init_clients():
    """Инициализирует модель и Telegram-клиент. Вызывать перед стартом бота."""
    global model, bot, dp

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    logging.info("Checking .env at: %s", env_path)

    # Требуемые переменные
    required = ["GENAI_API_KEY", "TG_BOT_TOKEN"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        logging.error("Missing environment variables: %s", ", ".join(missing))
        raise RuntimeError("Отсутствуют переменные окружения: %s" % ", ".join(missing))

    # Инициализация модели и бота
    genai.configure(api_key=os.environ["GENAI_API_KEY"])
    model = genai.GenerativeModel(os.getenv("GENAI_MODEL", "gemini-flash-latest"))

    bot = Bot(token=os.environ["TG_BOT_TOKEN"])
    dp = Dispatcher(bot)

    # Регистрация хэндлеров
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(message_handler)


async def cmd_start(message: types.Message):
    await message.reply("Привет, Макс!")


async def message_handler(message: types.Message):
    # Вызов модели и отправка ответа
    await handle_message_text(model, bot, message.chat.id, message.text)


async def handle_message_text(model, bot, chat_id, text):
    try:
        call = getattr(model, "generate_content", None)
        if call is None:
            raise AttributeError("Модель не предоставляет метод generate_content")

        if inspect.iscoroutinefunction(call):
            response = await call(text)
        else:
            response = await asyncio.to_thread(call, text)

        out_text = getattr(response, "text", str(response))

    except Exception as e:
        logging.exception("Ошибка при вызове модели")
        await bot.send_message(chat_id, f"Ошибка при вызове модели: {e}")
        return

    # Try sending as Markdown; if Telegram can't parse entities, escape and retry.
    try:
        await bot.send_message(chat_id, out_text, parse_mode="Markdown")
    except CantParseEntities:
        logging.warning("Can't parse entities in model output; escaping Markdown and retrying")
        try:
            escaped = escape_md(out_text)
        except Exception:
            # If escaping fails for some reason, fallback to raw text
            escaped = out_text
        try:
            await bot.send_message(chat_id, escaped, parse_mode="Markdown")
        except Exception:
            logging.exception("Failed to send escaped Markdown; sending without parse_mode")
            await bot.send_message(chat_id, out_text)


def main():
    init_clients()
    # Ensure there's an event loop for aiogram's executor on Python 3.10+
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()