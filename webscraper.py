from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

df = pd.DataFrame(columns=["Title", "Meta_Score", "User_score", "Release_Date", "Console", "url"])    

page = 1
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=condensed&page={page}'

with requests.Session() as session:
       while page < 2:
              req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              main_container = page_soup.findAll("div", "col main_col")

              containers = main_container[0].findAll("div", "product_wrap")
              for container in containers:
                     games_string = container.find("a", href = True)['href']
                     game = games_string.split("/")[3].replace("-"," ")
                     console = games_string.split("/")[2].replace("-"," ")
                     game_url = 'https://www.metacritic.com' + str(games_string) + '/user-reviews'

                     meta_score = container.find("div", "metascore_w small game positive").contents[0]
                     user_score = container.find('span', class_ = "data").contents[0]

                     rawdate = container.find('li', 'stat release_date full_release_date')
                     date = rawdate.find('span', 'data').contents[0]
                     
                     game_data = {'Title':[game], "Meta_Score":[meta_score], "User_score":[user_score], "Release_Date": [date], "Console":[console], "url":[game_url]}
                     df = df.append(pd.DataFrame(data = game_data)).reset_index(drop = True)

              page += 1

with requests.Session() as session:
       for game in df['url']:
              req = Request(game, headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              container = page_soup.findAll("li", "score_count")
              pos_score = container[0].find("span", "count").contents[0]
              mix_score = container[1].find("span", "count").contents[0]
              neg_score = container[2].find("span", "count").contents[0]


