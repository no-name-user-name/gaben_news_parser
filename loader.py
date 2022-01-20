import logging

from database import db
from datetime import datetime

import config

logging.basicConfig(filename='logs.log', filemode='w',encoding='utf-8', level=logging.ERROR)
logging.exception(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
db.create_tables()
print('~~ Silent Start ~~')

