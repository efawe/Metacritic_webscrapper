from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import html5lib

import numpy as np
import pandas as pd

df = pd.DataFrame(columns=["title", "meta_Score", "user_Score", "release_Date", "console", "url",
                           "user_Pos", "user_Mix", "user_Neg", 'crit_Pos','crit_Mix','crit_Neg','pos_userReview',
                           'mix_userReview', 'neg_userReview','pos_critReview', 'mix_critReview', 'neg_critReview' , 'prod_Rating'])    

page = 0
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered'

with requests.Session() as session:
    while page < 164:
        try:
            if page != 0:
                url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=' + str(page)  
            req = Request(url, headers ={'User-Agent':'Mozilla/5.0'})
            page1 = urlopen(req)
            if page1.getcode() == 200:
                webpage = page1.read()
                page_soup = soup(webpage, "html.parser")
                main_container = page_soup.findAll("div", "col main_col")
        
                containers = main_container[0].findAll("div", "product_wrap")
                for container in containers:
                    games_string = container.find("a", href = True)['href']
                    game = games_string.split("/")[3].replace("-"," ")
                    console = games_string.split("/")[2].replace("-"," ")
                    game_url = 'https://www.metacritic.com' + str(games_string)
        
                    meta_score = container.find("div", "metascore_w").contents[0]
                    user_score = container.find('span', class_ = "data").contents[0]
        
                    rawdate = container.find('li', 'stat release_date full_release_date')
                    date = rawdate.find('span', 'data').contents[0]
                             
                    game_data = {'title':[game], "meta_Score":[meta_score], "user_Score":[user_score], "release_Date": [date], "console":[console],
                                 "url":[game_url]}
                    df = df.append(pd.DataFrame(data = game_data)).reset_index(drop = True)
        except Exception as inst:
            print (inst)
            print (page)
        page += 1
              
print ("Done")


with requests.Session() as session:
       for game in df['url']:
              while True:
                     try:
                            req = requests.get(game , headers ={'User-Agent':'Mozilla/5.0'})
                            if req.status_code == 200:
                                   break
                            if (req.status_code == 403 or req.status_code == 404): 
                                   print (game)
                                   break
                     except Exception as inst:
                            print (inst)
                            print (game) 
              if (req.status_code == 403 or req.status_code == 404): 
                     continue             
              page_soup = soup(req.content, "html.parser")
              container = page_soup.findAll("li", "score_count")
              
              df['crit_Pos'][df['url'] == game] = container[0].find("span", "count").contents[0]
              df['crit_Mix'][df['url'] == game] = container[1].find("span", "count").contents[0]
              df['crit_Neg'][df['url'] == game] = container[2].find("span", "count").contents[0]
              df['user_Pos'][df['url'] == game] = container[3].find("span", "count").contents[0]
              df['user_Mix'][df['url'] == game] = container[4].find("span", "count").contents[0]
              df['user_Neg'][df['url'] == game] = container[5].find("span", "count").contents[0]

              prod_container = page_soup.find('li', 'summary_detail product_rating')
              df['prod_Rating'][df['url'] == game]  = prod_container.find('span', 'data').contents[0] 
              
print ("Done")              
              
with requests.Session() as session:
    for game in df['url']:
        while True: 
            try:
                req = requests.get(game + "/user-reviews" , headers ={'User-Agent':'Mozilla/5.0'})
                if req.status_code == 200:
                    break
                if (req.status_code == 403 or req.status_code == 404): 
                    print (game)
                    break
            except Exception as inst:
                print (inst)
                print (game) 
        if (req.status_code == 403 or req.status_code == 404): 
              continue              
        page_soup = soup(req.content, "html.parser")
        container = page_soup.findAll("ol", "score_counts hover_none")

        if len(container) == 1:       
              df['pos_critReview'][df['url'] == game] = container[1].find("span", "count").contents[0]
              df['mix_critReview'][df['url'] == game] = container[1].find("span", "count").contents[0]
              df['neg_critReview'][df['url'] == game] = container[1].find("span", "count").contents[0]  

       df['pos_userReview'][df['url'] == game] = container[0].find("span", "count").contents[0]
       df['mix_userReview'][df['url'] == game] = container[0].find("span", "count").contents[0]
       df['neg_userReview'][df['url'] == game] = container[0].find("span", "count").contents[0]      
   


df.to_csv("metacritic.csv", index = False)              

