from aiogram import Router, types
from aiogram.filters import Command, Text, or_f, and_f
from aiogram.fsm.context import FSMContext
from typing import Optional
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from aiogram import F

from app.config import config
from app.request_handler import rh
from app.s3handler import s3_handler

class OrderForm(StatesGroup):
    order_forming = State()

class ConsumeCallback(CallbackData, prefix="consume"):
    action: str
    value: Optional[int]
    extra_value: Optional[int]

orders = {}

router = Router()

@router.message(or_f(
    Command(commands=[config.commands.collect_order.command]),
    Text(text=config.commands.collect_order.text_eq)
))
async def collect_offer_start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(OrderForm.order_forming)
    await state.set_data({})
    await message.answer(text=config.commands.collect_order.message, reply_markup=config.collect_order_manage())
    await list_offers_handler(message)

@router.message(
    and_f(
        or_f(
            Command(commands=[config.commands.list_offers.command]),
            Text(text=config.commands.list_offers.text_eq)
        ),
        OrderForm.order_forming
    )
)
async def list_offers_handler(message: types.Message):
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

@router.callback_query(
    and_f(
        OrderForm.order_forming,
        ConsumeCallback.filter(F.action == config.callback.order_add.cb_data)
    )
)
async def order_add_callback(call: types.CallbackQuery, state: FSMContext, callback_data: ConsumeCallback):
    data = await state.get_data()
    if str(callback_data.value) in data.keys():
        data[str(callback_data.value)] += int(callback_data.extra_value)
    else:
        data[str(callback_data.value)] = int(callback_data.extra_value)
    if data[str(callback_data.value)] < 1:
        del data[str(callback_data.value)]
    await state.set_data(data)
    await call.answer(config.callback.order_add.good_message)
    

@router.callback_query(
    ConsumeCallback.filter(F.action == config.callback.offer_open.cb_data)
)
async def open_offer_callback(call: types.CallbackQuery, callback_data: ConsumeCallback):
    res = await config.loop.create_task(rh.get_offer(callback_data.value))
    if res["ans"]:
        if res["offer"]["photo"] == None:
            await call.message.answer(
                text=config.offer_message_text(
                    long=True,
                    title=res["offer"]["title"],
                    cost=res["offer"]["cost"],
                    desc=res["offer"]["desc"],
                    hidden=res["offer"]["hidden"],
                    quantity=res["offer"]["quantity"]
                ),
                reply_markup=config.offer_consume_markup(ConsumeCallback, int(res["offer"]["offer_id"]), 1)
            )
        else:
            photo_bytes = s3_handler.load(file_name=res["offer"]["photo"])
            photo_file = types.BufferedInputFile(
                photo_bytes, res["offer"]["photo"].split("images/")[1])
            await call.message.answer_photo(
                photo=photo_file,
                caption=config.offer_message_text(
                    long=True,
                    title=res["offer"]["title"],
                    cost=res["offer"]["cost"],
                    desc=res["offer"]["desc"],
                    hidden=res["offer"]["hidden"],
                    quantity=res["offer"]["quantity"]
                ),
                reply_markup=config.offer_consume_markup(ConsumeCallback, int(res["offer"]["offer_id"]), 1)
            )
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()

@router.callback_query(
    and_f(
        OrderForm.order_forming,
        ConsumeCallback.filter(F.action == config.callback.offer_open_incr.cb_data)
    )
)
async def open_offer_incr_callback(call: types.CallbackQuery, callback_data: ConsumeCallback):
    await call.message.edit_reply_markup(reply_markup=config.offer_consume_markup(ConsumeCallback, int(callback_data.value), int(callback_data.extra_value)))
    await call.answer()

@router.message(
    and_f(
        or_f(
            Command(commands=[config.commands.finish_order.command]),
            Text(text=config.commands.finish_order.text_eq)
        ),
        OrderForm.order_forming
    )
)
async def finish_offer_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    offer_id = 0
    titles = []
    costs = []
    nums = []

    for offer_id, num in data.items():
        res = await config.loop.create_task(rh.get_offer(offer_id=offer_id))
        if res["ans"]:
            offer_id = offer_id
            titles.append(res["offer"]["title"])
            costs.append(res["offer"]["cost"])
            if num > int(res["offer"]["quantity"]):
                nums.append(int(res["offer"]["quantity"]))
            else:
                nums.append(num)
        else:
            await message.answer(config.bad_message)
            return
    if len(data) > 0:
        await message.answer(
            text=config.collect_order_text(titles, nums, costs),
            reply_markup=config.collect_order_markup(ConsumeCallback, offer_id)
        )
    else:
        await message.answer(
            text=config.collect_order_text(titles, nums, costs)
        )
    

@router.callback_query(
    and_f(
        ConsumeCallback.filter(F.action == config.callback.order_consume.cb_data),
        OrderForm.order_forming
    )
)
async def order_consume_callback(call: types.CallbackQuery, callback_data: ConsumeCallback, state: FSMContext):
    offer = await config.loop.create_task(rh.get_offer(callback_data.value))
    if not(offer["ans"]):
        await call.message.answer(text=config.bad_message)
        return
    
    res = await config.loop.create_task(rh.get_user_chat_id(offer["offer"]["user_id"]))
    if res["ans"]:
        orders[str(call.id)] = await state.get_data()
        await config.bot.send_message(
            chat_id=res["chat_id"], 
            text=call.message.text,
            reply_markup=config.offer_consume_message_markup(call.from_user.id, ConsumeCallback, call.id)
        )
        await call.message.answer(text=config.callback.order_consume.good_message)
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()
    await state.clear()
    await call.message.edit_reply_markup(None)

@router.callback_query(
    ConsumeCallback.filter(F.action == config.callback.order_confirm.cb_data)
)
async def order_confirm_callback(call: types.CallbackQuery, callback_data: ConsumeCallback):
    order: dict = orders[str(callback_data.value)]
    for item in order.items():
        res = await config.loop.create_task(rh.decr_quantity_offer(item[0], item[1]))
        if not(res["ans"]):
            call.message.answer(config.bad_message)
            return
    del orders[str(callback_data.value)]
    await call.message.edit_reply_markup(None)
    await call.message.answer(config.callback.order_confirm.good_message)
    await call.answer()

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
