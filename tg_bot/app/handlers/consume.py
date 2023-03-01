from aiogram import Router, types
from aiogram.filters import Command, Text, or_f
from aiogram.fsm.context import FSMContext
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram import F

from app.config import config
from app.request_handler import rh


class ConsumeCallback(CallbackData, prefix="consume"):
    action: str
    value: Optional[int]
    extra_value: Optional[int]


router = Router()

@router.message(or_f(
    Command(commands=[config.commands.collect_order.command]),
    Text(text=config.commands.collect_order.text_eq)
))
async def collect_offer_start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    message.answer(
        text=config.commands.collect_order.message
    )

@router.callback_query(
    ConsumeCallback.filter(F.action == config.callback.offer_open.cb_data)
)
async def open_offer_callback(call: types.CallbackQuery, callback_data: ConsumeCallback):
    res = await config.loop.create_task(rh.get_offer(callback_data.value))
    if res["ans"]:
        await call.message.answer(
            text=config.offer_message_text(
                long=True,
                title=res["offer"]["title"],
                cost=res["offer"]["cost"],
                desc=res["offer"]["desc"],
                hidden=res["offer"]["hidden"],
                quantity=res["offer"]["quantity"]
            ),
            reply_markup=config.offer_consume_markup(int(res["offer"]["offer_id"]), int(res["offer"]["user_id"]), ConsumeCallback)
        )
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()

@router.callback_query(
    ConsumeCallback.filter(F.action == config.callback.offer_consume.cb_data)
)
async def offer_consume_callback(call: types.CallbackQuery, callback_data: ConsumeCallback):
    res = await config.loop.create_task(rh.get_user_chat_id(callback_data.extra_value))
    if res["ans"]:
        offer = await config.loop.create_task(rh.get_offer(callback_data.value))
        if offer["ans"]:
            await config.bot.send_message(
                chat_id=res["chat_id"],
                text=config.offer_consume_message_text(offer["offer"]),
                reply_markup=config.offer_consume_message_markup(str(call.from_user.id))
            )
        else:
            await call.message.answer(text=config.bad_message)
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()
    await call.message.edit_reply_markup(None)

@router.callback_query(
    ConsumeCallback.filter(F.action == config.callback.prev_list.cb_data)
)
async def list_offer_callback(call: types.CallbackQuery, callback_data: ConsumeCallback):
    res = await config.loop.create_task(rh.get_list_offers(
        chat_id="",
        use_chat_id=False,
        use_hidden=False,
        list_start=callback_data.value,
        list_end=int(callback_data.value)+config.num_offer_in_list
    ))
    if res["ans"]:
        await call.message.edit_reply_markup(reply_markup=config.offer_choose_markup(res["offers"], ConsumeCallback, int(callback_data.value)))
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()


@router.message(or_f(
    Command(commands=[config.commands.list_offers.command]),
    Text(text=config.commands.list_offers.text_eq)
))
async def list_offers_handler(message: types.Message, state: FSMContext):
    await state.clear()
    res = await config.loop.create_task(
        rh.get_list_offers(
            chat_id="",
            use_chat_id=False,
            use_hidden=False,
            list_start=0,
            list_end=config.num_offer_in_list
        )
    )

    if res["ans"]:
        await message.answer(
            text=config.commands.list_offers.message,
            reply_markup=config.offer_choose_markup(
                offers=res["offers"],
                cb=ConsumeCallback,
                list_start=0
            )
        )
    else:
        await message.answer(text=config.bad_message)
