import asyncio
import importlib.util
import os
import pytest

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BOT_PATH = os.path.join(ROOT, "tg-bot ai gemimi.py")


def load_bot_module():
    spec = importlib.util.spec_from_file_location("bot_mod", BOT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.asyncio
async def test_handle_message_markdown_fallback():
    mod = load_bot_module()

    # Prepare a fake model whose generate_content returns an object with text
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    class FakeModel:
        def generate_content(self, text):
            # Return a string with an unmatched '[' to simulate broken markdown
            return FakeResponse("Hello [world - unmatched bracket")

    # Prepare a fake bot which raises CantParseEntities on first send, then succeeds
    class FakeBot:
        def __init__(self):
            self.calls = []
            self._count = 0

        async def send_message(self, chat_id, text, parse_mode=None):
            self._count += 1
            if self._count == 1:
                # Simulate Telegram rejecting the first message due to bad entities
                raise mod.CantParseEntities("can't find end of the entity")
            # Record successful send
            self.calls.append((chat_id, text, parse_mode))
            return True

    fake_bot = FakeBot()
    fake_model = FakeModel()

    # Run handler
    await mod.handle_message_text(fake_model, fake_bot, chat_id=12345, text="trigger")

    # After handler, fake_bot.calls should contain one successful send (the retry)
    assert len(fake_bot.calls) == 1
    chat_id, sent_text, parse_mode = fake_bot.calls[0]
    assert chat_id == 12345
    # We expect parse_mode to be "Markdown" for the retry
    assert parse_mode == "Markdown"
    # The sent_text should contain the original content (possibly escaped)
    assert "Hello" in sent_text
