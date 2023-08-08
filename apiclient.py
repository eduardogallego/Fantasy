import json
import logging
import os
import requests

from time import time
from utils import Config


class ApiClient:

    def __init__(self, config):
        self.logger = logging.getLogger('api-client')
        self.config = config
        access_token = None
        token_type = None
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8,gl;q=0.7',
            'Origin': 'https://fantasy.laliga.com',
            'Referer': 'https://fantasy.laliga.com/',
            'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-App': 'Fantasy-web',
            'X-Lang': 'es'
        }
        self.auth_headers = self.headers.copy()
        self.auth_headers['Content-Type'] = 'application/json'
        while access_token is None or token_type is None:
            if os.path.isfile(config.get('credentials_file')):
                with open(config.get('credentials_file')) as input_file:
                    credentials = json.load(input_file)
                access_token = credentials['access_token']
                expires_on = credentials['expires_on']
                token_type = credentials['token_type']
                if int(time()) < expires_on:
                    break
            self.authenticate()
        self.headers['Access-Control-Allow-Credentials'] = 'true'
        self.headers['Access-Control-Allow-Origin'] = '*'
        self.headers['Authorization'] = f"{token_type} {access_token}"

    def authenticate(self):
        auth_dict = {"policy": "B2C_1A_ResourceOwnerv2", "username": self.config.get('user_name'),
                     "password": self.config.get('user_password')}
        response = requests.post(self.config.get("auth_url"), json=auth_dict, headers=self.auth_headers)
        if response.status_code != 200:
            self.logger.error('Authenticate %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        token_dict = {"code": response_dict['code'], "policy": "B2C_1A_ResourceOwnerv2"}
        response = requests.post(self.config.get("token_url"), json=token_dict, headers=self.auth_headers)
        if response.status_code != 200:
            self.logger.error('Token %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        with open(self.config.get('credentials_file'), 'w') as outfile:
            json.dump({'access_token': response_dict['access_token'], 'expires_on': response_dict['expires_on'],
                       'token_type': response_dict['token_type']}, outfile)

    def get_market(self):
        response = requests.get(self.config.get("market_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get market %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get market %s - Ok: %s' % (response.status_code, response_dict))
        response = []
        for entry in response_dict:
            position = entry['playerMaster']['positionId']
            if position == 5 or ('sellerTeam' in entry and entry['sellerTeam']['manager']['managerName'] == 'Edu'):
                continue  # manager position or mines
            player_id = entry['playerMaster']['id']
            player = entry['playerMaster']['nickname']
            team = entry['playerMaster']['team']['slug']
            status = entry['playerMaster']['playerStatus']
            value = entry['playerMaster']['marketValue']
            points = entry['playerMaster']['points']
            avgPoints = entry['playerMaster']['averagePoints']
            bids = entry['numberOfBids'] if 'numberOfBids' in entry else None
            myBid = entry['bid']['money'] if 'bid' in entry else None
            seller = entry['sellerTeam']['manager']['managerName'] if 'sellerTeam' in entry else None
            market_variation_3d = self.get_market_variation_3d(player_id)
            response.append((player, team, position, status, value, market_variation_3d,
                             points, avgPoints, bids, myBid, seller))
        return response

    def get_market_variation_3d(self, player_id):
        response = requests.get(self.config.get("market_value_url") % player_id, headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get player %s marked value %s - Error: %s'
                              % (player_id, response.status_code, response.reason))
        response_list = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get player %s marked value %s - Ok: %s' % (player_id, response.status_code, response_list))
        history_size = min(len(response_list), 3)
        end_value = response_list[len(response_list) - 1]['marketValue']
        ini_value = response_list[len(response_list) - history_size - 1]['marketValue']
        return round((end_value - ini_value) * 100 / ini_value)

    def get_operations(self):
        response = requests.get(self.config.get("history_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get operations %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get operations %s - Ok: %s' % (response.status_code, response_dict))
        response = []
        for operation in response_dict:
            operation_type = operation['operation']
            value = operation['money']
            timestamp = operation['date']
            player_id = operation['player']['id']
            player_name = operation['player']['nickname']
            player_position = operation['player']['positionId']
            response.append({"player_id": player_id, "name": player_name, "pos": player_position,
                             "type": operation_type, "value": value, "timestamp": timestamp})
        return response

    def get_players(self):
        response = requests.get(self.config.get("players_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get players %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get players %s - Ok: %s' % (response.status_code, response_dict))
        players = []
        for player in response_dict:
            position = player['positionId']
            if position == 5:
                continue;
            name = player['nickname']
            team = player['team']['slug']
            status = player['playerStatus']
            value = player['marketValue']
            points = player['points']
            average_points = player['averagePoints']
            last_season_points = player['lastSeasonPoints'] if 'lastSeasonPoints' in player else 0
            seller = player['manager']['managerName'] if 'manager' in player else None
            players.append((name, team, position, status, value, points, average_points, last_season_points, seller))
        return players

    def get_team(self):
        response = requests.get(self.config.get("team_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get team %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get team %s - Ok: %s' % (response.status_code, response_dict))
        manager = response_dict['manager']['managerName']
        team_money = response_dict['teamMoney']
        team_value = response_dict['teamValue']
        team_points = response_dict['teamPoints']
        team_dict = {'team_manager': manager, 'team_money': team_money,
                     'team_value': team_value, 'team_points': team_points}
        players = []
        for player in response_dict['players']:
            player_id = player['playerMaster']['id']
            name = player['playerMaster']['nickname']
            position = player['playerMaster']['positionId']
            value = player['playerMaster']['marketValue']
            status = player['playerMaster']['playerStatus']
            team = player['playerMaster']['team']['slug']
            points = player['playerMaster']['points']
            clause = player['buyoutClause']
            clause_tt = player['buyoutClauseLockedEndTime']
            percent_change_3d = self.get_market_variation_3d(player_id)
            players.append((player_id, name, team, position, status, value,
                            percent_change_3d, clause, clause_tt, points))
        return team_dict, players


if __name__ == "__main__":
    configuration = Config()
    api_client = ApiClient(configuration)
    # print(json.dumps(api_client.get_market()))
    # print(json.dumps(api_client.get_market_variation_3d('58')))
    # print(json.dumps(api_client.get_operations()))
    # print(json.dumps(api_client.get_players()))
    # team_dict, players = api_client.get_team()
    # print(json.dumps(team_dict))
    # print(json.dumps(players))
