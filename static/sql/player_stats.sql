SELECT
    lname, fname, suffix,

    team,

    COUNT(*) AS gp,

    ROUND(AVG(min), 1) AS min,
    ROUND(AVG(pts), 1) AS pts,

    ROUND(IFNULL(100*SUM(fgm)/SUM(fga), 0), 1) AS fg_pct,
    ROUND(IFNULL(100*SUM(tpm)/SUM(tpa), 0), 1) AS tp_pct,
    ROUND(IFNULL(100*SUM(ftm)/SUM(fta), 0), 1) AS ft_pct,

    ROUND(AVG(reb), 1) AS reb,
    ROUND(AVG(ast), 1) AS ast,
    ROUND(AVG(tov), 1) AS tov,
    ROUND(AVG(stl), 1) AS stl,
    ROUND(AVG(blk), 1) AS blk,
    
    ROUND(AVG(oreb), 1) AS oreb,
    ROUND(AVG(dreb), 1) AS dreb,
    ROUND(AVG(pf), 1) AS pf

FROM stats

JOIN game
ON game.id = stats.game

JOIN player
ON player.id = stats.player

JOIN roster
USING (player, season)

WHERE season = {season}

GROUP BY player, season
HAVING (gp >= 25)

ORDER BY pts DESC, gp DESC

LIMIT {page}, 100;