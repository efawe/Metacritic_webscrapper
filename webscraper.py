from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

df = pd.DataFrame(columns=["Title", "Meta_Score", "User_score", "Release_Date", "Console"])    


page = 1
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=condensed&page={page}'

with requests.Session() as session:
       while page < 163:
              req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              main_container = page_soup.findAll("div", "col main_col")

              containers = main_container[0].findAll("div", "product_wrap")
              for container in containers:
                     games_string = container.find("a", href = True)['href'].split("/")
                     game = games_string[3].replace("-"," ")
                     console = games_string[2].replace("-"," ")

                     meta_score = container.find("div", "metascore_w small game positive").contents[0]
                     user_score = container.find('span', class_ = "data").contents[0]

                     rawdate = container.find('li', 'stat release_date full_release_date')
                     date = rawdate.find('span', 'data').contents[0]
              
                     game_data = {'Title':[game], "Meta_Score":[meta_score], "User_score":[user_score], "Release_Date": [date], "Console":[console]}
                     df = df.append(pd.DataFrame(data = game_data))

              page += 1


req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")
page_soup
main_container = page_soup.findAll("div", "col main_col")

containers = main_container[0].findAll("div", "product_wrap")
for container in containers:
       games_string = container.find("a", href = True)['href'].split("/")
       game = games_string[3].replace("-"," ")
       console = games_string[2].replace("-"," ")

       meta_score = container.find("div", "metascore_w small game positive").contents[0]
       user_score = container.find('span', class_ = "data").contents[0]

       rawdate = container.find('li', 'stat release_date full_release_date')
       date = rawdate.find('span', 'data').contents[0]
     
       game_data = {'Title':[game], "Meta_Score":[meta_score], "User_score":[user_score], "Release_Date": [date], "Console":[console]}
       df = df.append(pd.DataFrame(data = game_data))