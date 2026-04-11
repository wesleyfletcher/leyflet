SELECT
    name,
    code,
    IFNULL(conf, 'Independent') AS conf
FROM member

JOIN team
ON member.team = team.name

WHERE season = {season}
ORDER BY conf ASC, name ASC;