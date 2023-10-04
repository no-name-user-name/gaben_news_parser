import datetime

from telebot import TeleBot
from telebot.types import CallbackQuery, PhotoSize

import config


def get_bot_callbacks(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def command(call: CallbackQuery):
        cid = call.from_user.id
        mid = call.message.id

        caption = call.message.caption
        entities = call.message.caption_entities
        img: PhotoSize = call.message.photo[-1]

        log = {
            'cid': call.from_user.id,
            'username': call.from_user.username,
            'type': 'callback',
            'callback': call.data
        }

        print(f"[{datetime.datetime.now()}] {log}")
        params = call.data.split('-')

        match params[0]:
            case 'main':
                pass

            case 'post':
                match params[1]:
                    case 'publish':
                        bot.parse_mode = None
                        bot.send_photo(config.group, img.file_id, caption=caption, caption_entities=entities)
                        bot.edit_message_reply_markup(cid, mid, reply_markup=None)

            case 'close':
                bot.delete_message(cid, mid)

            case 'soon':
                bot.answer_callback_query(call.id, 'Скоро', show_alert=True)
