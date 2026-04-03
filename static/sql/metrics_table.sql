SELECT *
FROM metrics

JOIN member
USING (season, team)

WHERE conf LIKE '%{conf}%'
AND season = {season}

ORDER BY kenpom ASC