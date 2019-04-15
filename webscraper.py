from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

df = pd.DataFrame(columns=["title", "meta_Score", "user_Score", "release_Date", "console", "url",
                           "user_Pos", "user_Mix", "user_Neg", 'crit_Pos','crit_Mix','crit_Neg','pos_Review',
                           'mix_Review', 'neg_Review', 'prod_Rating'])    

page = 1
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=condensed&page={page}'

with requests.Session() as session:
       while page < 164:
              req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              main_container = page_soup.findAll("div", "col main_col")

              containers = main_container[0].findAll("div", "product_wrap")
              for container in containers:
                     games_string = container.find("a", href = True)['href']
                     game = games_string.split("/")[3].replace("-"," ")
                     console = games_string.split("/")[2].replace("-"," ")
                     game_url = 'https://www.metacritic.com' + str(games_string)

                     meta_score = container.find("div", "metascore_w small game positive").contents[0]
                     user_score = container.find('span', class_ = "data").contents[0]

                     rawdate = container.find('li', 'stat release_date full_release_date')
                     date = rawdate.find('span', 'data').contents[0]
                     
                     game_data = {'title':[game], "meta_Score":[meta_score], "user_Score":[user_score], "release_Date": [date], "console":[console],
                                  "url":[game_url]}
                     df = df.append(pd.DataFrame(data = game_data)).reset_index(drop = True)

              page += 1

with requests.Session() as session:
       for url in df['url']:
              req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              container = page_soup.findAll("li", "score_count")
              user_container = page_soup.findAll("ol", "score_counts hover_none")
              crit_container = page_soup.find_all("ol", "score_counts")
              sub_container = container[0].findAll("li", "score_count")
              sub_container[0]

              df['user_Pos'][df['url'] == url] = container[0].find("span", "count").contents[0]
              df['user_Mix'][df['url'] == url] = container[1].find("span", "count").contents[0]
              df['user_Neg'][df['url'] == url] = container[2].find("span", "count").contents[0]
              df['crit_Pos'][df['url'] == url] = container[3].find("span", "count").contents[0]
              df['crit_Mix'][df['url'] == url] = container[4].find("span", "count").contents[0]
              df['crit_Neg'][df['url'] == url] = container[5].find("span", "count").contents[0]
              
with requests.Session() as session:
       for url in df['url']:
              req = Request(url+ '/user-reviews', headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              container = page_soup.find("div", "module reviews_module user_reviews_module")
              
              df['pos_Review'][df['url'] == game] = container.findAll("span", "count")[0].contents[0]
              df['mix_Review'][df['url'] == game] = container.findAll("span", "count")[1].contents[0]
              df['neg_Review'][df['url'] == game] = container.findAll("span", "count")[2].contents[0]

              prod_container = page_soup.find('li', 'summary_detail product_rating')
              df['prod_Rating'][df['url'] == game]  = prod_container.find('span', 'data').contents[0]
