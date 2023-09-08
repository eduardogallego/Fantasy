import json
import logging
import os

from apiclient import ApiClient
from database import Database
from datetime import timedelta
from flask import Flask, redirect, render_template, request, send_from_directory
from flask_login import LoginManager, login_required, login_user
from utils import Config, Logger, User
from werkzeug import serving

Logger()
serving._log_add_style = False          # disable colors in werkzeug server
logger = logging.getLogger('server')
config = Config()
app = Flask(__name__)
app.secret_key = config.get('secret_key')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
user = User(config.get('team_id'), config.get('user_name'), config.get('user_password'))


@login_manager.user_loader
def load_user(user_id):
    return user if user.get_id() == user_id else None


@app.route('/login', methods=['GET'])
def login():
    return render_template("login_form.html", error=None)


@app.route('/login_action', methods=['POST'])
def login_action():
    form_user = request.form['user']
    form_password = request.form['password']
    if user.get_user_name() == form_user and user.login(form_password) \
            and login_user(user=user, remember=True, duration=timedelta(days=30)):
        logger.info("User %s authenticated" % form_user)
        return redirect("/team")
    else:
        user.logout()
        logger.warning("Authentication error %s %s" % (form_user, form_password))
        return render_template("login_form.html", error="Authentication error: wrong user/pwd")


@app.route('/', methods=['GET'])
@login_required
def root():
    return redirect("/team")


@app.route('/market', methods=['GET'])
@login_required
def market():
    database = Database(config)
    money, value, points = database.get_team_status()
    return render_template("market.html", points=points, cash=money, team=value, total=(money + value))


@app.route('/market.json', methods=['GET'])
def market_json():
    database = Database(config)
    return database.get_market()


@app.route('/next_match', methods=['GET'])
@login_required
def next_match():
    database = Database(config)
    money, value, points = database.get_team_status()
    return render_template("next_match.html", points=points, cash=money, team=value, total=(money + value))


@app.route('/next_match.json', methods=['GET'])
def next_match_json():
    database = Database(config)
    return database.get_next_match()


@app.route('/news', methods=['GET'])
@login_required
def news():
    database = Database(config)
    money, value, points = database.get_team_status()
    return render_template("news.html", points=points, cash=money, team=value, total=(money + value))


@app.route('/news.json', methods=['GET'])
def news_json():
    api_client = ApiClient(config)
    return json.dumps(api_client.get_news())


@app.route('/players', methods=['GET'])
@login_required
def players():
    database = Database(config)
    money, value, points = database.get_team_status()
    return render_template("players.html", points=points, cash=money, team=value, total=(money + value))


@app.route('/players.json', methods=['GET'])
def players_json():
    database = Database(config)
    return database.get_players()


@app.route('/players_top.json', methods=['GET'])
def players_top_json():
    database = Database(config)
    return database.get_players_top()


@app.route('/operations', methods=['GET'])
@login_required
def operations():
    database = Database(config)
    money, value, points = database.get_team_status()
    return render_template("operations.html", points=points, cash=money, team=value, total=(money + value))


@app.route('/operations.json', methods=['GET'])
def operations_json():
    database = Database(config)
    return database.get_operations()


@app.route('/points', methods=['GET'])
@login_required
def points():
    database = Database(config)
    money, value, team_points = database.get_team_status()
    return render_template("points.html", points=team_points, cash=money, team=value, total=(money + value))


@app.route('/points.json', methods=['GET'])
def points_json():
    database = Database(config)
    return database.get_points()


@app.route('/team', methods=['GET'])
@login_required
def team():
    database = Database(config)
    money, value, points = database.get_team_status()
    return render_template("team.html", points=points, cash=money, team=value, total=(money + value))


@app.route('/team.json', methods=['GET'])
def team_json():
    database = Database(config)
    return database.get_team()


@app.route('/rivals.json', methods=['GET'])
def rivals_json():
    database = Database(config)
    return database.get_rivals()


@app.route('/update_market', methods=['GET'])
def update_market():
    database = Database(config)
    database.update_market()
    return redirect("/market")


@app.route('/update_next_match', methods=['GET'])
def update_next_match():
    database = Database(config)
    database.update_next_match()
    return redirect("/next_match")


@app.route('/update_operations', methods=['GET'])
def update_operations():
    database = Database(config)
    database.update_operations()
    return redirect("/operations")


@app.route('/update_players', methods=['GET'])
def update_players():
    database = Database(config)
    database.update_players()
    return redirect("/players")


@app.route('/update_points', methods=['GET'])
def update_points():
    database = Database(config)
    database.update_points()
    return redirect("/points")


@app.route('/update_team', methods=['GET'])
def update_team():
    database = Database(config)
    database.update_operations()
    database.update_teams()
    return redirect("/team")


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/images/<image>', methods=['GET'])
def get_image(image):
    return send_from_directory(os.path.join(app.root_path, 'images'), image)


@app.route('/web/<resource>', methods=['GET'])
def get_resource(resource):
    return send_from_directory(os.path.join(app.root_path, 'web'), resource)


debug_mode = config.get('debug_mode') == 'True'
app.run(host='0.0.0.0', port=config.get('port'), debug=debug_mode)
