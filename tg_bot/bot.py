from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import BotCommand
import os
import logging
from aiogram.utils import executor

from app.config import bc
from app.handlers.common import register_handlers_common
from app.handlers.manage_offer import register_handlers_manage_offers

logger = logging.getLogger(__name__)

async def on_startup(dp: Dispatcher):
    logger.info("Starting bot")
    commands = [
        BotCommand(command="/"+com, description=inf["desc"]) for com, inf in bc.COMMANDS.items()
    ]
    await dp.bot.set_my_commands(commands)
    logger.info("Set bot commands")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=os.environ.get("TOKEN"), parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    dp.setup_middleware(LoggingMiddleware(logger=logger))

    register_handlers_common(dp)
    register_handlers_manage_offers(dp)

    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)

