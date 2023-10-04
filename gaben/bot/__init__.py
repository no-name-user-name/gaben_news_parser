from time import sleep

from gaben.bot._callbacks import get_bot_callbacks
from gaben.bot._cmds import get_bot_input_cmd
from gaben.bot._docs import get_bot_input_docs
from gaben.bot._text import get_bot_input_text
from gaben.bot.base_functions import get_bot
from gaben.bot.base_functions import listener


def start():
    while 1:
        try:
            bot = get_bot()
            bot.set_update_listener(listener)
            get_bot_input_cmd(bot)
            get_bot_input_text(bot)
            get_bot_callbacks(bot)
            get_bot_input_docs(bot)
            bot.infinity_polling()
        except Exception as e:
            print("Ошибка в работе бота. Попытка перезапуска через 5 секунд...")

            sleep(5)
