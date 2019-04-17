from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from BeautifulSoup import BeautifulSoup
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib2

import numpy as np
import pandas as pd
import re

df = pd.DataFrame(columns=["title", "console", "publisher", "developer", "vg_Score","meta_Score"
                           "total_Ship", "total_Sale","na_Sale", "pal_Sale", "japan_Sale", "other_sale"
                           "relase_Date", "last_Update"])    

page = 1
url1 = 'http://www.vgchartz.com/games/games.php?page=1'
url2 = '&results=10&name=&console=&keyword=&publisher=&genre=&order=Sales&ownership=Both'
url3 = '&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC'
url4 = '&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1'
url5 = '&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1'
url6 = '&showshipped=1&alphasort=&showmultiplat=No'

url = url1 + url2 + url3 +url4 + url5 + url6


with requests.Session() as session:
    while page < 2:
        req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
        webpage = urlopen(req).read()

        page_soup = soup(webpage, "html.parser")
        main_container = page_soup.find("div", id = "generalBody")



              containers = main_container[0].findAll("div", "product_wrap")
              for container in containers:
                     games_string = container.find("a", href = True)['href']
                     game = games_string.split("/")[3].replace("-"," ")
                     console = games_string.split("/")[2].replace("-"," ")
                     game_url = 'https://www.metacritic.com' + str(games_string)

                     meta_score = container.find("div", "metascore_w small game positive").contents[0]
                     user_score = container.find('span', style = True).contents[0]

                     rawdate = container.find('li', 'stat release_date full_release_date')
                     date = rawdate.find('span', 'data').contents[0]
                     
                     game_data = {'title':[game], "meta_Score":[meta_score], "user_Score":[user_score], "release_Date": [date], "console":[console],
                                  "url":[game_url]}
                     df = df.append(pd.DataFrame(data = game_data)).reset_index(drop = True)

              page += 1


def test(req):
    req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
    webpage = urlopen(req).read()

    return soup(webpage, "html.parser")                