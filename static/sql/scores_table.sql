SELECT 
    id,
    game.season, game_date,
    home_team, away_team,

    neutral, event, arena,
    status, overtimes,

    tip, half, clock,

    IFNULL(active.home_score, complete.home_score) AS home_score,
    IFNULL(active.away_score, complete.away_score) AS away_score,

    IFNULL(active.home_score_1h, complete.home_score_1h) AS home_score_1h,
    IFNULL(active.away_score_1h, complete.away_score_1h) AS away_score_1h,
    IFNULL(active.home_score_2h, complete.home_score_2h) AS home_score_2h,
    IFNULL(active.away_score_2h, complete.away_score_2h) AS away_score_2h,

    IFNULL(active.home_score_ot, complete.home_score_ot) AS home_score_ot,
    IFNULL(active.away_score_ot, complete.away_score_ot) AS away_score_ot,

    home_code.code AS home_team_code,
    away_code.code AS away_team_code,

    home_conf.conf AS home_conf,
    away_conf.conf AS away_conf,

    CONCAT(home_record.season_wins, '-', home_record.season_losses) AS home_season_record,
    CONCAT(away_record.season_wins, '-', away_record.season_losses) AS away_season_record,

    CONCAT(home_record.conf_wins, '-', home_record.conf_losses) AS home_conf_record,
    CONCAT(away_record.conf_wins, '-', away_record.conf_losses) AS away_conf_record

FROM game

LEFT JOIN complete
USING (id)

LEFT JOIN active
USING (id)

LEFT JOIN scheduled
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

JOIN team_records AS home_record
ON game.home_team = home_record.team
    AND game.season = home_record.season

JOIN team_records AS away_record
ON game.away_team = away_record.team
    AND game.season = away_record.season

WHERE game_date = '{date}'

ORDER BY id;