from flask import *
from database import database

import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/teams/')
def teams():
    team = request.args.get('team')

    db = database()
    teams_list = list(db.show('team')['name'])
    db.close()

    return render_template('pages/teams.html', team=team, teams_list=teams_list)

@app.route('/scores/')
def scores():
    dt = request.args.get('date')

    if dt:
        dt = datetime.date.fromisoformat(dt)
    else:
        dt = datetime.date.today()

    previous = str(dt - datetime.timedelta(days=1)).replace('-', '')
    next     = str(dt + datetime.timedelta(days=1)).replace('-', '')

    date_str = dt.strftime('%B %d, %Y')

    db = database()
    game_table = db.query(f'SELECT * FROM game JOIN complete USING (id) WHERE game_date = "{dt}"')
    db.close()

    games = []
    for i in range(len(game_table)):
        row = game_table.loc[i]

        games.append({
            'home_team'  : row['home_team'],
            'away_team'  : row['away_team'],
            'home_score' : row['home_score'],
            'away_score' : row['away_score']     
        })

    return render_template('pages/scores.html', date=date_str, previous=previous, next=next, games=games)

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