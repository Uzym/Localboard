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
            message = "Здравствуйте! Для поиска объявлений напишите /list_offer"

        class help:
            admin_command = False
            command = "help"
            text_eq = "Помощь"
            desc = "помощь"
            message = "Для поиска объявлений напишите /list_offer"

        class cancel:
            admin_command = False
            command = "cancel"
            text_eq = "Отменить"
            desc = "отменить действие"
            message = "Действие отменено"

        class collect_order:
            admin_command = False
            command = "collect_order"
            text_eq = "Собрать букет самому"
            desc = "собрать букет"
            message = "Нажмите на кнопку товара чтобы получить более подробную информацию по нему и добавить в заказ"

        class list_offers:
            admin_command = False
            command = "list_offers"
            text_eq = "Купить готовый букет"
            desc = "вывести список доступных букетов"
            message = "Просто нажмите на заинтересовавший вас товар для получения более подробной информации"

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
        builder.button(text=self.commands.list_offers.text_eq)
        builder.adjust(3, 1)
        return builder.as_markup(resize_keyboard=True)

    class callback:
        class offer_consume:
            cb_data = "offer_consume"
            text = "Приобрести"
            message = "Скоро продавец свяжется с вами"
        
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
        builder.adjust(2, 2, 2, 1)
        
        return builder.as_markup()
    
    def offer_consume_markup(self, offer_id: int, user_id: int, cb) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self.callback.offer_consume.text,
            callback_data=cb(
                action=self.callback.offer_consume.cb_data, 
                value=offer_id,
                extra_value=user_id
            ).pack()
        )
        return builder.as_markup()
    
    def offer_consume_message_text(self, offer):
        text = "Отклик на объявление\n"
        text += self.offer_message_text(
            long=True,
            title=offer["title"],
            cost=offer["cost"],
            desc=offer["desc"],
            hidden=offer["hidden"],
            quantity=offer["quantity"]
        )
        return text
    
    def offer_consume_message_markup(self, user_id: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="Покупатель",
            url=f"tg://user?id={user_id}"
        )
        return builder.as_markup()
    

config = Config()
