import asyncio
import importlib.util
import os
import types
import sys
# Load the bot module by path because filename contains spaces/hyphens
THIS_DIR = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
MODULE_PATH = os.path.join(ROOT, 'tg-bot ai gemimi.py')

spec = importlib.util.spec_from_file_location('bot_module', MODULE_PATH)
bot_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot_module)

handle_message_text = bot_module.handle_message_text

class FakeBot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text, parse_mode=None):
        self.sent.append((chat_id, text, parse_mode))

async def test_handle_message_sync_model():
    class SyncModel:
        def generate_content(self, text):
            return types.SimpleNamespace(text=f"sync:{text}")

    bot = FakeBot()
    model = SyncModel()

    await handle_message_text(model, bot, 42, "hello")

    assert len(bot.sent) == 1
    assert bot.sent[0][0] == 42
    assert bot.sent[0][1] == "sync:hello"
    assert bot.sent[0][2] == "Markdown"

async def test_handle_message_async_model():
    class AsyncModel:
        async def generate_content(self, text):
            await asyncio.sleep(0)  # yield
            return types.SimpleNamespace(text=f"async:{text}")

    bot = FakeBot()
    model = AsyncModel()

    await handle_message_text(model, bot, 7, "world")

    assert len(bot.sent) == 1
    assert bot.sent[0][0] == 7
    assert bot.sent[0][1] == "async:world"
    assert bot.sent[0][2] == "Markdown"
