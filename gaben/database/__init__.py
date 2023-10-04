# - *- coding: utf- 8 - *-

# - *- coding: utf- 8 - *-
import sqlite3


class DataBase:
    def __init__(self, db_name: str = 'db'):
        self.mydb = sqlite3.connect(f'{db_name}.sqlite')
        self.mydb.row_factory = self.dict_factory
        self.__create_tables()

    @staticmethod
    def dict_factory(cursor, row):
        """Convert cortage to dict"""
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def __create_tables(self):
        cursor = self.mydb.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS news (
                        id INTEGER PRIMARY KEY,
                        url VARCHAR(255),
                        tags VARCHAR(255) DEFAULT '',
                        name VARCHAR(255),
                        create_date DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """
                       )
        cursor.close()

    def add_news(self, url: str):
        cursor = self.mydb.cursor()
        cursor.execute("""INSERT INTO news (url) VALUES (?)""", (url,))
        self.mydb.commit()
        result = cursor.lastrowid
        cursor.close()
        return result

    def get_news(self, url: str):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM news WHERE url = ?", (url,))
        result = cursor.fetchone()
        cursor.close()
        return result

