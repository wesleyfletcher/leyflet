SELECT
    team,
    COUNT(*) AS gp,
    ROUND(AVG(off), 1) AS off,
    ROUND(AVG(def), 1) AS def,
    ROUND(AVG(off-def), 1) AS diff
FROM (

    SELECT
        home_team AS team,
        home_score AS off,
        away_score AS def

    FROM game
    JOIN complete
    USING (id)

    WHERE season = {season}

    UNION

    SELECT
        away_team AS team,
        away_score AS off,
        home_score AS def

    FROM game
    JOIN complete
    USING (id)

    WHERE season = {season}
) AS team_scores

GROUP BY team
ORDER BY diff DESC;