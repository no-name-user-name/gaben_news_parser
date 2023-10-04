from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from gaben.bot.base_functions import get_bot

bot = get_bot()


def render(cid, msg, reply_markup, mid=None):
    if not mid:
        with open('assets/botpics/main.mp4', 'rb') as anim:
            return bot.send_animation(cid, anim, caption=msg, disable_notification=True, reply_markup=reply_markup)
    else:
        return bot.edit_message_caption(msg, cid, mid, reply_markup=reply_markup)


def main(cid, mid=None):
    pass


def message_box(cid, msg, mid=None, back_callback=None, back_button_text='◂ Назад', step_name=None):
    config.user_step[cid] = step_name
    markup = InlineKeyboardMarkup()
    if back_callback is not None:
        markup.row(InlineKeyboardButton(back_button_text, callback_data=back_callback))

    m = render(cid, msg, markup, mid)

    return m.message_id
