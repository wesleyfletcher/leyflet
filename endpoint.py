from database import database
import datetime

def teams(code):
    data = {}

    if code:
        db = database()
        name = db.query(f'SELECT name FROM team WHERE code = "{code}"')
        db.close()

        if type(name) == str:
            data['list'] = False

            data['name'] = name
            data['code'] = code

            ## other team info sheets

            return data
    
    data['list'] = True

    db = database()
    team_table = db.query('SELECT name, code FROM team ORDER BY name ASC')
    db.close()

    data['teams'] = []
    for i in range(len(team_table)):
        row = team_table.loc[i]
        data['teams'].append({
            'name' : row['name'],
            'code' : row['code']
        })
    
    return data

def scores(date, conf):
    data = {}

    today = datetime.date.today() if not date else datetime.date.fromisoformat(date)

    previous = str(today - datetime.timedelta(days=1)).replace('-', '')
    next     = str(today + datetime.timedelta(days=1)).replace('-', '')

    data['date'] = {
        'today' : today.strftime('%B %d, %Y'),
        'previous' : previous,
        'next' : next
    }

    conf = '' if not conf else conf.replace('_', ' ')
    data['conf'] = conf.replace(' ', '_')

    db = database()
    scores_table = db.runfile('scores_table', today=today, conf=conf)
    db.close()

    data['scores'] = []
    for i in range(len(scores_table)):
        row = scores_table.loc[i]
        data['scores'].append({
            'id' : row['id'],
            'home_team' : row['home_team'], 'home_code' : row['home_team_code'],
            'away_team' : row['away_team'], 'away_code' : row['away_team_code'],
            'neutral' : bool(row['neutral']), 'overtimes' : int(row['overtimes']),
            'home_score' : int(row['home_score']), 'away_score' : int(row['away_score']),
            'home_score_1h' : int(row['home_score_1h']), 'away_score_1h' : int(row['away_score_1h']),
            'home_score_2h' : int(row['home_score_2h']), 'away_score_2h' : int(row['away_score_2h']),
            'home_score_ot' : int(row['home_score_ot']) if row['home_score_ot'] else None,
            'away_score_ot' : int(row['away_score_ot']) if row['away_score_ot'] else None
        })

    return data

def stats():
    pass

def rankings():
    pass

def standings(season, conf):
    data = {}

    season = 2025 if not season else season
    conf = '' if not conf else conf.replace('-', ' ')

    db = database()

    conf_standings = db.runfile('conf_standings', conf=conf, season=season)

    db.close()

    for i in range(len(conf_standings)):
        row = conf_standings.loc[i]

        if row['conf'] not in data:
            data[row['conf']] = []
        
        data[row['conf']].append({
            'team' : row['team'],
            'conf_wins'   : int(row['conf_wins']),
            'conf_losses' : int(row['conf_losses']),
            'conf_pct'    : '{:0.3f}'.format(row['season_pct']).lstrip('0'),

            'season_wins'   : int(row['season_wins']),
            'season_losses' : int(row['season_losses']),
            'season_pct'    : '{:0.3f}'.format(row['season_pct']).lstrip('0'),

            'home_record' : f'{row['home_wins']}-{row['home_losses']}',
            'away_record' : f'{row['away_wins']}-{row['away_losses']}',
            'neutral_record' : f'{row['neutral_wins']}-{row['neutral_losses']}'
        })

    return data

def bracket():
    pass

def games(id):
    data = {}

    db = database()

    game_table = db.runfile('game_table', id=id)
    stat_table = db.runfile('box_score', id=id)
    play_table = db.runfile('play_table', id=id)

    db.close()

    if len(game_table) == 0:
        raise ValueError("Game does not exist")
    
    game_table = game_table.loc[0]

    ## General info

    data['status'] = game_table['status']
    data['game_date'] = game_table['game_date'].strftime("%B %d, %Y")

    data['home_team'], data['away_team'] = game_table['home_team'], game_table['away_team']
    data['home_code'], data['away_code'] = game_table['home_team_code'], game_table['away_team_code']

    data['home_score'], data['away_score'] = int(game_table['home_score']), int(game_table['away_score'])
    data['home_score_1h'], data['away_score_1h'] = int(game_table['home_score_1h']), int(game_table['away_score_1h'])
    data['home_score_2h'], data['away_score_2h'] = int(game_table['home_score_2h']), int(game_table['away_score_2h'])

    data['home_score_ot'] = int(game_table['home_score_ot']) if game_table['home_score_ot'] else None
    data['away_score_ot'] = int(game_table['away_score_ot']) if game_table['away_score_ot'] else None

    data['neutral'] = bool(game_table['neutral'])
    data['overtimes'] = int(game_table['overtimes'])

    ## Stats

    data['stats'] = {data['away_team'] : [], data['home_team'] : []}
    for i in range(len(stat_table)):
        row = stat_table.loc[i]

        data['stats'][row['team']].append({
            'lname' : row['lname'],
            'fname' : row['fname'],
            'suffix' : ' ' + row['suffix'] if row['suffix'] else '',

            'min' : int(row['min']),
            'pts' : int(row['pts']),
            'fgm' : int(row['fgm']),
            'fga' : int(row['fga']),
            'tpm' : int(row['tpm']),
            'tpa' : int(row['tpa']),
            'ftm' : int(row['ftm']),
            'fta' : int(row['fta']),

            'reb' : int(row['reb']),
            'ast' : int(row['ast']),
            'to'  : int(row['to']),
            'stl' : int(row['stl']),
            'blk' : int(row['blk']),

            'oreb' : int(row['oreb']),
            'dreb' : int(row['dreb']),
            'pf' : int(row['pf'])
        })

    ## Plays

    data['plays'] = {}
    for i in range(len(play_table)):
        row = play_table.loc[i]

        if row['half'] not in data['plays']:
            data['plays'][row['half']] = []

        data['plays'][row['half']].append({
            'type'   : row['type'],
            'text'   : row['text'],
            'clock'  : str(row['clock'])[:5],
            'team'   : row['team'],
            'player' : int(row['player']) if row['player'] else None,
            'points' : int(row['points'])
        })

    return data

def players(id):
    pass