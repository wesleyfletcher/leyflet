from database import database
import datetime

CURRENT_SEASON = 2025

def teams_list():
    data = {}

    db = database()
    team_table = db.runfile('teams_list')
    db.close()

    for i in range(len(team_table)):
        row = team_table.loc[i]

        if row['code'] not in data:
            data[row['code']] = {
                'name' : row['name'], 
                'conf' : {}
            }

        data[row['code']]['conf'][int(row['season'])] = row['conf']
    
    return data

def teams(code, season):
    data = {}

    season = CURRENT_SEASON if not season else season

    db = database()
    name = db.query(f'SELECT name FROM team WHERE code = "{code}"')

    if type(name) != str:
        raise ValueError(f'Team {code} not found')
    
    data['name'] = name
    data['code'] = code

    record = db.query(f'SELECT season_wins, season_losses FROM team_records WHERE season = {season} AND team = "{name}"')
    data['wins'] = record.loc[0, 'season_wins']
    data['losses'] = record.loc[0, 'season_losses']

    game_log = db.runfile('game_log', name=name, season=season)
    stats_table = db.runfile('roster_stats', name=name, season=season)
    roster_table = db.runfile('team_roster', name=name, season=season)

    db.close()

    data['schedule'] = []
    for i in range(len(game_log)):
        row = game_log.loc[i]
        data['schedule'].append({
            'id'         : row['id'],
            'game_date'  : row['game_date'].strftime('%b %d'), # maybe strftime this
            'site'       : row['site'],
            'opponent'   : row['opponent'],
            'team_score' : int(row['team_score']),
            'oppt_score' : int(row['oppt_score']),
            'result'     : 'W' if int(row['team_score']) > int(row['oppt_score']) else 'L',
            'overtimes'  : int(row['overtimes']),
            'event'      : row['event'] if row['event'] else ''
        })

    data['stats'] = []
    for i in range(len(stats_table)):
        row = stats_table.loc[i]
        data['stats'].append({
            'lname' : row['lname'],
            'fname' : row['fname'],
            'suffix' : f' {row['suffix']}' if row['suffix'] else '',

            'gp'  : int(row['gp']),
            'min' : float(row['min']),
            'pts' : float(row['pts']),

            'fg_pct' : float(row['fg_pct']),
            'tp_pct' : float(row['fg_pct']),
            'ft_pct' : float(row['ft_pct']),

            'reb' : float(row['reb']),
            'ast' : float(row['ast']),
            'tov' : float(row['tov']),
            'stl' : float(row['stl']),
            'blk' : float(row['blk']),

            'oreb' : float(row['oreb']),
            'dreb' : float(row['dreb']),
            'pf' : float(row['pf'])
        })

    data['roster'] = []
    for i in range(len(roster_table)):
        row = roster_table.loc[i]
        data['roster'].append({
            'lname' : row['lname'],
            'fname' : row['fname'],
            'suffix' : f' {row['suffix']}' if row['suffix'] else '',

            'position' : row['position'],
            'height' : row['height'],
            'weight' : row['weight'],

            'city' : row['city'],
            'state' : row['state']
        })

    return data

def scores(date, conf):
    data = {}

    date = datetime.date.today() if not date else datetime.date.fromisoformat(date)
    data['date'] = date

    conf = conf.replace("-", " ") if conf else ''

    db = database()

    confs_list = db.query("SELECT DISTINCT conf FROM member WHERE conf IS NOT NULL ORDER BY conf ASC")

    scores_table = db.runfile('scores_table', date=date, conf=conf)
    key_players = db.runfile('key_players', date=date, conf=conf)
    
    db.close()

    data['conf'] = conf if conf != '' else 'all'
    data['confs_list'] = list(confs_list['conf'])

    data['scores'] = {}
    for i in range(len(scores_table)):
        row = scores_table.loc[i]

        if row['status'] == 'Complete':
            ots = int(row['overtimes'])

            game_time = 'FINAL'
            if ots == 1:
                game_time += '/OT'
            elif ots > 1:
                game_time += f'/{ots}OT'

        elif row['status'] == 'Active':
            ots = 0
            if 'OT' in row['half']:
                ots = int(row['half'][:-2])

            game_time = f'{row['half']} {str(row['clock'])[-5:]}'
        else:
            ots = 0

            game_time = str(row['tip'])[-8:-3]

        data['scores'][int(row['id'])] = {
            'home_team' : row['home_team'], 'home_code' : row['home_team_code'],
            'away_team' : row['away_team'], 'away_code' : row['away_team_code'],

            'neutral' : bool(row['neutral']),
            'overtimes' : ots,
            'status' : row['status'],
            'game_time' : game_time,

            'home_score' : row['home_score'], 'away_score' : row['away_score'],
            'home_score_1h' : row['home_score_1h'], 'away_score_1h' : row['away_score_1h'],
            'home_score_2h' : row['home_score_2h'], 'away_score_2h' : row['away_score_2h'],
            'home_score_ot' : row['home_score_ot'], 'away_score_ot' : row['away_score_ot'],

            'home_conf' : row['home_conf'], 'away_conf' : row['away_conf'],

            'home_season_record' : row['home_season_record'],
            'away_season_record' : row['away_season_record'],
            'home_conf_record'   : row['home_conf_record'],
            'away_conf_record'   : row['away_conf_record']
        }

    for i in range(len(key_players)):
        row = key_players.loc[i]
        data['scores'][int(row['game'])].update({
            'away_scorer' : row['away_scorer'],

            'away_lname' : row['away_lname'], 'away_fname' : row['away_fname'],
            'away_suffix' : f' {row['away_suffix']}' if row['away_suffix'] else '',

            'away_pts' : int(row['away_pts']),
            'away_fgm' : int(row['away_fgm']), 'away_fga' : int(row['away_fga']),
            'away_reb' : int(row['away_reb']), 'away_ast' : int(row['away_ast']),

            'home_scorer' : row['home_scorer'],

            'home_lname' : row['home_lname'], 'home_fname' : row['home_fname'],
            'home_suffix' : f' {row['home_suffix']}' if row['home_suffix'] else '',

            'home_pts' : int(row['home_pts']),
            'home_fgm' : int(row['home_fgm']), 'home_fga' : int(row['home_fga']),
            'home_reb' : int(row['home_reb']), 'home_ast' : int(row['home_ast'])
        })

    return data

def stats(season, conf, page):
    data = {}

    season = CURRENT_SEASON if not season else season
    conf = conf = '' if not conf else conf.replace('-', ' ')
    page = 0 if not page else 100*(int(page)-1)

    db = database()
    player_table = db.runfile('player_stats', season=season, conf=conf, page=page)
    db.close()
    
    data['players'] = []
    for i in range(len(player_table)):
        row = player_table.loc[i]
        data['players'].append({
            'lname' : row['lname'],
            'fname' : row['fname'],
            'suffix' : ' ' + row['suffix'] if row['suffix'] else '',

            'team' : row['team'],

            'gp' : int(row['gp']),
            'min' : float(row['min']),
            'pts' : float(row['pts']),

            'fg_pct' : float(row['fg_pct']),
            'tp_pct' : float(row['tp_pct']),
            'ft_pct' : float(row['ft_pct']),

            'reb' : float(row['reb']),
            'ast' : float(row['ast']),
            'tov' : float(row['tov']),
            'stl' : float(row['stl']),
            'blk' : float(row['blk']),
            
            'oreb' : float(row['oreb']),
            'dreb' : float(row['dreb']),
            'pf' : float(row['pf'])
        })

    return data

def rankings(season, conf):
    data = []

    season = CURRENT_SEASON if not season else season
    conf = '' if not conf else conf.replace('-', ' ')

    db = database()
    metrics_table = db.runfile('metrics_table', season=season, conf=conf)
    db.close()

    for i in range(len(metrics_table)):
        row = metrics_table.loc[i]
        
        data.append({
            'team' : row['team'],
            'kenpom' : int(row['kenpom']),
            'net'    : int(row['net']),
            'wab'    : int(row['wab']),
            'sor'    : int(row['sor']),
            'torvik' : int(row['torvik'])
        })

    return data

def standings(season, conf):
    data = {}

    season = CURRENT_SEASON if not season else season
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
            'suffix' : f' {row['suffix']}' if row['suffix'] else '',

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
            'tov' : int(row['tov']),
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