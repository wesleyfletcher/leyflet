SELECT
    game.id AS game,

    t1.player AS away_scorer,
    t1.lname AS away_lname, t1.fname AS away_fname, t1.suffix AS away_suffix,

    t1.pts AS away_pts, t1.fgm AS away_fgm, t1.fga AS away_fga,
    t1.reb AS away_reb, t1.ast AS away_ast,

    t2.player AS home_scorer,
    t2.lname AS home_lname, t2.fname AS home_fname, t2.suffix AS home_suffix,

    t2.pts AS home_pts, t2.fgm AS home_fgm, t2.fga AS home_fga,
    t2.reb AS home_reb, t2.ast AS home_ast

FROM game

JOIN (
    SELECT
        game,
        team, conf,
        
        player,
        lname, fname, suffix,

        pts,
        fgm, fga,
        reb, ast

    FROM (
        SELECT
            game, team, season,
            MIN(player) AS player

        FROM (
            SELECT
                game, team,
                MAX(pts) AS pts

            FROM stats

            JOIN game
            ON stats.game = game.id

            JOIN roster
            USING (player, season)

            WHERE game_date = '{date}'

            GROUP BY game, team
        ) AS leading_scorers

        JOIN (
            SELECT *
            FROM stats

            JOIN game
            ON stats.game = game.id

            JOIN roster
            USING (player, season)
        ) AS game_teams
        USING (game, team, pts)

        GROUP BY game, team
    ) AS leading_scorers

    JOIN stats
    USING (game, player)

    JOIN player
    ON player.id = stats.player

    JOIN member
    USING (team, season)
) AS t1,

(
    SELECT
        game,
        team, conf,
        
        player,
        lname, fname, suffix,

        pts,
        fgm, fga,
        reb, ast

    FROM (
        SELECT
            game, team, season,
            MIN(player) AS player

        FROM (
            SELECT
                game, team,
                MAX(pts) AS pts

            FROM stats

            JOIN game
            ON stats.game = game.id

            JOIN roster
            USING (player, season)

            WHERE game_date = '{date}'

            GROUP BY game, team
        ) AS leading_scorers

        JOIN (
            SELECT *
            FROM stats

            JOIN game
            ON stats.game = game.id

            JOIN roster
            USING (player, season)
        ) AS game_teams
        USING (game, team, pts)

        GROUP BY game, team
    ) AS leading_scorers

    JOIN stats
    USING (game, player)

    JOIN player
    ON player.id = stats.player

    JOIN member
    USING (team, season)
) AS t2

WHERE t1.game = game.id
  AND t2.game = game.id
  AND t1.team = game.away_team
  AND t2.team = game.home_team

  AND (t1.conf LIKE '%{conf}%'
  OR t2.conf LIKE '%{conf}%')

  AND game.status = 'Complete'

ORDER BY game;