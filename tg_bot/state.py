from aiogram.utils.helper import Helper, HelperMode, ListItem

class BotStates(Helper):
    mode = HelperMode.snake_case
    
    WAIT_USER_DESC = ListItem()
    WAIT_USER_NAME = ListItem()
    
    WAIT_OFFER_TITLE = ListItem()
    WAIT_OFFER_DESC = ListItem()
    WAIT_OFFER_COST = ListItem()

if __name__ == '__main__':
    print(BotStates.all())