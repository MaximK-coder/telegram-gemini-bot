import importlib.util
import os
import asyncio

TEST_PATH = os.path.join(os.path.dirname(__file__), 'tests', 'test_handler.py')
spec = importlib.util.spec_from_file_location('test_mod', TEST_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

async def run():
    await mod.test_handle_message_sync_model()
    await mod.test_handle_message_async_model()

if __name__ == '__main__':
    asyncio.run(run())
