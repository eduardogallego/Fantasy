import logging
import sqlite3

from sqlite3 import Error
from utils import Logger

Logger()
logger = logging.getLogger('server')


class Database:

    def __init__(self):
        db_file = r"database.db"
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_file)
        except Error as e:
            logger.ERROR("Database Error: " + e)

    def get_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, pos, buy_tt, buy_value, sell_tt, sell_value FROM operations")
        rows = cursor.fetchall()
        for row in rows:
            print(row)


if __name__ == "__main__":
    database = Database()
    database.get_operations()
