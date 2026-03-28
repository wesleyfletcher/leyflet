SELECT
    team, conf,
    wins AS season_wins, losses AS season_losses,
    ROUND(wins / (wins + losses), 3) AS season_pct
FROM season_records
WHERE season = {season}
AND conf LIKE '%{conf}%'
ORDER BY conf ASC, season_pct DESC