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
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkNBdXdPcWRMN2YyXzlhTVhZX3ZkbEcyVENXbVV4aklXV1MwNVB4WHljcUkiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJOb3Qgc3VwcG9ydGVkIGN1cnJlbnRseS4gVXNlIG9pZCBjbGFpbS4iLCJleHRlbnNpb25fVXNlclByb2ZpbGVJZCI6IjYzNjFlM2M2LTU3OTUtNGNmNC05MzYzLTc3MDIzNDU1YjI1OSIsIm9pZCI6IjYzNjFlM2M2LTU3OTUtNGNmNC05MzYzLTc3MDIzNDU1YjI1OSIsImV4dGVuc2lvbl9FbWFpbFZlcmlmaWVkIjp0cnVlLCJhenAiOiJmZWM5ZTNmZC04Zjg4LTQ1YWItOGNiZC1iNzBiOWQ2NWRkZTAiLCJ2ZXIiOiIxLjAiLCJpYXQiOjE2OTEyNDkwMDIsImF1ZCI6ImZlYzllM2ZkLThmODgtNDVhYi04Y2JkLWI3MGI5ZDY1ZGRlMCIsImV4cCI6MTY5MTMzNTQwMiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYWxpZ2EuZXMvMzM1MzE2ZWItZjYwNi00MzYxLWJiODYtMzVhN2VkY2RjZWMxL3YyLjAvIiwibmJmIjoxNjkxMjQ5MDAyfQ.XWXzh9CRaoAi7JY9LeQn-e-0y4Rj2AnJprb3AP2Ym_P34CUBO-8g3kG1jq2kcAO61eg0JfZ-_UlwwHCjfgzZWrm7FVeKdf7axItmN5LXgSUpxn4_Mi3HE5bjxrgJUQMsYboEH2C1w_bov8_32tnYUN90VIR5cZpuSZLcAo55W6LlA7dXnOCUQzDnatZRGcEC2fyadOqU897rTqiInJwbKQCMrV-z33QL5BcBjNVE3OFlqr3qwi7zccaLpqm8f9tSEeWNO_z9jah16nLXgAwOeS7e6Hn2PYbMRk02kNiSzqoCEoCIPNW2RTKZCe_n-EC7Pd36npny_9uEpsrCeWvF_w',
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

    def get_players(self):
        response = requests.get(config.get("team_url"), headers=self.headers)
        if response.status_code != 200:
            self.logger.error('Get players %s - Error: %s' % (response.status_code, response.reason))
        response_dict = json.loads(response.text.encode().decode('utf-8-sig'))
        self.logger.info('Get players %s - Ok: %s' % (response.status_code, response_dict))
        print('Get players %s - Ok: %s' % (response.status_code, response_dict))
        manager = response_dict['manager']['managerName']
        team_money = response_dict['teamMoney']
        team_value = response_dict['teamValue']
        team_points = response_dict['teamPoints']
        team_players = response_dict['playersNumber']
        print(f'{manager} - Cash: {team_money}, Team ({team_players}): {team_value}, Points {team_points}')
        for player in response_dict['players']:
            player_name = player['playerMaster']['nickname']
            player_value = player['buyoutClause']
            player_status = player['playerMaster']['playerStatus']
            player_team = player['playerMaster']['team']['name']
            player_slug = player['playerMaster']['team']['slug']
            player_points = player['playerMaster']['points']
            print(f'- {player_name}, {player_team}, {player_slug}, {player_status}, {player_value}, {player_points}')


if __name__ == "__main__":
    config = Config()
    web_client = ApiClient(config)
    web_client.get_players()
