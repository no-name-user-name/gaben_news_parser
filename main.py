import loader
from parsers import Parser
from time import sleep
from utils.base_functions import log

def main(p):
    pars_count = 0
    while 1:
        try:
            p.start()
            pars_count += 1
            print(pars_count)
            sleep(60)
        except Exception as e:
            log(e)

if __name__ == '__main__':
    p = Parser()
    main(p)