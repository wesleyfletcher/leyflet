SELECT *
FROM metrics

JOIN quad_records
USING (season, team)

JOIN member
USING (season, team)

JOIN team
ON metrics.team = team.name

WHERE season = {season}

ORDER BY kenpom ASC