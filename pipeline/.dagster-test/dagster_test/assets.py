from dagster import asset
import requests

@asset
def espn_scoreboard():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?groups=50"

    req = requests.get(url=url)
    return req.json()

print(espn_scoreboard().get('events'))