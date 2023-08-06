import json
import logging
import sqlite3

from apiclient import ApiClient
from datetime import datetime
from sqlite3 import Error
from utils import Config


class Database:

    db_file = r"database.db"
    # timestamp: datetime.now().astimezone().isoformat(), +timezone +Tsyntax, 2023-08-06T02:29:33.213873+02:00

    def __init__(self, config):
        self.logger = logging.getLogger('database')
        self.config = config
        self.api_client = ApiClient(config)
        self.connection = None
        try:
            self.connection = sqlite3.connect(self.db_file)
        except Error as e:
            self.logger.ERROR("Database Error: " + e)

    def get_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, pos, buy_tt, buy_value, sale_tt, sale_value FROM operations "
                       "WHERE sale_tt IS NOT NULL ORDER BY sale_tt DESC, buy_tt DESC")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({"name": row[0], "pos": row[1], "buy_tt": datetime.fromisoformat(row[2]).strftime('%d-%m-%y'),
                           "buy_value": '{0:.2f}'.format(round(row[3] / 1000000, 2)),
                           "sale_tt": datetime.fromisoformat(row[4]).strftime('%d-%m-%y'),
                           "sale_value": '{0:.2f}'.format(round(row[5] / 1000000, 2)),
                           "benefit": '{0:.2f}'.format(round((row[5] - row[3]) / 1000000, 2)),
                           "percent": f"{round((row[5] - row[3]) * 100 / row[3], 0)}%"})
        return json.dumps(result)

    def update_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT status_value FROM status WHERE status_key = 'last_operation'")
        last_operation = cursor.fetchone()[0]
        sale_operations = []
        buy_operations = []
        latest_operation = None
        for operation in self.api_client.get_operations():
            if last_operation is None \
                    or datetime.fromisoformat(operation['timestamp']) > datetime.fromisoformat(last_operation):
                if operation['type'] == 'sale':
                    sale_operations.append(operation)
                else:
                    buy_operations.append((operation['player_id'], operation['name'], operation['pos'],
                                           operation['timestamp'], operation['value']))
                if latest_operation is None or operation['timestamp'] > latest_operation:
                    latest_operation = operation['timestamp']
        if buy_operations:
            cursor.executemany('INSERT INTO operations(player_id,name,pos,buy_tt,buy_value) VALUES(?,?,?,?,?)',
                               buy_operations)
        for sale in sale_operations:
            cursor.execute(f"UPDATE operations SET sale_tt = '{sale['timestamp']}', sale_value = {sale['value']} "
                           f"WHERE player_id = '{sale['player_id']}' AND sale_tt IS NULL")
        if latest_operation is not None:
            cursor.execute(f"UPDATE status SET status_value = '{latest_operation}' where status_key = 'last_operation'")
        self.connection.commit()


if __name__ == "__main__":
    configuration = Config()
    database = Database(configuration)
    # database.update_operations()
    database.get_operations()
