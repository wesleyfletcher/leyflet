SELECT *
FROM team_records

JOIN team
ON team_records.team = team.name

WHERE season = {season}
AND conf LIKE '%{conf}%'
ORDER BY conf ASC, season_pct DESC