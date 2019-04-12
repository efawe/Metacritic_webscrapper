from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

df = pd

page = 1
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=condensed&page={page}'

with requests.Session() as session:
       while True:
              req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
              webpage = urlopen(req).read()

              page_soup = soup(webpage, "html.parser")
              page_soup
              main_container = page_soup.findAll("div", "col main_col")

              containers = main_container[0].findAll("div", "product_wrap")
              for container in containers:
                     #print (container)
                     games_string = container.find("a", href = True)['href']
                     print (games_string)
                     meta_score = container.find("div", "metascore_w small game positive").contents[0]
                     print (meta_score)
                     user_score = container.find('span', class_ = "data").contents[0]
                     print (user_score)
                     rawdate = container.find('li', 'stat release_date full_release_date')
                     date = rawdate.find('span', 'data').contents[0]
                     print (date)
              #print (container.findAll("div", "data textscore textscore_favorable"))
                     #print (container.findAll("span", "data"))

              page += 1


games_string['href']
containers[0].findAll("a")['href']

#sessions = requests.Session()   
#response = sessions.get(url, timeout = 5)
#content = BeautifulSoup(response.content, headers={'User-Agent': 'Mozilla/5.0'})

#print (content)