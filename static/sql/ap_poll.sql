SELECT
    week,
    team,
    ap_poll,
    ap_pts,
    ap_first_votes
FROM polls
WHERE season = {season}
ORDER BY week ASC, ap_poll ASC