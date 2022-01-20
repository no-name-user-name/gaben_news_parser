import telebot
from utils.decorators import catcherError
from database import db
from config import token

@catcherError
def get_bot():
    return telebot.TeleBot(token)