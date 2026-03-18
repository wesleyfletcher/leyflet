from database import database
import datetime

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