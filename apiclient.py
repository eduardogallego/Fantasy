import json
import logging
import requests

from utils import Config


class ApiClient:

    def __init__(self, config):
        self.logger = logging.getLogger('api-client')
        self.config = config
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8,gl;q=0.7',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkNBdXdPcWRMN2YyXzlhTVhZX3ZkbEcyVENXbVV4aklXV1MwNVB4WHljcUkiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJOb3Qgc3VwcG9ydGVkIGN1cnJlbnRseS4gVXNlIG9pZCBjbGFpbS4iLCJleHRlbnNpb25fVXNlclByb2ZpbGVJZCI6IjYzNjFlM2M2LTU3OTUtNGNmNC05MzYzLTc3MDIzNDU1YjI1OSIsIm9pZCI6IjYzNjFlM2M2LTU3OTUtNGNmNC05MzYzLTc3MDIzNDU1YjI1OSIsImV4dGVuc2lvbl9FbWFpbFZlcmlmaWVkIjp0cnVlLCJhenAiOiJmZWM5ZTNmZC04Zjg4LTQ1YWItOGNiZC1iNzBiOWQ2NWRkZTAiLCJ2ZXIiOiIxLjAiLCJpYXQiOjE2OTEzMzY0NzAsImF1ZCI6ImZlYzllM2ZkLThmODgtNDVhYi04Y2JkLWI3MGI5ZDY1ZGRlMCIsImV4cCI6MTY5MTQyMjg3MCwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYWxpZ2EuZXMvMzM1MzE2ZWItZjYwNi00MzYxLWJiODYtMzVhN2VkY2RjZWMxL3YyLjAvIiwibmJmIjoxNjkxMzM2NDcwfQ.PwoPn4G-TTDPI98XdJe_io4FnOcuwDkYzxzQoNPT0TtXIlELN6DSRfIeuezcNF0eqnk97X3dga8ZPbaqFc-aCyvwKhRSjCC2pAw5xugt_UwkBXOtNPQsVm9ihHTNySrNXj7LaXs1vD0SXQf0LBKDHPNYWmM2hljJTA_XcGQCcuEldHsqiYfO-4JK5XW7sKK-2zRNySWS0mYKIMbvkLPvRZj7FO6xzejabH3VsfsCDTfhZc5G5Mc8qgEx9ORtFulqif2sTlcOObJf8TI0cMEObNEuJff8P-n8U7fXCHHUiAQeAzuUyhwrOk-yHYRI03YRC_LuHNtppp6MpCgnOh6R9Q',
            'Origin': 'https://fantasy.laliga.com',
            'Referer': 'https://fantasy.laliga.com/',
            'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-App': 'Fantasy-web',
            'X-Lang': 'es'
        }

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
            # print(player, team, position, status, value, market_variation_3d, points, avgPoints, bids, myBid, seller)
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
        # print(round((end_value - ini_value) * 100 / ini_value))
        return round((end_value - ini_value) * 100 / ini_value)

    def get_players(self):
        response = requests.get(self.config.get("team_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get players %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get players %s - Ok: %s' % (response.status_code, response_dict))
        manager = response_dict['manager']['managerName']
        team_money = response_dict['teamMoney']
        team_value = response_dict['teamValue']
        team_points = response_dict['teamPoints']
        # print(manager, team_money, team_value, team_points')
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
            percent_change_3d = self.get_market_variation_3d(player_id)
            # print(name, player_id, team, position, status, value, percent_change_3d, points')
            players.append((player_id, name, team, position, status, value, percent_change_3d, points))
        return team_dict, players

    def get_operations(self):
        response = requests.get(self.config.get("history_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get players %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get players %s - Ok: %s' % (response.status_code, response_dict))
        response = []
        for operation in response_dict:
            type = operation['operation']
            value = operation['money']
            timestamp = operation['date']
            player_id = operation['player']['id']
            player_name = operation['player']['nickname']
            player_position = operation['player']['positionId']
            # print((player_id, player_name, player_position, type, value, timestamp))
            response.append({"player_id": player_id, "name": player_name, "pos": player_position,
                             "type": type, "value": value, "timestamp": timestamp})
        return response


if __name__ == "__main__":
    configuration = Config()
    api_client = ApiClient(configuration)
    # api_client.get_operations()
    # api_client.get_players()
    # api_client.get_market_variation('230')
    api_client.get_market()
