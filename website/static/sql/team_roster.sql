SELECT
    lname, fname, suffix,
    IFNULL(position, '') AS position,
    IFNULL(height, '') AS height,
    IFNULL(weight, '') AS weight,
    IFNULL(city, '') AS city,
    IFNULL(state, '') AS state
FROM roster

JOIN player
ON player.id = roster.player

WHERE team = '{name}'
AND season = {season}