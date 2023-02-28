from aiogram import Bot, Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio

from app.handlers import common, consume, manage

logger = logging.getLogger(__name__)

async def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
    bot = Bot("5914064878:AAGLPDKK2SHeoAIwt08LJH_33p66UoI3KgE")

    dp.include_router(manage.router)
    dp.include_router(common.router)
    dp.include_router(consume.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
    
