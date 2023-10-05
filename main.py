import threading
from time import sleep

from gaben import Parser, bot


def parser_loop():
    while 1:
        try:
            Parser().start()
        except Exception as e:
            raise

        finally:
            sleep(60)


if __name__ == '__main__':
    print('~~ Silent Start ~~')
    threading.Thread(target=parser_loop).start()

    bot.start()
