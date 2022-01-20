# - *- coding: utf- 8 - *-
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
token = config["settings"]["token"]
admin = config["settings"]["admin_id"]
group = config['settings']['group_id']

tags = {
    'Steam':'#steam',
    'EpicGames':'#epic',
    'Epic':'#epic',
    'Amazon':'#amazon',
    'Epic Games':'#epic',
    'EGS':'#epic',
    'GOG': '#gog',
    'Prime Gaming':'#amazon',
    'Xbox': '#xbox',
    'IndieGala':'#indieGala',
    'PS Store':'#playstation',
    'PS Plus':'#playstation',
    'Ubisoft':'#ubisoft',
    'Nintendo':'#nintendo',
    'Blizzard':'#blizzard',
    'Microsoft Store':'#microsoft',
    'Rockstar':'#rockstar',
    'Origin':'#origin',
    'Call of Duty':'#cod',
    'Battlefield':'#bf',
    'Cyberpunk':'#cyberpunk',
    'Cyberpunk':'#cyberpunk',
    'распродажа':'#распродажа',
    'халява':'#халява',
    'скидки':'#скидки',
    'скидка':'#скидки',
    'дарит': '#халява',
    'дарит': '#халява',
    'бесплатно': '#халява',
    'бесплатная раздача':'#раздача',
    'бесплатно отдают':'#халява',
    'бесплатно забрать':'#халява',
    'Бесплатная':'#халява',
    'Открыта раздача':'#раздача',
    'Бесплатная раздача':'#раздача',
    'бесплатный доступ':'#доступно',
    'Бесплатные выходные':'#выходные',
    'раздают':'#раздача',
    'раздает':'#раздача',
    'раздает ключи':'#ключ',
    'закрытое бета-тестирование':'#збт',
}