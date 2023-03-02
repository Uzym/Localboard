import uuid
from aiogram import Router, types, F
from aiogram.filters import Command, Text, or_f, and_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from app.config import config
from app.request_handler import rh
from app.filters import ManageChatFilter
from app.s3handler import s3_handler


class OfferManageForm(StatesGroup):
    wait_title = State()
    wait_desc = State()
    wait_cost = State()
    wait_quantity = State()
    wait_delete = State()
    wait_photo = State()


class ManageCallback(CallbackData, prefix="manage"):
    action: str
    value: Optional[int]


router = Router()
router.message.filter(
    ManageChatFilter()
)


@router.callback_query(
    ManageCallback.filter(F.action == config.callback.offer_open.cb_data)
)
async def open_offer_callback(call: types.CallbackQuery, callback_data: ManageCallback):
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
                reply_markup=config.offer_manage_markup(
                    int(callback_data.value), ManageCallback)
            )
        else:
            photo_bytes = s3_handler.load(res["offer"]["photo"])
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
                reply_markup=config.offer_manage_markup(
                    int(callback_data.value), ManageCallback)
            )
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()


@router.callback_query(
    ManageCallback.filter(F.action == config.callback.prev_list.cb_data)
)
async def list_offer_callback(call: types.CallbackQuery, callback_data: ManageCallback):
    res = await config.loop.create_task(rh.get_list_offers(
        chat_id=str(call.message.chat.id),
        use_chat_id=True,
        use_hidden=True,
        list_start=callback_data.value,
        list_end=int(callback_data.value)+config.num_offer_in_list
    ))
    if res["ans"]:
        await call.message.edit_reply_markup(reply_markup=config.offer_choose_markup(res["offers"], ManageCallback, int(callback_data.value)))
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()


@router.message(or_f(
    Command(commands=[config.commands.my_offers.command]),
    Text(text=config.commands.my_offers.text_eq)
))
async def my_offers_handler(message: types.Message, state: FSMContext):
    res = await config.loop.create_task(rh.get_list_offers(
        chat_id=str(message.chat.id),
        use_chat_id=True,
        use_hidden=True,
        list_start=0,
        list_end=config.num_offer_in_list
    ))

    if res["ans"]:
        await message.answer(
            text=config.commands.my_offers.message,
            reply_markup=config.offer_choose_markup(
                offers=res["offers"],
                cb=ManageCallback,
                list_start=0
            )
        )
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.message(or_f(
    Command(commands=[config.commands.new_offer.command]),
    Text(text=config.commands.new_offer.text_eq)
))
async def new_offer_handler(message: types.Message, state: FSMContext):
    res = await config.loop.create_task(rh.new_offer(str(message.chat.id)))
    if res["ans"]:
        await message.answer(
            text=config.offer_message_text(
                long=True,
                title=res["offer"]["title"],
                cost=res["offer"]["cost"],
                desc=res["offer"]["desc"],
                hidden=res["offer"]["hidden"],
                quantity=res["offer"]["quantity"]
            ),
            reply_markup=config.offer_manage_markup(
                int(res["offer"]["offer_id"]), ManageCallback)
        )
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_title.cb_data))
async def offer_title_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    await call.answer(text=config.callback.offer_title.message)
    await state.set_data({"offer_id": callback_data.value})
    await state.set_state(OfferManageForm.wait_title)


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_cost.cb_data))
async def offer_cost_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    await call.answer(text=config.callback.offer_cost.message)
    await state.set_data({"offer_id": callback_data.value})
    await state.set_state(OfferManageForm.wait_cost)


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_desc.cb_data))
async def offer_desc_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    await call.answer(text=config.callback.offer_desc.message)
    await state.set_data({"offer_id": callback_data.value})
    await state.set_state(OfferManageForm.wait_desc)


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_quantity.cb_data))
async def offer_quantity_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    await call.answer(text=config.callback.offer_quantity.message)
    await state.set_data({"offer_id": callback_data.value})
    await state.set_state(OfferManageForm.wait_quantity)


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_photo.cb_data))
async def offer_photo_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    await call.answer(text=config.callback.offer_photo.message)
    await state.set_data({"offer_id": callback_data.value})
    await state.set_state(OfferManageForm.wait_photo)


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_delete.cb_data))
async def offer_delete_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    await call.answer(text=config.callback.offer_delete.message)
    await state.set_data({"offer_id": callback_data.value})
    await state.set_state(OfferManageForm.wait_delete)


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_publish.cb_data))
async def offer_publish_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    res = await rh.publish_offer(callback_data.value)
    if res["ans"]:
        await call.message.answer(text=config.callback.offer_publish.good_message)
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()


@router.callback_query(ManageCallback.filter(F.action == config.callback.offer_hidden.cb_data))
async def offer_hidden_callback(call: types.CallbackQuery, callback_data: ManageCallback, state: FSMContext):
    res = await rh.hidden_offer(callback_data.value)
    if res["ans"]:
        await call.message.answer(text=config.callback.offer_hidden.good_message)
    else:
        await call.message.answer(text=config.bad_message)
    await call.answer()


@router.message(and_f(F.text, OfferManageForm.wait_title))
async def offer_title_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await config.loop.create_task(rh.add_title_offer(offer_id=data["offer_id"], data=message.text))
    if res["ans"]:
        await message.answer(text=config.callback.offer_title.good_message)
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.message(and_f(F.text.regexp("\d+"), OfferManageForm.wait_cost))
async def offer_cost_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await config.loop.create_task(rh.add_cost_offer(offer_id=data["offer_id"], data=message.text))
    if res["ans"]:
        await message.answer(text=config.callback.offer_cost.good_message)
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.message(and_f(F.text, OfferManageForm.wait_desc))
async def offer_desc_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await config.loop.create_task(rh.add_desc_offer(offer_id=data["offer_id"], data=message.text))
    if res["ans"]:
        await message.answer(text=config.callback.offer_desc.good_message)
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.message(and_f(F.text.regexp("\d+"), OfferManageForm.wait_quantity))
async def offer_quantity_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await config.loop.create_task(rh.add_quantity_offer(offer_id=data["offer_id"], data=message.text))
    if res["ans"]:
        await message.answer(text=config.callback.offer_quantity.good_message)
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.message(and_f(F.text == "Да", OfferManageForm.wait_delete))
async def offer_delete_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await config.loop.create_task(rh.delete_offer(offer_id=data["offer_id"]))
    if res == 1:
        await message.answer(text=config.callback.offer_delete.good_message)
    else:
        await message.answer(text=config.bad_message)
    await state.clear()


@router.message(OfferManageForm.wait_photo)
async def offer_photo_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_info = await config.bot.get_file(message.photo[len(message.photo) - 1].file_id)
    photo = await config.bot.download_file(file_info.file_path)
    name = str(uuid.uuid4())
    file_path = 'images/' + name + '.' + \
        file_info.file_path.split('photos/')[1].split('.')[-1]
    s3_handler.save(file_path=file_path, content=photo.read())
    res = await config.loop.create_task(rh.add_photo_offer(offer_id=data["offer_id"], photo=file_path))
    if res["ans"]:
        await message.answer(text=config.callback.offer_photo.good_message)
    else:
        await message.answer(text=config.bad_message)
    await state.clear()
