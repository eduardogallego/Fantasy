import json
import logging
import sqlite3

from apiclient import ApiClient
from datetime import datetime, timezone
from htmlparser import StartingTeamParser
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
            self.logger.error("Database Error: " + str(e))

    def get_market(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, m.team, pos, status, buy_value, percent_change_3d, points, "
                       "matches, average, bids, myBid, seller, rival, inout, percentage "
                       "FROM market AS m LEFT JOIN next AS n ON m.team = n.team and name = player "
                       "ORDER BY average DESC, percent_change_3d DESC")
        rows = cursor.fetchall()
        result = []
        value_list = []
        for row in rows:
            value_list.append(row[8])
        list.sort(value_list, reverse=True)
        for row in rows:
            index = value_list.index(row[8]) + 1
            result.append({"index": index, "player": row[0], "team": row[1], "pos": row[2],
                           "status": row[3], "buy_value": '{0:.2f}'.format(round(row[4] / 1000000, 2)),
                           "change_3d": '{0:.2f}'.format(round(row[5] * row[4] / 100000000, 2)),
                           "percent_chg_3d": row[5], "points": row[6], "matches": row[7],
                           "average": '{0:.2f}'.format(round(row[8] / 100, 2)), "bids": row[9],
                           "myBid": '{0:.2f}'.format(round(row[10] / 1000000, 2)) if row[10] is not None else None,
                           "seller": row[11], "tag": 0, "rival": row[12], "inout": row[13], "percentage": row[14]})
        return json.dumps(result)

    def get_next_match(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT team, player, rival, inout, percentage FROM next ORDER BY team ASC, percentage DESC")
        rows = cursor.fetchall()
        result = []
        index = 0
        for row in rows:
            index += 1
            result.append({"index": index, "team": row[0], "player": row[1], "rival": row[2],
                           "inout": row[3], "percentage": row[4]})
        return json.dumps(result)

    def get_players(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, p.team, pos, status, sale_value, points, average_points, "
                       "last_season_points, seller, rival, inout, percentage "
                       "FROM players AS p LEFT JOIN next AS n ON p.team = n.team and name = player "
                       "ORDER BY average_points DESC, points DESC, sale_value ASC")
        rows = cursor.fetchall()
        result = []
        index = 0
        for row in rows:
            index += 1
            result.append({"index": index, "player": row[0], "team": row[1], "pos": row[2], "status": row[3],
                           "sale_value": '{0:.2f}'.format(round(row[4] / 1000000, 2)),
                           "points": row[5], "average": '{0:.2f}'.format(round(row[6], 2)),
                           "lastSeasonPoints": row[7], "seller": row[8], "rival": row[9],
                           "inout": row[10], "percentage": row[11], "tag": 0})
        return json.dumps(result)

    def get_players_top(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, p.team, pos, status, sale_value, points, average_points, "
                       "last_season_points, seller, rival, inout, percentage "
                       "FROM players AS p LEFT JOIN next AS n ON p.team = n.team and name = player "
                       "WHERE points > 2 * average_points "
                       "ORDER BY average_points DESC, points DESC, sale_value ASC")
        rows = cursor.fetchall()
        players = []
        goalkeepers = defenders = midfielders = strikers = 0
        for row in rows:
            if row[3] != 'ok':
                continue
            elif row[2] == 1 and goalkeepers == 0:
                goalkeepers += 1
                players.append(row + (goalkeepers + defenders + midfielders + strikers,))
            elif row[2] == 2 and defenders < 5 and (defenders + midfielders) < 9 and (defenders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                defenders += 1
                players.append(row + (goalkeepers + defenders + midfielders + strikers,))
            elif row[2] == 3 and midfielders < 5 and (defenders + midfielders) < 9 and (midfielders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                midfielders += 1
                players.append(row + (goalkeepers + defenders + midfielders + strikers,))
            elif row[2] == 4 and strikers < 3 and (defenders + strikers) < 7 and (midfielders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                strikers += 1
                players.append(row + (goalkeepers + defenders + midfielders + strikers,))
            if len(players) == 11:
                break
        result = []
        index = 0
        for player in players:
            index += 1
            result.append({"index": index, "player": player[0], "team": player[1], "pos": player[2],
                           "status": player[3], "sale_value": '{0:.2f}'.format(round(player[4] / 1000000, 2)),
                           "points": player[5], "average": '{0:.2f}'.format(round(player[6], 2)),
                           "lastSeasonPoints": player[7], "seller": player[8], "rival": player[9],
                           "inout": player[10], "percentage": player[11], "tag": player[12]})
        return json.dumps(result)

    def get_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, pos, buy_tt, buy_value, sale_tt, sale_value, clause_update, buyer, seller "
                       "FROM operations ORDER BY sale_tt DESC, buy_tt DESC")
        rows = cursor.fetchall()
        result = []
        benefit_list = []
        for row in rows:
            benefit_list.append(0 if row[5] is None else (row[5] - row[3] - row[6]))
        list.sort(benefit_list, reverse=True)
        for row in rows:
            benefit = 0 if row[5] is None else (row[5] - row[3] - row[6])
            index = benefit_list.index(benefit) + 1
            result.append({"index": index, "name": row[0], "pos": row[1],
                           "buy_tt": datetime.fromisoformat(row[2]).strftime('%d-%m'),
                           "buy_value": '{0:.2f}'.format(round(row[3] / 1000000, 2)),
                           "sale_tt": None if row[4] is None else datetime.fromisoformat(row[4]).strftime('%d-%m'),
                           "sale_value": None if row[5] is None else '{0:.2f}'.format(round(row[5] / 1000000, 2)),
                           "benefit": None if benefit is None else '{0:.2f}'.format(round(benefit / 1000000, 2)),
                           "percent": None if benefit is None else round(benefit * 100 / (row[3] + row[6]), 0),
                           "clause_update": '{0:.2f}'.format(round(row[6] / 1000000, 2)),
                           "buyer": row[7], "seller": row[8]})
        return json.dumps(result)

    def get_points(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT points.player, points.team, points.pos, manager_id,'
                       '(coalesce(j1,0) + coalesce(j2,0) + coalesce(j3,0) + coalesce(j4,0) + coalesce(j5,0) '
                       '+ coalesce(j6,0) + coalesce(j7,0) + coalesce(j8,0) + coalesce(j9,0) + coalesce(j10,0) '
                       '+ coalesce(j11,0) + coalesce(j12,0) + coalesce(j13,0) + coalesce(j14,0) + coalesce(j15,0) '
                       '+ coalesce(j16,0) + coalesce(j17,0) + coalesce(j18,0) + coalesce(j19,0) + coalesce(j20,0) '
                       '+ coalesce(j21,0) + coalesce(j22,0) + coalesce(j23,0) + coalesce(j24,0) + coalesce(j25,0) '
                       '+ coalesce(j26,0) + coalesce(j27,0) + coalesce(j28,0) + coalesce(j29,0) + coalesce(j30,0) '
                       '+ coalesce(j31,0) + coalesce(j32,0) + coalesce(j33,0) + coalesce(j34,0) + coalesce(j35,0) '
                       '+ coalesce(j36,0) + coalesce(j37,0) + coalesce(j38,0)) as total, '
                       'j1, j2, j3, j4, j5, j6, j7, j8, j9, j10, j11, j12, j13, j14, j15, j16, j17, j18, j19, j20, '
                       'j21, j22, j23, j24, j25, j26, j27, j28, j29, j30, j31, j32, j33, j34, j35, j36, j37, j38 '
                       'FROM points LEFT JOIN teams ON points.id = teams.id '
                       'ORDER BY total DESC, points.pos ASC')
        rows = cursor.fetchall()
        result = []
        total_list = []
        for row in rows:
            total_list.append(row[4])
        list.sort(total_list, reverse=True)
        goalkeepers = defenders = midfielders = strikers = 0
        for row in rows:
            index = total_list.index(row[4]) + 1
            tag = 0
            if row[2] == 1 and goalkeepers == 0:
                goalkeepers += 1
                tag = goalkeepers + defenders + midfielders + strikers
            elif row[2] == 2 and defenders < 5 and (defenders + midfielders) < 9 and (defenders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                defenders += 1
                tag = goalkeepers + defenders + midfielders + strikers
            elif row[2] == 3 and midfielders < 5 and (defenders + midfielders) < 9 and (midfielders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                midfielders += 1
                tag = goalkeepers + defenders + midfielders + strikers
            elif row[2] == 4 and strikers < 3 and (defenders + strikers) < 7 and (midfielders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                strikers += 1
                tag = goalkeepers + defenders + midfielders + strikers
            active = row[3] is not None and row[3] == self.config.get('team_id')
            result.append({"index": index, "player": row[0], "team": row[1], "pos": row[2], "total": row[4],
                           "j1": row[5], "j2": row[6], "j3": row[7], "j4": row[8], "j5": row[9],
                           "j6": row[10], "j7": row[11], "j8": row[12], "j9": row[13], "j10": row[14],
                           "j11": row[15], "j12": row[16], "j13": row[17], "j14": row[18], "j15": row[19],
                           "j16": row[20], "j17": row[21], "j18": row[22], "j19": row[23], "j20": row[24],
                           "j21": row[25], "j22": row[26], "j23": row[27], "j24": row[28], "j25": row[29],
                           "j26": row[30], "j27": row[31], "j28": row[32], "j29": row[33], "j30": row[34],
                           "j31": row[35], "j32": row[36], "j33": row[37], "j34": row[38], "j35": row[39],
                           "j36": row[40], "j37": row[41], "j38": row[42], "tag": tag, "active": active})
        return json.dumps(result)

    def get_status(self, key):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT status_value FROM status WHERE status_key = '{key}'")
        return cursor.fetchone()[0]

    def get_team(self):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT t.player, t.team, t.pos, status, t.buy_value, t.sale_value, clause_value, clause_tt, '
                       f'clause_update, percent_change_3d, points, matches, average, tag, rival, inout, percentage '
                       f'FROM teams AS t INNER JOIN operations AS o ON o.player_id = t.id '
                       f'LEFT JOIN next AS n ON t.team = n.team AND t.player = n.player '
                       f'WHERE manager_id == "{self.config.get("team_id")}" AND o.sale_value IS NULL '
                       f'ORDER BY t.pos ASC, average DESC')
        rows = cursor.fetchall()
        result = []
        value_list = []
        for row in rows:
            value_list.append(row[12])
        list.sort(value_list, reverse=True)
        for row in rows:
            index = value_list.index(row[12]) + 1
            buy_value = None if row[4] is None else '{0:.2f}'.format(round(row[4] / 1000000, 2))
            benefit = None if row[4] is None else '{0:.2f}'.format(round((row[5] - row[4] - row[8]) / 1000000, 2))
            perc_ben = None if row[4] is None else round((row[5] - row[4] - row[8]) * 100 / (row[4] + row[8]))
            clause_secs = round((datetime.fromisoformat(row[7]) - datetime.now(timezone.utc)).total_seconds())
            clause = '{0:.2f}'.format(round(row[6] / 1000000, 2))
            if clause_secs > 86400:
                clause = f'{round(clause_secs / 86400)}d'
            elif clause_secs > 3600:
                clause = f'{round(clause_secs / 3600)}h'
            elif clause_secs > 60:
                clause = f'{round(clause_secs / 60)}m'
            elif clause_secs > 0:
                clause = f'{clause_secs}s'
            perc_clause = None if clause_secs > 0 else round(((row[6] - row[5]) * 100) / row[5])
            result.append({"index": index, "player": row[0], "team": row[1], "pos": row[2], "status": row[3],
                           "buy_value": buy_value, "sale_value": '{0:.2f}'.format(round(row[5] / 1000000, 2)),
                           "clause": clause, "clause_update": '{0:.2f}'.format(round(row[8] / 1000000, 2)),
                           "perc_clause": perc_clause, "benefit": benefit, "perc_ben": perc_ben,
                           "change_3d": '{0:.2f}'.format(round(row[9] * row[5] / 100000000, 2)),
                           "perc_chg_3d": row[9], "points": row[10], "matches": row[11],
                           "average": '{0:.2f}'.format(round(row[12] / 100, 2)), "tag": row[13],
                           "rival": row[14], "inout": row[15], "percentage": row[16]})
        return json.dumps(result)

    def get_rivals(self):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT t.player, t.team, pos, status, m.manager, sale_value, clause_value, clause_tt, '
                       f'percent_change_3d, t.points, matches, average, tag, rival, inout, percentage '
                       f'FROM teams AS t INNER JOIN managers AS m ON t.manager_id = m.id '
                       f'LEFT JOIN next AS n ON t.team = n.team and t.player = n.player '
                       f'WHERE manager_id != "{self.config.get("team_id")}" '
                       f'ORDER BY m.points DESC, m.team_value DESC, pos ASC, average DESC')
        rows = cursor.fetchall()
        result = []
        value_list = []
        for row in rows:
            value_list.append(row[11])
        list.sort(value_list, reverse=True)
        for row in rows:
            index = value_list.index(row[11]) + 1
            clause_secs = round((datetime.fromisoformat(row[7]) - datetime.now(timezone.utc)).total_seconds())
            clause = '{0:.2f}'.format(round(row[6] / 1000000, 2))
            if clause_secs > 86400:
                clause = f'{round(clause_secs / 86400)}d'
            elif clause_secs > 3600:
                clause = f'{round(clause_secs / 3600)}h'
            elif clause_secs > 60:
                clause = f'{round(clause_secs / 60)}m'
            elif clause_secs > 0:
                clause = f'{clause_secs}s'
            perc_clause = None if clause_secs > 0 else round(((row[6] - row[5]) * 100) / row[5])
            result.append({"index": index, "player": row[0], "team": row[1], "pos": row[2], "status": row[3],
                           "manager": row[4], "sale_value": '{0:.2f}'.format(round(row[5] / 1000000, 2)),
                           "clause": clause, "perc_clause": perc_clause,
                           "change_3d": '{0:.2f}'.format(round(row[8] * row[5] / 100000000, 2)), "perc_chg_3d": row[8],
                           "points": row[9], "matches": row[10], "average": '{0:.2f}'.format(round(row[11] / 100, 2)),
                           "tag": row[12], "rival": row[13], "inout": row[14], "percentage": row[15]})
        return json.dumps(result)

    def get_team_status(self):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT team_money, team_value, points FROM managers WHERE id = "{self.config.get("team_id")}"')
        row = cursor.fetchone()
        money = round(row[0] / 1000000)
        value = round(row[1] / 1000000)
        points = row[2]
        return money, value, points

    def update_market(self):
        cursor = self.connection.cursor()
        market = self.api_client.get_market()
        cursor.execute('DELETE FROM market')
        cursor.executemany('INSERT INTO market(name,team,pos,status,buy_value,percent_change_3d,points,'
                           'matches,average,bids,myBid,seller) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', market)
        self.connection.commit()

    def update_next_match(self):
        cursor = self.connection.cursor()
        starting_teams = self.api_client.get_starting_teams()
        players = []
        for team in starting_teams:
            for player in team['players']:
                players.append((StartingTeamParser.teams_dict.get(team['team'], team['team']),
                                StartingTeamParser.players_dict.get(f"{team['team']}_{player}", player),
                                StartingTeamParser.teams_dict.get(team['rival'], team['rival']),
                                team['in_out'], team['players'][player]))
        cursor.execute('DELETE FROM next')
        cursor.executemany('INSERT INTO next(team,player,rival,inout,percentage) VALUES(?,?,?,?,?)', players)
        self.connection.commit()

    def update_operations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT status_value FROM status WHERE status_key = 'last_operation'")
        last_operation = cursor.fetchone()[0]
        sale_operations = []
        clause_updates = []
        buy_operations = []
        latest_operation = None
        for operation in self.api_client.get_operations():
            if datetime.fromisoformat(operation['timestamp']) > datetime.fromisoformat(last_operation):
                if operation['type'] == 'sale':
                    sale_operations.append(operation)
                # celif operation['type'] == 'buyout_updated':
                #     clause_updates.append((operation['player_id'], operation['money'] - operation['previous_money']))
                elif operation['type'] == 'purchase':
                    buy_operations.append((operation['player_id'], operation['name'], operation['pos'],
                                           operation['timestamp'], operation['money'], operation['to_from']))
                if latest_operation is None or operation['timestamp'] > latest_operation:
                    latest_operation = operation['timestamp']
        if buy_operations:
            cursor.executemany('INSERT INTO operations(player_id,name,pos,buy_tt,buy_value,seller) VALUES(?,?,?,?,?,?)',
                               buy_operations)
        for clause_update in clause_updates:
            cursor.execute(f"SELECT clause_update FROM operations "
                           f"WHERE player_id = '{clause_update[0]}' AND sale_tt IS NULL")
            previous_clause = cursor.fetchone()[0]
            cursor.execute(f"UPDATE operations SET clause_update = '{previous_clause + clause_update[1]}' "
                           f"WHERE player_id = '{clause_update[0]}' AND sale_tt IS NULL")
        for sale in sale_operations:
            buyer = 'NULL' if sale['to_from'] is None else f"'{sale['to_from']}'"
            cursor.execute(f"UPDATE operations SET sale_tt = '{sale['timestamp']}', sale_value = {sale['money']}, "
                           f"buyer = {buyer} WHERE player_id = '{sale['player_id']}' AND sale_tt IS NULL")
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

    def update_points(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM points')
        last_week = self.api_client.get_last_week_with_points()
        for i in range(1, last_week + 1):
            points = self.api_client.get_points(i)
            cursor.executemany(f'INSERT OR IGNORE INTO points(id, player, team, pos, j{i}) VALUES(?,?,?,?,?)', points)
            for player in points:
                if player[4] is not None:
                    cursor.execute(f"UPDATE points SET j{i} = {player[4]} WHERE id = '{player[0]}'")
        self.connection.commit()

    def update_status(self, cursor, key, value):
        cursor.execute(f"UPDATE status SET status_value = '{value}' where status_key = '{key}'")

    def tag_top_players(self, players):
        # 4 pos, 5 status, 8 sell value, 14 average
        sorted_players = sorted(sorted(players, key=lambda x: x[8]), key=lambda x: x[14], reverse=True)
        result = []
        goalkeepers = defenders = midfielders = strikers = 0
        for player in sorted_players:
            if player[5] != 'ok':
                result.append(player + (0,))
            elif player[4] == 1 and goalkeepers == 0:
                goalkeepers += 1
                result.append(player + (goalkeepers + defenders + midfielders + strikers,))
            elif player[4] == 2 and defenders < 5 and (defenders + midfielders) < 9 and (defenders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                defenders += 1
                result.append(player + (goalkeepers + defenders + midfielders + strikers,))
            elif player[4] == 3 and midfielders < 5 and (defenders + midfielders) < 9 and (midfielders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                midfielders += 1
                result.append(player + (goalkeepers + defenders + midfielders + strikers,))
            elif player[4] == 4 and strikers < 3 and (defenders + strikers) < 7 and (midfielders + strikers) < 7 \
                    and (defenders + midfielders + strikers) < 10:
                strikers += 1
                result.append(player + (goalkeepers + defenders + midfielders + strikers,))
            else:
                result.append(player + (0,))
        return result

    def update_teams(self):
        cursor = self.connection.cursor()
        teams = self.api_client.get_teams()
        managers_db = []
        players_db = []
        for team in teams:
            managers_db.append((team['id'], team['manager'], team['money'], team['value'], team['points']))
            team_players_db = []
            for player in team['players']:
                buy_tt = None
                buy_value = None
                if team['id'] == self.config.get('team_id'):
                    cursor.execute(f"SELECT buy_tt, buy_value FROM operations "
                                   f"WHERE player_id = {player[0]} AND sale_tt IS NULL")
                    buy_prices = cursor.fetchone()
                    buy_tt = buy_prices[0]
                    buy_value = buy_prices[1]
                team_players_db.append((player[0], team['id'], player[1], player[2], player[3],
                                        player[4], buy_tt, buy_value, player[5], player[6],
                                        player[7], player[8], player[9], player[10], player[11]))
            players_db.extend(self.tag_top_players(team_players_db))
        cursor.execute('DELETE FROM managers')
        cursor.executemany('INSERT INTO managers(id,manager,team_money,team_value,points) VALUES(?,?,?,?,?)',
                           managers_db)
        cursor.execute('DELETE FROM teams')
        cursor.executemany('INSERT INTO teams(id,manager_id,player,team,pos,status,buy_tt,buy_value,sale_value,'
                           'percent_change_3d,clause_value,clause_tt,points,matches,average,tag) '
                           'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', players_db)
        self.connection.commit()


if __name__ == "__main__":
    configuration = Config()
    database = Database(configuration)
    # database.update_operations()
    # print(database.get_operations())
    # database.update_teams()
    # print(database.get_team_status())
    # print(database.get_team())
    # print(database.get_rivals())
    # database.update_market()
    # print(database.get_market())
    # database.update_players()
    # print(database.get_players())
    # print(database.get_players_top())
    # database.update_points()
    # print(database.get_points())
    # database.update_next_match()
    # print(database.get_next_match())
