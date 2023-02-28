from aiogram import Router, types
from aiogram.filters import Command, Text, or_f
from aiogram.fsm.context import FSMContext
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from app.config import config
from app.filters import ManageChatFilter


class ManageCallback(CallbackData, prefix="consume"):
    action: str
    value: Optional[int]

router = Router()
router.message.filter(
    ManageChatFilter()
)

@router.message(or_f(
    Command(commands=[config.commands.my_offers.command]),
    Text(text=config.commands.my_offers.text_eq)
))
async def my_offers_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        config.commands.my_offers.message
    )

