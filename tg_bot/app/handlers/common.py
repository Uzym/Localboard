from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.config import bc

async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(bc.COMMANDS['start']['message'])

async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(bc.COMMANDS['cancel']['message'])

async def help_handler(message: types.Message, state: FSMContext):
    await message.reply(bc.COMMANDS['help']['message'], parse_mode="HTML")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start", state='*')
    dp.register_message_handler(help_handler, commands="help", state='*')
    dp.register_message_handler(cancel_handler, commands="cancel", state='*')
