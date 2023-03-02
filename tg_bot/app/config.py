import emoji
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram import Bot
import os
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import asyncio


class Config:
    manage_chat = ("-1001837532813", )

    loop = asyncio.new_event_loop()
    bot = Bot(os.environ.get("TOKEN"))

    num_offer_in_list = 12
    string_size_in_list = 2

    bad_message = "Произошла ошибка"

    class commands:
        class start:
            admin_command = False
            command = "start"
            text_eq = "Начать"
            desc = "входная точка в функционал бота"
            message = "Здравствуйте! Для создания заказа напишите /collect_order или используйте встренную клавиатуру"

        class help:
            admin_command = False
            command = "help"
            text_eq = "Помощь"
            desc = "помощь"
            message = "Приветствую! Я - телеграм бот компании, которая занимается продажей красивых и свежих голландских тюльпанов на 8 марта!\n" \
                "Наша компания гордится тем, что предлагает только самые качественные цветы, выращенные в Голландии. Мы уверены, что наш выбор ярких и красивых тюльпанов подарит радость и улыбки вашим любимым женщинам в этот особенный день!\n" \
                "Чтобы заказать наши цветы, просто выберите из нашего каталога тюльпанов те, которые вам нравятся, и укажите желаемое количество и адрес доставки. Мы гарантируем своевременную доставку и высокий уровень обслуживания для наших клиентов.\n"\
                "Не упустите возможность порадовать своих любимых женщин на 8 марта и сделать этот день незабываемым с помощью наших красивых голландских тюльпанов! Спасибо, что выбрали нашу компанию."

        class cancel:
            admin_command = False
            command = "cancel"
            text_eq = "Отменить"
            desc = "отменить действие"
            message = "Действие отменено"

        class collect_order:
            admin_command = False
            command = "collect_order"
            text_eq = "Создать новый заказ"
            desc = "создать новый заказ"
            message = "Выберите товары, а когда захотите закончить выбор используйте команду /finish_order или просто напишите Закончить выбор"

        class finish_order:
            admin_command = False
            command = "finish_order"
            text_eq = "Закончить выбор" 
            desc = "закончить выбор заказа"
            message = "Выберите товары, а когда захотите закончить выбор используйте команду /finish_order или просто напишите Закончить выбор"

        class list_offers:
            admin_command = False
            command = "list_offers"
            text_eq = "Открыть список товаров"
            desc = "открыть список"
            message = "Нажмите на кнопку товара чтобы получить более подробную информацию по нему и добавить в заказ"

        class new_offer:
            admin_command = True
            command = "new_offer"
            text_eq = "Создать объявление"
            desc = "создать объявление"
            message = "Создано следующее объявление"

        class my_offers:
            admin_command = True
            command = "my_offers"
            text_eq = "Мои объявления"
            desc = "вывести все ваши объявления"
            message = "Вам принадлежат следующие объявления:"

    def consume_buttons(self) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text=self.commands.start.text_eq)
        builder.button(text=self.commands.help.text_eq)
        builder.button(text=self.commands.cancel.text_eq)
        # builder.button(text=self.commands.list_offers.text_eq)
        builder.button(text=self.commands.collect_order.text_eq)
        builder.adjust(3, 1)
        return builder.as_markup(resize_keyboard=True)

    class callback:
        
        class offer_decr:
            cb_data = "offer_decr"
            text = "Уменьшить количество товара"
            message = "Введите число на которое хотите уменьшить"
            good_message = "Количество изменено"

        class offer_desc:
            cb_data = "offer_desc"
            text = "изменить описание"
            message = "Введите описание"
            good_message = "Описание изменено"

        class offer_title:
            cb_data = "offer_title"
            text = "изменить название"
            message = "Введите название"
            good_message = "Название изменено"

        class offer_cost:
            cb_data = "offer_cost"
            text = "изменить цену"
            message = "Введите цену"
            good_message = "Цена изменена"

        class offer_quantity:
            cb_data = "offer_quantity"
            text = "изменить количество объявлений"
            message = "Введите количество"
            good_message = "Количество изменено"

        class offer_delete:
            cb_data = "offer_delete"
            text = "удалить"
            message = "Вы уверены?"
            good_message = "Удалено"

        class offer_publish:
            cb_data = "offer_publish"
            text = "опубликовать"
            good_message = "Опубликовано"

        class offer_hidden:
            cb_data = "offer_hidden"
            text = "скрыть"
            good_message = "Скрыто"
        
        class offer_photo:
            cb_data = "offer_photo"
            text = "изменить фото"
            message = "Отправьте фото"
            good_message = "Фото изменено"

        class offer_open:
            cb_data = "offer_open"
            text = "открыть"
            good_message = "Открыто"

        class next_list:
            cb_data = "offer_list"
            text = "->"
            good_message = "Следующая страница"

        class prev_list:
            cb_data = "offer_list"
            text = "<-"
            good_message = "Предыдущая страница"
        
        class order_add:
            cb_data = "order_add"
            text = "{} {} единиц товара"
            good_message = "Добавленно"

        class order_consume:
            cb_data = "order_consume"
            text = "Приобрести"
            good_message = "Скоро продавец свяжется с вами"
        
        class order_confirm:
            cb_data = "order_confirm"
            text = "Подтвердить"
            good_message = "Подтверждено"

        class offer_open_incr:
            cb_data = "offer_open_incr"
            text = "+{}"

    def offer_message_text(self, long: bool, title: str, cost = None, desc = None, hidden = None, quantity = None) -> str:
        msg = ""
        if long:
            msg = f"{title}, {cost}\n{desc}\n"
            if quantity != 0 and quantity != None:
                msg += f"Осталось: {quantity} штук\n"
            if hidden == 1:
                msg += "Скрыто"
        else:
            msg = f"{title}, {cost}"
        return msg
    
    def offer_choose_markup(self, offers: list, cb, list_start: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for offer in offers:
            builder.button(
                text=self.offer_message_text(
                    long=False,
                    title=offer["title"],
                    cost=offer["cost"],
                ),
                callback_data=cb(
                    action=self.callback.offer_open.cb_data, value=int(offer["offer_id"])
                ).pack()
            )
        
        if list_start > 0:
            builder.button(
                text=self.callback.prev_list.text,
                callback_data=cb(
                    action=self.callback.prev_list.cb_data,
                    value=int(list_start)-int(self.num_offer_in_list)
                ).pack()
            )

        if len(offers) > 0:
            builder.button(
                text=self.callback.next_list.text,
                callback_data=cb(
                    action=self.callback.next_list.cb_data,
                    value=int(list_start)+int(self.num_offer_in_list)
                ).pack()
            )
        
        string_size = [self.string_size_in_list for i in range(len(offers) // self.string_size_in_list)]
        if len(offers) % self.string_size_in_list != 0:
            string_size.append(len(offers) % self.string_size_in_list)
        builder.adjust(*string_size, 2)
        
        return builder.as_markup()
    
    def offer_manage_markup(self, offer_id: int, cb) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self.callback.offer_title.text,
            callback_data=cb(
                action=self.callback.offer_title.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_cost.text,
            callback_data=cb(
                action=self.callback.offer_cost.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_desc.text,
            callback_data=cb(
                action=self.callback.offer_desc.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_quantity.text,
            callback_data=cb(
                action=self.callback.offer_quantity.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_photo.text,
            callback_data=cb(
                action=self.callback.offer_photo.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_hidden.text,
            callback_data=cb(
                action=self.callback.offer_hidden.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_publish.text,
            callback_data=cb(
                action=self.callback.offer_publish.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.button(
            text=self.callback.offer_delete.text,
            callback_data=cb(
                action=self.callback.offer_delete.cb_data, 
                value=offer_id
            ).pack()
        )
        builder.adjust(2, 2, 1, 2, 1)
        
        return builder.as_markup()
    
    def offer_consume_message_markup(self, user_id: str, cb, order_id: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="Покупатель",
            url=f"tg://user?id={user_id}"
        )
        builder.button(
            text=self.callback.order_confirm.text,
            callback_data=cb(action=self.callback.order_confirm.cb_data, value=order_id).pack()
        )
        builder.adjust(2)
        return builder.as_markup()
    
    def offer_consume_markup(self, cb, offer_id, num: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="-1",
            callback_data=cb(action=self.callback.offer_open_incr.cb_data, value=offer_id, extra_value=num-1).pack()
        )
        builder.button(
            text="0",
            callback_data=cb(action=self.callback.offer_open_incr.cb_data, value=offer_id, extra_value=0).pack()
        )
        builder.button(
            text="+1",
            callback_data=cb(action=self.callback.offer_open_incr.cb_data, value=offer_id, extra_value=num+1).pack()
        )
        if num >= 0:
            builder.button(
                text=self.callback.order_add.text.format("Добавить к заказу", num),
                callback_data=cb(action=self.callback.order_add.cb_data, value=offer_id, extra_value=num).pack()
            )
        else:
            builder.button(
                text=self.callback.order_add.text.format("Убрать из заказа", abs(num)),
                callback_data=cb(action=self.callback.order_add.cb_data, value=offer_id, extra_value=num).pack()
            )
        builder.adjust(3, 1)
        return builder.as_markup()
    
    def collect_order_text(self, titles, nums, costs) -> str:
        text = "Заказ:\n"
        price = 0
        for idx, title in enumerate(titles):
            cost = int(costs[idx])*int(nums[idx])
            price += cost
            text += f"{idx + 1}) {title}, {nums[idx]} шт. Стоимость {costs[idx]} * {nums[idx]} = {cost} руб.\n"
        text += f"Итого: {price} руб."
        return text
    
    def collect_order_markup(self, cb, offer_id) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self.callback.order_consume.text,
            callback_data=cb(
                action=self.callback.order_consume.cb_data,
                value=offer_id
            ).pack()
        )
        return builder.as_markup()

    def collect_order_manage(self) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text=self.commands.list_offers.text_eq)
        builder.button(text=self.commands.finish_order.text_eq)
        builder.button(text=self.commands.collect_order.text_eq)
        builder.button(text=self.commands.cancel.text_eq)
        builder.adjust(1, 1, 2)
        return builder.as_markup(resize_keyboard=True)


config = Config()
