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

JOIN arena
ON game.arena = arena.id

WHERE game.id = {id}