from flask import *

import endpoint

app = Flask(__name__)

@app.errorhandler(Exception)
def error(e):
    return render_template('error.html', error=f'{e} {type(e)}')

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/teams/')
def teams_list():
    data = endpoint.teams_list()
    return render_template('pages/teams_list.html', data=data)

@app.route('/teams/<code>')
def teams(code):
    season = request.args.get('season')

    data = endpoint.teams(code, season)

    return render_template('pages/teams.html', data=data)

@app.route('/scores/', methods=['GET', 'POST'])
def scores():
    date = request.args.get('date')
    conf = request.args.get('conf')

    data = endpoint.scores(date, conf)

    return render_template('pages/scores.html', data=data)

@app.route('/stats/')
def stats():
    season = request.args.get('season')
    conf = request.args.get('conf')
    page = request.args.get('page')

    data = endpoint.stats(season, conf, page)

    return render_template('pages/stats.html', data=data)

@app.route('/rankings/')
def rankings():
    season = request.args.get('season')
    conf = request.args.get('conf')

    data = endpoint.rankings(season, conf)

    return render_template('pages/rankings.html', data=data)

@app.route('/standings/')
def standings():

    season = request.args.get('season')
    conf = request.args.get('conf')

    data = endpoint.standings(season, conf)

    return render_template('pages/standings.html', data=data)

@app.route('/bracket/')
def bracket():
    return render_template('pages/bracket.html')

@app.route('/games/<id>')
def games(id):
    data = endpoint.games(id)

    return render_template('pages/games.html', data=data)

@app.route('/players/<id>')
def players(id):
    data = endpoint.players(id)

    return render_template('pages/players.html', data=data)

if __name__=='__main__':
   app.run() 