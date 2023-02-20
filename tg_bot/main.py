from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

from request_handler import RequestHandler
from config import BotConfig

botconfig = BotConfig()

rh = RequestHandler(os.environ.get("apidemon_url"))

bot = Bot(token=os.environ.get("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# main

@dp.message_handler(state='*', commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(botconfig.COMMANDS['start']['message'])

@dp.message_handler(state='*', commands=['help'])
async def help_handler(message: types.Message):
    await message.reply(botconfig.COMMANDS['help']['message'], parse_mode="HTML")

@dp.message_handler(state='*', commands=['test'])
async def test_handler(message: types.Message):
    inline_choose = InlineKeyboardMarkup().add(InlineKeyboardButton(text="test", callback_data="test 3"))
    res = await rh.test()
    await message.reply(res, reply_markup=inline_choose)

@dp.callback_query_handler()
async def test2_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.message.chat.id, text=str(callback.data.rsplit(None, 2)))

# user

# @dp.message_handler(state='*', commands=['reg_user'])
# async def reg_user_handler(message: types.Message):
#     await message.reply(MESSAGES['start'])

@dp.message_handler(state='*', commands=['get_me']) # нужно ли?
async def add_desc_user_handler(message: types.Message):
    pass

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

    res = await rh.new_offer(str(message.chat.id))
    await message.reply(text=res + str(message.chat.id), reply_markup=botconfig.offer_inline_manage(0))

# offer use

@dp.message_handler(state='*', commands=['find_offer'])
async def new_offer_handler(message: types.Message):
    pass

@dp.message_handler(state='*', commands=['list_offer']) # выводится краткий список по офферам
async def new_offer_handler(message: types.Message):
    pass


# создать обработчик инлайнов для удаления и изменения параметров

# locations # их будем делать позже

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
