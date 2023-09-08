import unicodedata

from html.parser import HTMLParser


class StartingTeamParser(HTMLParser):

    teams = ['alaves', 'almeria', 'athletic', 'atletico', 'barcelona', 'betis', 'cadiz', 'celta',
             'getafe', 'girona', 'granada', 'las-palmas', 'mallorca', 'osasuna', 'rayo-vallecano',
             'real-madrid', 'real-sociedad', 'sevilla', 'valencia', 'villarreal']
    teams_dict = {'alaves': 'd-alaves', 'almeria': 'ud-almeria', 'athletic': 'athletic-club',
                  'atletico': 'atletico-de-madrid', 'barcelona': 'fc-barcelona', 'betis': 'real-betis',
                  'cadiz': 'cadiz-cf', 'celta': 'rc-celta', 'getafe': 'getafe-cf', 'girona': 'girona-fc',
                  'granada': 'granada-cf', 'las-palmas': 'ud-las-palmas', 'mallorca': 'rcd-mallorca',
                  'osasuna': 'c-a-osasuna', 'rayo': 'rayo-vallecano', 'sevilla': 'sevilla-fc',
                  'valencia': 'valencia-cf', 'villarreal': 'villarreal-cf'}

    def __init__(self, team):
        super().__init__()
        self.team = team.replace('-vallecano', '')
        self.in_out = ''
        self.rival = ''
        self.status = ''
        self.player = ''
        self.players = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and self.status == '':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'juggador':
                    self.status = 'jug_a'
                    break
        elif tag == 'span' and self.status == 'jug_a':
            self.status = 'jug_s'
        elif tag == 'div' and self.status == '':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'row mini-match-info mb-2':
                    self.status = 'out'
                    break
        elif tag == 'img' and self.status in ['in', 'out']:
            for attr in attrs:
                if attr[0] == 'alt':
                    found_team = unicodedata.normalize('NFKD', attr[1].replace(' ', '-'))\
                        .encode('ASCII', 'ignore').decode('utf-8').lower()
                    if found_team != self.team:
                        self.rival = found_team
                        self.in_out = self.status
                        self.status = ''
                    else:
                        self.status = 'in'
                    break

    def handle_endtag(self, tag):
        if tag == 'span' and self.status == 'jug_s':
            self.status = 'jug_p'

    def handle_data(self, data):
        if self.status == 'jug_s':
            self.player = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore').decode('utf-8').lower()
        elif self.status == 'jug_p' and '%' in data:
            self.players.append((self.player, data.strip()[:-1]))
            self.status = ''
