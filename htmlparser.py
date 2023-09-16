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
        'almeria_Puigmal': 'Arnau Puigmal', 'almeria_Luis Maximiano': 'Maximiano', 'almeria_Édgar': 'Edgar',
        'almeria_Koné': 'Kone', 'almeria_Baptistão': 'Leo Baptistao', 'almeria_Lazaro': 'Lázaro',
        'almeria_Pubill': 'Marc Pubill', 'almeria_Lopy': 'Dion',
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
        'betis_Ayoze': 'Ayoze Pérez', 'betis_Iglesias': 'Borja Iglesias', 'betis_Bravo': 'Claudio Bravo',
        'betis_Guido': 'Guido Rodríguez', 'betis_Y. Sabaly': 'Sabaly', 'betis_Carvalho': 'William Carvalho',
        'cadiz_Ramos': 'Chris Ramos', 'cadiz_Ocampo': 'Brian Ocampo', 'cadiz_Iza Carcelén': 'Iza',
        'cadiz_José Mari': 'Jose Mari', 'cadiz_Momo': 'Momo Mbaye', 'cadiz_Guardiola': 'Sergi Guardiola',
        'celta_Domínguez': 'Carlos Domínguez', 'celta_Beltrán': 'Fran Beltrán', 'celta_Núñez': 'Unai Nuñez',
        'celta_Strand Larsen': 'Larsen', 'celta_De la Torre': 'De La Torre', 'celta_Sotelo': 'Hugo Sotelo',
        'celta_Kevin': 'Kevin Vázquez', 'celta_Miguel': 'Miguel Rodríguez',
        'getafe_Soria': 'David Soria', 'getafe_Mayoral': 'Borja Mayoral', 'getafe_D. Duarte': 'Domingos Duarte',
        'getafe_Iglesias': 'Juan Iglesias', 'getafe_Luis Milla': 'Milla',
        'girona_Blind': 'Daley Blind', 'girona_Miguel': 'Miguel Gutiérrez', 'girona_Savinho': 'Sávio',
        'girona_Herrera': 'Yangel Herrera', 'girona_Arnau': 'Arnau Mtnez.', 'girona_Kébé': 'Ibrahima Kebé',
        'granada_Adri López': 'Adri Lopez', 'granada_Callejón': 'Callejon', 'granada_F. Diédhiou': 'Diedhiou',
        'granada_Villar': 'Gonzalo Villar', 'granada_I. Miquel': 'Miquel', 'granada_Raúl F.': 'Raúl F',
        'granada_Ferreira': 'André F.', 'granada_Puertas': 'Antonio Puertas',
        'las-palmas_Alex Suárez': 'Álex Suárez', 'las-palmas_J. Araujo': 'Araujo', 'las-palmas_Viera': 'Jonathan Viera',
        'las-palmas_Marmol': 'Mika Marmol', 'las-palmas_Kaba': 'Sory Kaba', 'las-palmas_Aarón': 'Aarón Escandell',
        'las-palmas_S. Cardona': 'Cardona', 'las-palmas_M. Cardona': 'Marc', 'las-palmas_Saúl Coco': 'Coco',
        'las-palmas_Curbelo': 'E. Curbelo', 'las-palmas_Iñaki González': 'Iñaki', 'las-palmas_Muñoz': 'Javi Muñoz',
        'las-palmas_Á. Lemos': 'Lemos S', 'las-palmas_Perrone': 'Máximo Perrone',
        'mallorca_Abdon': 'Abdón', 'mallorca_Antonio': 'Antonio Sánchez', 'mallorca_Cuéllar': 'Cuellar',
        'mallorca_Giovanni': 'Gio González', 'mallorca_Van Der Heyden': 'Heyden', 'mallorca_Costa': 'Jaume Costa',
        'mallorca_Samú': 'Samu Costa',
        'osasuna_Rubén G.': 'Rubén García', 'osasuna_Oroz': 'Aimar Oroz', 'osasuna_Aitor': 'Aitor Fdez.',
        'osasuna_Chimy': 'Chimy Ávila', 'osasuna_Ibáñez': 'Ibañez', 'osasuna_Muñoz': 'Iker Muñoz',
        'osasuna_Arnáiz': 'Jose Arnaiz', 'osasuna_Herrera': 'Sergio Herrera',
        'rayo_Valentín': 'Óscar Valentín', 'rayo_Pep Chavarría': 'Chavarría', 'rayo_Méndez': 'Diego Méndez',
        'rayo_Pozo': 'José Pozo', 'rayo_De Tomás': 'RDT',
        'real-madrid_Lucas': 'Lucas Vázquez', 'real-madrid_Güler': 'Arda Güler',
        'real-madrid_Kepa': 'Arrizabalaga', 'real-madrid_Vinicius': 'Vinícius Jr',
        'real-sociedad_Brais': 'Brais Méndez', 'real-sociedad_Carlos': 'Carlos Fernández',
        'real-sociedad_González de Zarate': 'De Zarate', 'real-sociedad_Pacheco': 'Jon Pacheco',
        'real-sociedad_Tierney': 'Kieran Tierney', 'real-sociedad_Merino': 'Mikel Merino',
        'real-sociedad_Ali Cho': 'Momo Cho', 'real-sociedad_Marín': 'Pablo Marín',
        'sevilla_En Nesyri': 'En-Nesyri', 'sevilla_Jordan': 'Jordán', 'sevilla_Lukebakio': 'Lukébakio',
        'sevilla_Marcão': 'Marcao', 'sevilla_Rakitic': 'Rakitić', 'sevilla_Óliver': 'Óliver Torres',
        'sevilla_Ramos': 'Sergio Ramos',
        'valencia_Javi Guerra': 'Guerra', 'valencia_Duro': 'Hugo Duro', 'valencia_Gayà': 'Gayá',
        'valencia_Gabriel': 'Gabriel Paulista', 'valencia_Alberto Marí': 'Marí', 'valencia_Mosquera': 'Cristhian',
        'valencia_Yaremchuk': 'Roman Yaremchuk', 'valencia_Thierry': 'Thierry Correia', 'valencia_Özkacar': 'Cenk',
        'villarreal_Sörloth': 'Sorloth', 'villarreal_Baena': 'Álex Baena', 'villarreal_A. Moreno': 'Alberto Moreno',
        'villarreal_Femenia': 'Kiko Femenía', 'villarreal_Reina': 'Pepe Reina', 'villarreal_Yéremi': 'Yéremy Pino'
    }

    def __init__(self, team):
        super().__init__()
        self.team = team.replace('-vallecano', '')
        self.in_out = ''
        self.rival = ''
        self.status = ''
        self.player = ''
        self.players = {}

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
        elif tag == 'div' and self.status == 'player_percentage' and self.player not in self.players:
            self.players[self.player] = None
            self.status = ''

    def handle_data(self, data):
        if self.status == 'player':
            self.player = data.strip()
            self.status = 'player_percentage'
        elif self.status == 'player_percentage' and '%' in data:
            self.players[self.player] = data.strip()[:-1]
            self.status = ''
