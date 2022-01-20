# - *- coding: utf- 8 - *-
import sqlite3
from utils.decorators import catcherError
import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@catcherError
def db_con():
    mydb = sqlite3.connect(f'database/database.sqlite')
    mydb.row_factory = dict_factory
    return mydb

@catcherError       
def create_tables():
    mydb = db_con()
    mycursor = mydb.cursor()

    mycursor.execute(""" CREATE TABLE IF NOT EXISTS news (
                        id INTEGER PRIMARY KEY,
                        url VARCHAR(255),
                        tags VARCHAR(255) DEFAULT '',
                        name VARCHAR(255),
                        create_date DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """
    )

@catcherError
def add_news(url):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO news (url) VALUES (?)""", (url, ))
    mydb.commit()
    cursor.close()

@catcherError
def get_news(url):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM news WHERE url = ?",(url, ))
    result = cursor.fetchone()
    cursor.close()
    return result