from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from app.config import bc
from app.request_handler import rh

class OfferManageForm(StatesGroup):
    WAIT_OFFER_MANAGE = State()
    WAIT_OFFER_TITLE = State()
    WAIT_OFFER_DESC = State()
    WAIT_OFFER_COST = State()
    WAIT_OFFER_OPEN = State()

class CallbackOfferManage(CallbackData, prefix="manage"):
    action: str
    offer_id: int

async def my_offer_handler(message: types.Message, state: FSMContext):
    res = await rh.my_offers(message.chat.id)
    if res["ans"]:
        await state.finish()
        await message.answer(text=bc.COMMANDS["my_offers"]["message"], reply_markup=bc.offer_choose(res["offers"], "offer_manage"))
        await state.set_state(OfferManageForm.WAIT_OFFER_OPEN.state)
    else:   
        await message.answer(text=bc.BAD_MESSAGE)

async def open_offer_callback(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data.rsplit(None, 2)
    if callback_data[0] == "offer_manage":
        res = await rh.get_offer(callback_data[1])
        if res["ans"]:
            await callback_query.message.answer(
                text=bc.offer_format_long(
                    title=res["offer"]["title"],
                    cost=res["offer"]["cost"],
                    hidden=res["offer"]["hidden"],
                    desc=res["offer"]["desc"]
                ),
                reply_markup=bc.offer_inline_manage(
                    res["offer"]["offer_id"]
                ),
                parse_mode="HTML"
            )
            await state.set_state(OfferManageForm.WAIT_OFFER_MANAGE.state)
        else:
            await callback_query.message.answer(text=bc.BAD_MESSAGE)

async def new_offer_handler(message: types.Message, state: FSMContext):
    res = await rh.new_offer(str(message.chat.id))
    if res["ans"]:
        await state.finish()
        await message.answer(
            text=bc.offer_format_long(
                title=res["offer"]["offer"]["title"],
                cost=res["offer"]["offer"]["cost"],
                hidden=res["offer"]["offer"]["hidden"],
                desc=res["offer"]["offer"]["desc"]
            ),
            reply_markup=bc.offer_inline_manage(
                res["offer"]["offer"]["offer_id"]
            ),
            parse_mode="HTML"
        )
        await state.set_state(OfferManageForm.WAIT_OFFER_MANAGE.state)
    else:
        await message.answer(
            text=bc.COMMANDS["new_offer"]["bad_message"]
        )

async def manage_offer_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await rh.add_title_offer(offer_id=data["offer_id"], data=message.text)
    if res["ans"]:
        await message.answer(text=bc.INLINE_REQUSESTS["offer_add_title"]["good_message"])
        await state.set_state(OfferManageForm.WAIT_OFFER_MANAGE.state)
    else:
        await message.answer(text=bc.BAD_MESSAGE)

async def manage_offer_desc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await rh.add_desc_offer(offer_id=data["offer_id"], data=message.text)
    if res["ans"]:
        await message.answer(text=bc.INLINE_REQUSESTS["offer_add_desc"]["good_message"])
        await state.set_state(OfferManageForm.WAIT_OFFER_MANAGE.state)
    else:
        await message.answer(text=bc.BAD_MESSAGE)

async def manage_offer_cost(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res = await rh.add_cost_offer(offer_id=data["offer_id"], data=message.text)
    if res["ans"]:
        await message.answer(text=bc.INLINE_REQUSESTS["offer_add_cost"]["good_message"])
        await state.set_state(OfferManageForm.WAIT_OFFER_MANAGE.state)
    else:
        await message.answer(text=bc.BAD_MESSAGE)

async def manage_offer_callback(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data.rsplit(None, 2)
    if callback_data[0] == "offer_add_title":
        await callback_query.answer(
            text=bc.INLINE_REQUSESTS["offer_add_title"]["message"]
        )
        await state.set_state(OfferManageForm.WAIT_OFFER_TITLE.state)
        await state.set_data({"offer_id": callback_data[1]})
    elif callback_data[0] == "offer_add_desc":
        await callback_query.answer(
            text=bc.INLINE_REQUSESTS["offer_add_desc"]["message"]
        )
        await state.set_state(OfferManageForm.WAIT_OFFER_DESC.state)
        await state.set_data({"offer_id": callback_data[1]})
    elif callback_data[0] == "offer_add_cost":
        await callback_query.answer(
            text=bc.INLINE_REQUSESTS["offer_add_cost"]["message"]
        )
        await state.set_state(OfferManageForm.WAIT_OFFER_COST.state)
        await state.set_data({"offer_id": callback_data[1]})
    elif callback_data[0] == "offer_publish":
        res = await rh.publish_offer(callback_data[1])
        if res["ans"]:
            await callback_query.answer(
                text=bc.INLINE_REQUSESTS["offer_publish"]["message"]
            )
        else:
            await callback_query.answer(
                text=bc.BAD_MESSAGE
            )
    elif callback_data[0] == "offer_hidden":
        res = await rh.hidden_offer(callback_data[1])
        if res["ans"]:
            await callback_query.answer(
                text=bc.INLINE_REQUSESTS["offer_hidden"]["message"]
            )
        else:
            await callback_query.answer(
                text=bc.BAD_MESSAGE
            )

def register_handlers_manage_offers(dp: Dispatcher):
    dp.register_message_handler(new_offer_handler, commands="new_offer", state='*')
    dp.register_message_handler(my_offer_handler, commands="my_offers", state='*')
    dp.register_callback_query_handler(open_offer_callback, state=OfferManageForm.WAIT_OFFER_OPEN)
    dp.register_callback_query_handler(manage_offer_callback, state=OfferManageForm.all_states)
    dp.register_message_handler(manage_offer_title, state=OfferManageForm.WAIT_OFFER_TITLE)
    dp.register_message_handler(manage_offer_desc, state=OfferManageForm.WAIT_OFFER_DESC)
    dp.register_message_handler(manage_offer_cost, state=OfferManageForm.WAIT_OFFER_COST)
