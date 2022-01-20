
import logging
from datetime import datetime
from utils.decorators import catcherError


@catcherError
def log(e):
    print(e)
    logging.exception(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

