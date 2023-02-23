from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BotConfig:
    def __init__(self) -> None:
        self.BOTNAME = "Localboard"
        self.BAD_MESSAGE = "Произошла непредвиденная ошибка!"
        self.COMMANDS = {
            "start": {
                "desc": "входная точка в функционал бота",
                "message": ""
            },
            "cancel": {
                "desc": "отмена",
                "message": "Отменено"
            },
            "help": {
                "desc": "информация о боте и его функциях",
                "message": ""
            },
            "list_offer": {
                "desc": "вывести список доступных объявлений",
                "message": "" # тут нужна кнопка на смену локации
            },
            "new_offer": {
                "desc": "создать объявление",
                "message": "Создано следующее объявление",
                "bad_message": "Произошла непредвиденная ошибка!"
            },
            "my_offers": {
                "desc": "вывести все объявления которые принадлежат вам",
                "message": "Вам принадлежат следующие объявления:"
            },
            "get_me": {
                "desc": "посмотреть и изменить свой профиль"
            }
        }

        self.INLINE_REQUSESTS = {
            "offer_add_desc": {
                "text": "изменить описание",
                "message": "Введите описание",
                "good_message": "Описание изменено"
            },
            "offer_add_title": {
                "text": "изменить название",
                "message": "Введите название",
                "good_message": "Название изменено"
            },
            "offer_add_cost": {
                "text": "изменить цену",
                "message": "Введите цену",
                "good_message": "Цена изменена"
            },
            "offer_add_quantity": {
                "text": "изменить число предложений",
                "message": "Введите число",
                "good_message": "Количество изменено"
            },
            "offer_add_location": {
                "text": "изменить место",
                "message": "Выберите место",
                "good_message": "Место изменено"
            },
            "offer_publish": {
                "text": "опубликовать",
                "message": "Опубликовано"
            },
            "offer_hidden": {
                "text": "скрыть",
                "message": "Скрыто"
            }
        }
        
        self.help_message()
        self.start_message()
        
    def help_message(self):
        self.COMMANDS["help"]["message"] = \
            f"{self.BOTNAME} - это телеграмм бот для создания и поиска объявлений. Он имеет следующие функции:\n" \
            + "\n".join(['/' + com + " - " + inf["desc"] for com, inf in self.COMMANDS.items()])
    def start_message(self):
        self.COMMANDS["start"]["message"] = \
            "Здравствуйте! Данный бот служит для создания и поиска объявлений.\n" \
            "Для более подробной информации о функционале используйте /help\n" \
            "Для поиска объявлений используйте /list_offer\n" \
            "Для создания своего объявления используйте /new_offer"

    def offer_format_long(self, title="", cost="", desc="", user_name="", chat_id="", type="", hidden=0):
        msg = f"{title} - {cost}\n{desc}\n{user_name}"
        if hidden == 1:
            msg = msg + "\nСкрыто"
        return msg

    def offer_format_short(self, title, cost):
        return f"{title} - {cost}"
    
    def offer_inline_manage(self, offer_id) -> InlineKeyboardMarkup:
        inline_manage_offer = InlineKeyboardMarkup(row_width=1)
        inline_manage_offer.add(
            InlineKeyboardButton(
                callback_data="offer_add_title" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_add_title"]["text"]
            ),
            InlineKeyboardButton(
                callback_data="offer_add_desc" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_add_desc"]["text"]
            ),
            InlineKeyboardButton(
                callback_data="offer_add_cost" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_add_cost"]["text"]
            ),
            # InlineKeyboardButton(
            #     callback_data="offer_add_location" + " " + str(offer_id), 
            #     text=self.INLINE_REQUSESTS["offer_add_location"]["text"]
            # ),
            # InlineKeyboardButton(
            #     callback_data="offer_add_quantity" + " " + str(offer_id), 
            #     text=self.INLINE_REQUSESTS["offer_add_quantity"]["text"]
            # ),
            InlineKeyboardButton(
                callback_data="offer_hidden" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_hidden"]["text"]
            ),
            InlineKeyboardButton(
                callback_data="offer_publish" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_publish"]["text"]
            ),
        )
        return inline_manage_offer
    def offer_choose(self, offers, callback_data) -> InlineKeyboardMarkup:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        for offer in offers:
            inline_markup.add(
                InlineKeyboardButton(
                    text=self.offer_format_short(title=offer["title"], cost=offer["cost"]),
                    callback_data=callback_data + " " + str(offer["offer_id"])
                )
            )
        return inline_markup

bc = BotConfig()
