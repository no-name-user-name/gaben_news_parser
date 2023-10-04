import datetime

import telebot

from config import token


def get_bot(parse_mode="HTML") -> telebot.TeleBot:
    bot = telebot.TeleBot(token, parse_mode=parse_mode)
    return bot


def listener(messages):
    for m in messages:
        log = {
            'cid': m.from_user.id,
            'username': m.from_user.username,
            'type': 'text',
            'text': m.text
        }
        print(f"[{datetime.datetime.now()}] {log}")

