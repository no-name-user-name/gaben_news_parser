# - *- coding: utf- 8 - *-
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

token = config["settings"]["token"]
group = int(config['settings']['group'])
admins = [int(a) for a in config['settings']['admins'].split(',')]

known_users = {}
user_step = {}
username_list = {}
temp = {}


tags = {
    'Steam': '#steam',
    'EpicGames': '#epic',
    'Epic': '#epic',
    'Amazon': '#amazon',
    'Epic Games': '#epic',
    'EGS': '#epic',
    'GOG': '#gog',
    'Prime Gaming': '#amazon',
    'Xbox': '#xbox',
    'IndieGala': '#indieGala',
    'PS Store': '#playstation',
    'PS Plus': '#playstation',
    'Ubisoft': '#ubisoft',
    'Nintendo': '#nintendo',
    'Blizzard': '#blizzard',
    'Microsoft Store': '#microsoft',
    'Rockstar': '#rockstar',
    'Origin': '#origin',
    'Call of Duty': '#cod',
    'Battlefield': '#bf',
    'Cyberpunk': '#cyberpunk',
    'распродажа': '#распродажа',
    'халява': '#free',
    'скидки': '#sale',
    'скидка': '#sale',
    'скидкy': '#sale',
    'дарит': '#free',
    'бесплатно': '#free',
    'бесплатная раздача': '#free',
    'бесплатно отдают': '#free',
    'бесплатно забрать': '#free',
    'Бесплатная': '#free',
    'Открыта раздача': '#free',
    'Бесплатная раздача': '#free',
    'бесплатный доступ': '#доступно',
    'Бесплатные выходные': '#выходные',
    'раздают': '#раздача',
    'раздает': '#раздача',
    'раздает ключи': '#ключ',
    'закрытое бета-тестирование': '#збт',
}
