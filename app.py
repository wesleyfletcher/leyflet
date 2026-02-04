from flask import *
from database import database

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/teams/')
def teams():
    team = request.args.get('team')
    return render_template('pages/teams.html', team=team)

@app.route('/scores/')
def scores():
    return render_template('pages/scores.html')

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