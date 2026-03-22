from flask import *
import endpoint

import datetime

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
    return render_template('pages/rankings.html')

@app.route('/standings/')
def standings():
    return render_template('pages/standings.html')

@app.route('/bracket/')
def bracket():
    return render_template('pages/bracket.html')

@app.route('/game/<id>')
def game(id):
    data = endpoint.game(id)

    return render_template('pages/game.html', data=data)

if __name__=='__main__':
   app.run() 