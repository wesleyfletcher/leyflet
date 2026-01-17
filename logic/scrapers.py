from bs4 import BeautifulSoup
from selenium import webdriver

import requests
import time
import json

import pandas as pd

def appoll():
    url = "https://apnews.com/hub/ap-top-25-college-basketball-poll"
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find(class_='Results-items')
    rows = table.find_all('dd')

    rank_col = [row.find(class_='PollModuleRow-rank') for row in rows]
    team_col = [row.find(class_='PollModuleRow-team').find('a') for row in rows]

    ranks = [int(r.text) for r in rank_col]
    teams = [r.text for r in team_col]

    pd.DataFrame({'Rank' : ranks, 'Team' : teams}).to_csv('TEMP_TABLES/appoll.csv', index=False)

def kenpom():
    url = "https://kenpom.com"

    driver = webdriver.Chrome()
    driver.minimize_window()

    driver.get(url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    driver.close()

    tables = soup.find_all('tbody')
    rows = []

    for table in tables:
        rows += table.find_all('tr')

    rows = [row for row in rows if row.get('class') not in [['thead1'], ['thead2']]]

    rank_col = [row.find('td', class_='hard_left') for row in rows]
    team_col = [row.find('a').find(string=True) for row in rows]

    ranks = [int(r.text) for r in rank_col]
    teams = [r.text for r in team_col]

    pd.DataFrame({'Rank' : ranks, 'Team' : teams}).to_csv('TEMP_TABLES/kenpom.csv', index=False)

def net():
    url = "https://ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings"
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('tbody')
    rows = table.find_all('tr')

    rank_col = [row.find('td') for row in rows]
    team_col = [row.find_all('td')[1] for row in rows]

    ranks = [int(r.text) for r in rank_col]
    teams = [r.text for r in team_col]

    pd.DataFrame({'Rank' : ranks, 'Team' : teams}).to_csv('TEMP_TABLES/net.csv', index=False)

def torvik():
    url = "https://barttorvik.com/#"

    driver = webdriver.Chrome()
    driver.minimize_window()

    driver.get(url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    driver.close()

    rows = soup.find_all('tr', class_='seedrow')

    rank_col = [row.find('td', class_='lowrowclick') for row in rows]

    ranks = [int(r.text) for r in rank_col]
    teams = [row.find('a').find(string=True) for row in rows]

    pd.DataFrame({'Rank' : ranks, 'Team' : teams}).to_csv('TEMP_TABLES/torvik.csv', index=False)

def get_name(team : str):
    names = json.load(open('name_variants.json', 'r'))

    team = team.replace('-', ' ')
    chrs = '.,()'
    for chr in chrs:
        team = team.replace(chr, '')

    for key in names.keys():
        values = [val.lower() for val in names[key]]
        if team.lower() in values:
            return key
        
    raise ValueError(f"{team} not found.")