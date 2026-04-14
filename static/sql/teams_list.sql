SELECT
    season,
    name,
    code,
    IFNULL(conf, 'Independent') AS conf
FROM member

JOIN team
ON member.team = team.name

ORDER BY name, season;