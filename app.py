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

    db = endpoint.database()
    team = db.query(f'SELECT name FROM team WHERE code = "{code}"')
    teams_list = list(db.show('team')['name'])
    db.close()

    if type(team) != str:
        team = None

    return render_template('pages/teams.html', team=team, code=code, teams_list=teams_list)

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

if __name__=='__main__':
   app.run() 