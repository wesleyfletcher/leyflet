from dagster import asset
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@asset
def espn_scoreboard():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?groups=50"

    req = requests.get(url=url)
    return req.json()

@asset
def ncaa_stats():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    url = f'https://stats.ncaa.org'

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.close()

    file = open('test.html', 'w', encoding='utf-8')
    file.write(str(soup.prettify()))
    file.close()

    return soup