SELECT *
FROM team_records
WHERE season = {season}
AND conf LIKE '%{conf}%'
ORDER BY conf ASC, season_pct DESC