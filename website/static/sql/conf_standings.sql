SELECT
    team, code, conf,

    (conf_losses - conf_wins)/2 AS games_behind,

    conf_wins, conf_losses, conf_pct,
    season_wins, season_losses, season_pct,

    home_wins, home_losses,
    away_wins, away_losses,
    neutral_wins, neutral_losses
FROM team_records

JOIN team
ON team_records.team = team.name

WHERE season = {season}
AND conf LIKE '%{conf}%'
ORDER BY conf ASC, conf_pct DESC