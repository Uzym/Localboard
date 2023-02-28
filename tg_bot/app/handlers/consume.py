from aiogram import Router, types
from aiogram.filters import Command, Text, or_f
from aiogram.fsm.context import FSMContext
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from app.config import config


class ConsumeCallback(CallbackData, prefix="consume"):
    action: str
    value: Optional[int]


router = Router()


@router.message(or_f(
    Command(commands=[config.commands.list_offers.command]),
    Text(text=config.commands.list_offers.text_eq)
))
async def list_offers_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        config.commands.list_offers.message
    )

