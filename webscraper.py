from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered'

req = Request(url, headers ={'User-Agent':' Mozilla/5.0'})
webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")
page_soup

containers = page_soup.findAll("li", "product game_product")
for container in containers:
    #print(container)
    title = page_soup.findAll("div", "basic_stat product_title")
    print(title)

containers = page_soup.findAll("div", "product_wrap")
for container in containers:
       #print (container)
       ahref = container.findAll("a", href = True)
       print (ahref[0])
       print (container.find("div", "metascore_w small game positive"))
      #print (container.findAll("div", "data textscore textscore_favorable"))
       #print (container.findAll("span", "data"))
    


#sessions = requests.Session()   
#response = sessions.get(url, timeout = 5)
#content = BeautifulSoup(response.content, headers={'User-Agent': 'Mozilla/5.0'})

#print (content)