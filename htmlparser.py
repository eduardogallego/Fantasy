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
    players_dict = {
        'alaves_Rebbach': 'A. Rebbach', 'alaves_Benavidez': 'C. Benavidez', 'alaves_R. Duarte': 'Duarte',
        'alaves_Hagi': 'Ianis Hagi', 'alaves_Omorodion': 'Samu',
        'almeria_Puigmal': 'Arnau Puigmal', 'almeria_Luis Maximiano': 'Maximiano',
        'athletic_Ares': 'Adu Ares', 'athletic_Herrera': 'Ander Herrera',
        'athletic_R. de Galarreta': 'De Galarreta', 'athletic_I. Williams': 'Iñaki Williams',
        'athletic_N. Williams': 'Nico Williams', 'athletic_Unai G': 'Unai Gómez',
        'atletico_M. Llorente': 'Marcos Llorente', 'atletico_Grbic': 'Grbić',
        'atletico_Galán': 'Javi Galán', 'atletico_Molina': 'Nahuel Molina',
        'barcelona_Gündogan': 'Gundogan', 'barcelona_Íñigo': 'Iñigo Martínez', 'barcelona_Cancelo': 'Joao Cancelo',
        'barcelona_Yamal': 'Lamine Yamal', 'barcelona_Romeu': 'Oriol Romeu', 'barcelona_F. de Jong': 'De Jong',
        'barcelona_A. Christensen': 'Christensen', 'barcelona_Fermín': 'Fermin', 'barcelona_Ferran': 'Ferran Torres',
        'barcelona_João Félix': 'Joao Félix', 'barcelona_M. Alonso': 'Marcos Alonso',
        'barcelona_S. Roberto': 'Sergi Roberto', 'barcelona_Balde': 'Álex Balde',
        'betis_Ayoze': 'Ayoze Pérez',
        'cadiz_Ramos': 'Chris Ramos',
        'celta_Domínguez': 'Carlos Domínguez', 'celta_Beltrán': 'Fran Beltrán',
        'celta_Strand Larsen': 'Larsen', 'celta_Núñez': 'Unai Nuñez',
        'getafe_Soria': 'David Soria',
        'girona_Blind': 'Daley Blind', 'girona_Miguel': 'Miguel Gutiérrez', 'girona_Savinho': 'Sávio',
        'girona_Herrera': 'Yangel Herrera',
        'las-palmas_Alex Suárez': 'Álex Suárez', 'las-palmas_J. Araujo': 'Araujo', 'las-palmas_Viera': 'Jonathan Viera',
        'las-palmas_Marmol': 'Mika Marmol', 'las-palmas_Kaba': 'Sory Kaba',
        'osasuna_Rubén G.': 'Rubén García', 'osasuna_Oroz': 'Aimar Oroz', 'osasuna_Aitor': 'Aitor Fdez.',
        'osasuna_Chimy': 'Chimy Ávila', 'osasuna_Ibáñez': 'Ibañez', 'osasuna_Muñoz': 'Iker Muñoz',
        'osasuna_Arnáiz': 'Jose Arnaiz', 'osasuna_Herrera': 'Sergio Herrera',
        'rayo_Valentín': 'Óscar Valentín',
        'real-madrid_Lucas': 'Lucas Vázquez', 'real-madrid_Güler': 'Arda Güler',
        'real-madrid_Kepa': 'Arrizabalaga', 'real-madrid_Vinícius': 'Vinícius Jr',
        'real-sociedad_Brais': 'Brais Méndez',
        'valencia_Javi Guerra': 'Guerra', 'valencia_Duro': 'Hugo Duro', 'valencia_Gayà': 'Gayá',
        'villarreal_Sörloth': 'Sorloth', 'villarreal_Baena': 'Álex Baena'
    }

    def __init__(self, team):
        super().__init__()
        self.team = team.replace('-vallecano', '')
        self.in_out = ''
        self.rival = ''
        self.status = ''
        self.player = ''
        self.players = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.status == '':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'juggadores':
                    self.status = 'player_container'
                    break
                elif attr[0] == 'class' and attr[1] == 'row mini-match-info mb-2':
                    self.status = 'out'
                    break
        elif tag == 'span' and self.status == 'player_container':
            self.status = 'player'
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
        if tag == 'span' and self.status == 'player':
            self.status = 'player_percentage'

    def handle_data(self, data):
        if self.status == 'player':
            self.player = data.strip()
            self.status = 'player_percentage'
        elif self.status == 'player_percentage' and '%' in data:
            self.players.append((self.player, data.strip()[:-1]))
            self.status = ''
