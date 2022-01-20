import logging
from datetime import datetime

def log(e):
    print(e)
    logging.basicConfig(filename='logs.log', filemode='a',encoding='utf-8', level=logging.ERROR)
    logging.exception(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def catcherError(func):
    def f(*args):
        try:
            out = func(*args)
            return out
        except Exception as e:
            log(e)
    return f