from flask import *
import endpoint

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/teams/')
def teams():
    code = request.args.get('team')

    data = endpoint.teams(code)

    return render_template('pages/teams.html', data=data)

@app.route('/scores/')
def scores():
    date = request.args.get('date')
    conf = request.args.get('conf')

    data = endpoint.scores(date, conf)

    return render_template('pages/scores.html', data=data)

@app.route('/stats/')
def stats():
    return render_template('pages/stats.html')

@app.route('/rankings/')
def rankings():
    season = request.args.get('season')
    conf = request.args.get('conf')

    data = endpoint.rankings(season, conf)

    return render_template('pages/rankings.html', data=data)

@app.route('/standings/')
def standings():
    return render_template('pages/standings.html')

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