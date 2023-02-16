from aiogram.utils.helper import Helper, HelperMode, ListItem

class BotStates(Helper):
    mode = HelperMode.snake_case
    
    WAIT_USER_DESC = ListItem()
    WAIT_USER_NAME = ListItem()

if __name__ == '__main__':
    print(BotStates.all())