from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BotConfig:
    def __init__(self) -> None:
        self.BOTNAME = "Localboard"
        self.COMMANDS = {
            "start": {
                "desc": "входная точка в функционал бота",
                "message": ""
            },
            "help": {
                "desc": "информация о боте и его функциях",
                "message": ""
            },
            "list_offer": {
                "desc": "вывести список доступных предложений",
                "message": "" # тут нужна кнопка на смену локации
            },
            "new_offer": {
                "desc": "создать объявление",
                "message": "Создано следующее объявление"
            },
            "my_offer": {
                "desc": "вывести все объявления которые принадлежат вам"
            },
            "get_me": {
                "desc": "посмотреть и изменить свой профиль"
            }
        }

        self.INLINE_REQUSESTS = {
            "offer_add_desc": {
                "text": "изменить описание",
                "message": "Введите описание"
            },
            "offer_add_title": {
                "text": "изменить название",
                "message": "Введите название"
            },
            "offer_add_cost": {
                "text": "изменить цену",
                "message": "Введите цену"
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
        return f"<b>{title}<\b> - {cost}"
    
    def offer_inline_manage(self, offer_id):
        inline_manage_offer = InlineKeyboardMarkup(row_width=3)
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
            InlineKeyboardButton(
                callback_data="offer_publish" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_publish"]["text"]
            ),
            InlineKeyboardButton(
                callback_data="offer_hidden" + " " + str(offer_id), 
                text=self.INLINE_REQUSESTS["offer_hidden"]["text"]
            )
        )
        return inline_manage_offer