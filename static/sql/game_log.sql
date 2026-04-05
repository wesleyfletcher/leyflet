
SELECT
    id, game_date,
    CASE WHEN neutral THEN 'N' ELSE 'H' END AS site,
    away_team AS opponent,
    home_score AS team_score,
    away_score AS oppt_score,
    overtimes,
    event

FROM game
JOIN complete
USING (id)
WHERE home_team = '{name}'
AND season = {season}

UNION

SELECT
    id, game_date,
    CASE WHEN neutral THEN 'N' ELSE 'A' END AS site,
    home_team AS opponent,
    away_score AS team_score,
    home_score AS oppt_score,
    overtimes,
    event
    
FROM game
JOIN complete
USING (id)
WHERE away_team = '{name}'
AND season = {season}

ORDER BY game_date ASC;