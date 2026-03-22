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
    game_table = db.query(f'''
        SELECT *,
            home_code.code AS home_team_code,
            away_code.code AS away_team_code
        FROM game
                          
        JOIN complete
        USING (id)
                          
        JOIN team AS home_code
        ON game.home_team = home_code.name
        
        JOIN team AS away_code
        ON game.away_team = away_code.name
                          
        JOIN member AS home_conf
        ON game.home_team = home_conf.team
            AND game.season = home_conf.season
                          
        JOIN member AS away_conf
        ON game.away_team = away_conf.team
            AND game.season = away_conf.season
        
        WHERE game_date = '{today}'
        AND (home_conf.conf LIKE '%{conf}%'
            OR away_conf.conf LIKE '%{conf}%')
    ''')
    db.close()

    data['scores'] = []
    for i in range(len(game_table)):
        row = game_table.loc[i]
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

def standings():
    pass

def bracket():
    pass

def game(id):
    data = {}

    db = database()

    game_table = db.query(f'''
        SELECT *,
            home_code.code AS home_team_code,
            away_code.code AS away_team_code
        FROM game
                          
        JOIN complete
        USING (id)
                          
        JOIN team AS home_code
        ON game.home_team = home_code.name
        
        JOIN team AS away_code
        ON game.away_team = away_code.name

        WHERE id = {id}
    ''')

    play_table = db.query(f'''
        SELECT *
        FROM play
        WHERE game = {id}
        ORDER BY seq                
    ''')

    db.close()

    if len(game_table) == 0:
        raise ValueError("Game does not exist")
    
    game_table = game_table.loc[0]

    data['status'] = game_table['status']
    data['game_date'] = game_table['game_date']

    data['home_team'], data['away_team'] = game_table['home_team'], game_table['away_team']
    data['home_code'], data['away_code'] = game_table['home_team_code'], game_table['away_team_code']

    data['home_score'], data['away_score'] = int(game_table['home_score']), int(game_table['away_score'])
    data['home_score_1h'], data['away_score_1h'] = int(game_table['home_score_1h']), int(game_table['away_score_1h'])
    data['home_score_2h'], data['away_score_2h'] = int(game_table['home_score_2h']), int(game_table['away_score_2h'])

    data['home_score_ot'] = int(game_table['home_score_ot']) if game_table['home_score_ot'] else None
    data['away_score_ot'] = int(game_table['away_score_ot']) if game_table['away_score_ot'] else None

    data['neutral'] = bool(game_table['neutral'])
    data['overtimes'] = int(game_table['overtimes'])

    data['plays'] = {'1H' : [], '2H' : [], 'OT' : []}
    for i in range(len(play_table)):
        row = play_table.loc[i]

        data['plays'][row['half'][-2:]].append({
            'type' : row['type'],
            'text' : row['text'],
            'clock' : str(row['clock'])[:5],
            'team' : row['team'],
            'player' : int(row['player']) if row['player'] else None,
            'points' : int(row['points'])
        })

    return data