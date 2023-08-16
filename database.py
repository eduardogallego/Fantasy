import json
import logging
import sqlite3

from apiclient import ApiClient
from datetime import datetime, timezone
from sqlite3 import Error
from utils import Config


class Database:

    db_file = r"config/database.db"
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

    def get_market(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, team, pos, status, buy_value, percent_change_3d, points, avgPoints, "
                       "bids, myBid, seller FROM market ORDER BY avgPoints DESC, percent_change_3d DESC")
        rows = cursor.fetchall()
        result = []
        value_list = []
        for row in rows:
            value_list.append(row[4])
        list.sort(value_list, reverse=True)
        for row in rows:
            index = value_list.index(row[4]) + 1
            result.append({"index": index, "name": row[0], "team": row[1], "pos": row[2], "status": row[3],
                           "buy_value": '{0:.2f}'.format(round(row[4] / 1000000, 2)), "percent_chg_3d": row[5],
                           "points": row[6], "avgPoints": row[7], "bids": row[8],
                           "myBid": '{0:.2f}'.format(round(row[9] / 1000000, 2)) if row[9] is not None else None,
                           "seller": row[10]})
        return json.dumps(result)

    def get_players(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, team, pos, status, sale_value, points, average_points, last_season_points, seller "
                       "FROM players ORDER BY points DESC, sale_value ASC")
        rows = cursor.fetchall()
        result = []
        index = 0
        for row in rows:
            index += 1
            result.append({"index": index, "name": row[0], "team": row[1], "pos": row[2], "status": row[3],
                           "sale_value": '{0:.2f}'.format(round(row[4] / 1000000, 2)),
                           "points": row[5], "avgPoints": row[6], "lastSeasonPoints": row[7], "seller": row[8]})
        return json.dumps(result)

    def get_players_top(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, team, pos, status, sale_value, points, average_points, last_season_points, seller "
                       "FROM players ORDER BY points DESC, sale_value ASC")
        rows = cursor.fetchall()
        result = []
        goalkeepers = 0
        defenders = 0
        midfielders = 0
        strikers = 0
        index = 0
        for row in rows:
            if row[3] != 'ok':
                continue
            if (row[2] == 1 and goalkeepers < 1) or (row[2] == 2 and defenders < 5 and (defenders + midfielders) < 10)\
                    or (row[2] == 3 and midfielders < 5 and (midfielders + strikers) < 7 and (defenders + midfielders) < 10) \
                    or (row[2] == 4 and strikers < 3 and (midfielders + strikers) < 7):
                index += 1
                result.append({"index": index, "name": row[0], "team": row[1], "pos": row[2], "status": row[3],
                               "sale_value": '{0:.2f}'.format(round(row[4] / 1000000, 2)),
                               "points": row[5], "avgPoints": row[6], "lastSeasonPoints": row[7], "seller": row[8]})
                if row[2] == 1:
                    goalkeepers += 1
                elif row[2] == 2:
                    defenders += 1
                elif row[2] == 3:
                    midfielders += 1
                elif row[2] == 4:
                    strikers += 1
                if len(result) == 11:
                    break
        return json.dumps(result)

    def get_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, pos, buy_tt, buy_value, sale_tt, sale_value FROM operations "
                       "WHERE sale_tt IS NOT NULL ORDER BY sale_tt DESC, buy_tt DESC")
        rows = cursor.fetchall()
        result = []
        benefit_list = []
        for row in rows:
            benefit_list.append(row[5] - row[3])
        list.sort(benefit_list, reverse=True)
        for row in rows:
            benefit = row[5] - row[3]
            index = benefit_list.index(benefit) + 1
            result.append({"index": index, "name": row[0], "pos": row[1],
                           "buy_tt": datetime.fromisoformat(row[2]).strftime('%d-%m-%y'),
                           "buy_value": '{0:.2f}'.format(round(row[3] / 1000000, 2)),
                           "sale_tt": datetime.fromisoformat(row[4]).strftime('%d-%m-%y'),
                           "sale_value": '{0:.2f}'.format(round(row[5] / 1000000, 2)),
                           "benefit": '{0:.2f}'.format(round(benefit / 1000000, 2)),
                           "percent": round((row[5] - row[3]) * 100 / row[3], 0)})
        return json.dumps(result)

    def get_status(self, key):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT status_value FROM status WHERE status_key = '{key}'")
        return cursor.fetchone()[0]

    def get_team(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, team, pos, status, buy_value, sale_value, clause_value, clause_tt, "
                       "percent_change_3d, points FROM team ORDER BY pos ASC, sale_value DESC")
        rows = cursor.fetchall()
        result = []
        value_list = []
        for row in rows:
            value_list.append(row[6])
        list.sort(value_list, reverse=True)
        for row in rows:
            index = value_list.index(row[6]) + 1
            clause_secs = round((datetime.fromisoformat(row[7]) - datetime.now(timezone.utc)).total_seconds())
            result.append({"index": index, "name": row[0], "team": row[1], "pos": row[2], "status": row[3],
                           "buy_value": '{0:.2f}'.format(round(row[4] / 1000000, 2)),
                           "sale_value": '{0:.2f}'.format(round(row[5] / 1000000, 2)),
                           "clause_value": '{0:.2f}'.format(round(row[6] / 1000000, 2)), "clause_secs": clause_secs,
                           "benefit": '{0:.2f}'.format(round((row[5] - row[4]) / 1000000, 2)),
                           "percent_ben": round((row[5] - row[4]) * 100 / row[4]),
                           "change_3d": '{0:.2f}'.format(round(row[8] * row[5] / 100000000, 2)),
                           "percent_chg_3d": row[8],
                           "points": row[9]})
        return json.dumps(result)

    def get_team_status(self):
        money = round(int(self.get_status('team_money')) / 1000000)
        value = round(int(self.get_status('team_value')) / 1000000)
        points = self.get_status('team_points')
        return money, value, points

    def update_market(self):
        cursor = self.connection.cursor()
        market = self.api_client.get_market()
        cursor.execute('DELETE FROM market')
        cursor.executemany('INSERT INTO market(name,team,pos,status,buy_value,percent_change_3d,points,'
                           'avgPoints,bids,myBid,seller) VALUES(?,?,?,?,?,?,?,?,?,?,?)', market)
        self.connection.commit()

    def update_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT status_value FROM status WHERE status_key = 'last_operation'")
        last_operation = cursor.fetchone()[0]
        sale_operations = []
        buy_operations = []
        latest_operation = None
        for operation in self.api_client.get_operations():
            if datetime.fromisoformat(operation['timestamp']) > datetime.fromisoformat(last_operation):
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
            self.update_status(cursor, 'last_operation', latest_operation)
        self.connection.commit()

    def update_players(self):
        cursor = self.connection.cursor()
        players = self.api_client.get_players()
        cursor.execute('DELETE FROM players')
        cursor.executemany('INSERT INTO players(name, team, pos, status, sale_value, points, average_points, '
                           'last_season_points, seller) VALUES(?,?,?,?,?,?,?,?,?)', players)
        self.connection.commit()

    def update_status(self, cursor, key, value):
        cursor.execute(f"UPDATE status SET status_value = '{value}' where status_key = '{key}'")

    def update_team(self):
        cursor = self.connection.cursor()
        team, players = self.api_client.get_team()
        players_db = []
        for player in players:
            cursor.execute(f"SELECT buy_tt, buy_value FROM operations "
                           f"WHERE player_id = {player[0]} AND sale_tt IS NULL")
            buy_prices = cursor.fetchone()
            players_db.append((player[0], player[1], player[2], player[3], player[4], buy_prices[0],
                               buy_prices[1], player[5], player[6], player[7], player[8], player[9]))
        self.update_status(cursor, 'team_manager', team['team_manager'])
        self.update_status(cursor, 'team_money', team['team_money'])
        self.update_status(cursor, 'team_value', team['team_value'])
        self.update_status(cursor, 'team_points', team['team_points'])
        cursor.execute('DELETE FROM team')
        cursor.executemany('INSERT INTO team(player_id,name,team,pos,status,buy_tt,buy_value,sale_value,'
                           'percent_change_3d,clause_value,clause_tt,points) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                           players_db)
        self.connection.commit()


if __name__ == "__main__":
    configuration = Config()
    database = Database(configuration)
    # database.update_operations()
    # print(json.dumps(database.get_operations()))
    # database.update_team()
    # print(json.dumps(database.get_team()))
    # database.update_market()
    # print(json.dumps(database.get_market()))
    # database.update_players()
    # print(json.dumps(database.get_players()))
    # print(json.dumps(database.get_players_top()))
