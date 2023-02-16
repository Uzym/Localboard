from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import os

from request_handler import RequestHandler
from config import MESSAGES

rh = RequestHandler(os.environ.get("apidemon_url"))

bot = Bot(token=os.environ.get("TOKEN"), parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(state='*', commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(MESSAGES['start'])

@dp.message_handler(state='*', commands=['test'])
async def start_handler(message: types.Message):
    res = await rh.test()
    await message.reply(res)

# user
@dp.message_handler(state='*', commands=['reg_user'])
async def reg_user_handler(message: types.Message):
    await message.reply(MESSAGES['start'])

@dp.message_handler(state='*', commands=['change_desc_user']) # в инлайн
async def add_desc_user_handler(message: types.Message):
    pass

@dp.message_handler(state='*', commands=['change_name_user']) # в инлайн
async def change_name_user_handler(message: types.Message):
    pass

# offer manage

@dp.message_handler(state='*', commands=['my_offer']) # выводится краткий список по офферам пользователя с инлайнами на которые открываются офферы
async def my_offer_handler(message: types.Message):
    pass

@dp.message_handler(state='*', commands=['new_offer']) # создаётся болванка с инлайн кнопками добавить описание, название и т.д.
async def new_offer_handler(message: types.Message):
    pass



# создать обработчик инлайнов для удаления и изменения параметров

# location

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
