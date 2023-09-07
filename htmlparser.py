from html.parser import HTMLParser


class StartingTeamParser(HTMLParser):

    def __init__(self, team):
        super().__init__()
        self.team = team
        self.local = ''
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
        elif tag == 'section' and self.status == '':
            self.status = 'nxt_s'
        elif tag == 'div':
            if self.status == 'nxt_s':
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'equipo local':
                        self.status = 'visitante'
            elif self.status == 'visitante':
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'equipo visitante':
                        self.status = 'local'
        elif tag == 'img' and self.status in ['local', 'visitante']:
            for attr in attrs:
                if attr[0] == 'alt' and attr[1][:3].lower() != self.team[:3]:
                    self.rival = attr[1]
                    self.local = self.status
                    self.status = ''
        # print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if tag == 'span' and self.status == 'jug_s':
            self.status = 'jug_p'
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.status == 'jug_s':
            self.player = data
        elif self.status == 'jug_p' and '%' in data:
            self.players.append((self.player, data.strip()[:-1]))
            self.status = ''
        # print("Encountered some data  :", data)
