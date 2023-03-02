from aiogram import Router, types
from aiogram.filters import Command, Text, or_f
from aiogram.fsm.context import FSMContext

from app.config import config

router = Router()

@router.message(or_f(
        Command(commands=[config.commands.start.command]), 
        Text(text=config.commands.start.text_eq)
    ))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        config.commands.start.message,
        reply_markup=config.consume_buttons()
    )

@router.message(or_f(
        Command(commands=[config.commands.cancel.command]), 
        Text(text=config.commands.cancel.text_eq)
    ))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        config.commands.cancel.message,
        reply_markup=config.consume_buttons()
    )

@router.message(or_f(
        Command(commands=[config.commands.help.command]), 
        Text(text=config.commands.help.text_eq)
    ))
async def help_handler(message: types.Message):
    await message.answer(
        config.commands.help.message
    )

