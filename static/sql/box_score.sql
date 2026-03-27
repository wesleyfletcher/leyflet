SELECT *
FROM stats

JOIN game
ON game.id = stats.game

JOIN roster
USING (player, season)

JOIN player
ON player.id = stats.player

WHERE game = {id}
ORDER BY pts DESC