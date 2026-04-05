SELECT
    lname, fname, suffix,
    position,
    height,
    weight,
    city,
    state
FROM roster

JOIN player
ON player.id = roster.player

WHERE team = '{name}'
AND season = {season}