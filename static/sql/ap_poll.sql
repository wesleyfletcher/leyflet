SELECT
    week,
    team,
    code,
    ap_poll,
    ap_pts,
    ap_first_votes
FROM polls

JOIN team
ON polls.team = team.name

WHERE season = {season}
ORDER BY week ASC, ap_poll ASC