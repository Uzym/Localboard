from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

from request_handler import RequestHandler
from config import BotConfig
from state import BotStates

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
    inline_choose = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="test", callback_data="test 3"))
    res = await rh.test()
    await message.reply(res, reply_markup=inline_choose)

# user

# @dp.message_handler(state='*', commands=['reg_user'])
# async def reg_user_handler(message: types.Message):
#     await message.reply(MESSAGES['start'])


@dp.message_handler(state='*', commands=['get_me'])  # нужно ли?
async def add_desc_user_handler(message: types.Message):
    pass


@dp.message_handler(state='*', commands=['change_desc_user'])  # в инлайн
async def add_desc_user_handler(message: types.Message):
    pass


@dp.message_handler(state='*', commands=['change_name_user'])  # в инлайн
async def change_name_user_handler(message: types.Message):
    pass

# offer manage


# выводится краткий список по офферам пользователя с инлайнами на которые открываются офферы
@dp.message_handler(state='*', commands=['my_offer'])
async def my_offer_handler(message: types.Message):
    pass


# создаётся болванка с инлайн кнопками добавить описание, название и т.д.
@dp.message_handler(state='*', commands=['new_offer'])
async def new_offer_handler(message: types.Message):

    res = await rh.new_offer(str(message.chat.id))
    if res["ans"]:
        await message.reply(
            text=botconfig.offer_format_long(
                title=res["offer"]["offer"]["title"],
                cost=res["offer"]["offer"]["title"],
                hidden=res["offer"]["offer"]["hidden"],
                desc=res["offer"]["offer"]["desc"]
            ),
            reply_markup=botconfig.offer_inline_manage(
                res["offer"]["offer"]["offer_id"]
            ),
            parse_mode="HTML"
        )

# offer use


@dp.message_handler(state='*', commands=['find_offer'])
async def new_offer_handler(message: types.Message):
    pass


# выводится краткий список по офферам
@dp.message_handler(state='*', commands=['list_offer'])
async def new_offer_handler(message: types.Message):
    pass

# callback


@dp.callback_query_handler()
async def callback_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    command = callback.data.rsplit(None, 2)
    if command[0] == "offer_add_title":
        await bot.send_message(
            callback.message.chat.id,
            text=botconfig.INLINE_REQUSESTS["offer_add_title"]["message"]
        )
        await dp.current_state(user=callback.message.from_user.id).set_state(BotStates.WAIT_OFFER_TITLE)
    elif command[0] == "offer_add_desc":
        await bot.send_message(
            callback.message.chat.id,
            text=botconfig.INLINE_REQUSESTS["offer_add_desc"]["message"]
        )
        await dp.current_state(user=callback.message.from_user.id).set_state(BotStates.WAIT_OFFER_TITLE)
    elif command[0] == "offer_add_cost":
        await bot.send_message(
            callback.message.chat.id,
            text=botconfig.INLINE_REQUSESTS["offer_add_cost"]["message"]
        )
        await dp.current_state(user=callback.message.from_user.id).set_state(BotStates.WAIT_OFFER_TITLE)
    elif command[0] == "offer_publish":
        await bot.send_message(
            callback.message.chat.id,
            text=botconfig.INLINE_REQUSESTS["offer_publish"]["message"]
        )
    elif command[0] == "offer_hidden":
        await bot.send_message(
            callback.message.chat.id,
            text=botconfig.INLINE_REQUSESTS["offer_hidden"]["message"]
        )

# создать обработчик инлайнов для удаления и изменения параметров

# locations # их будем делать позже

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
