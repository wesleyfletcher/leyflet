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