import json
from os import times
from bs4 import BeautifulSoup
import requests
import unidecode
import json
import pandas as pd

def scrape():

    file_config= open('../data/config.json')

    config = json.load(file_config)
    res = requests.get(config['url'])
        
    soup = BeautifulSoup(res.text, 'html.parser')

    #filter articles blocks
    blocks = soup.find_all("section", {"class": "lb-post lb-type-HTML lb-tagName-"})

    #foreach article id->info
    hashmap = dict()
    list = []


    for block in blocks:
        soup = BeautifulSoup(str(block), 'html.parser')
        
        id  = soup.section['id']
        
        article = soup.find("div", {"class": "lb-body"})

        #timestamp of article
        time = soup.find("time")['datetime']
        #converting in Rome time zone
        time= pd.to_datetime(time)+ pd.Timedelta(hours=1)
        timestamp = time.timestamp()
        time = ','.join(str(x) for x in [time.month,time.day,time.hour,time.minute])



        #eliminate empty div
        for child in article.find_all(["div"]):
            soup = BeautifulSoup(str(child), 'html.parser')
            if not len(soup.text):
                child.decompose()

        
        try:
            if(article.h2!=None):
                title=article.h2.text
            else:
                title=article.h1.text
            title = unidecode.unidecode(title)
        #some blocks in starting html could have class of articles
        except: 
            title=None
            break

        try:
            if article.div!=None :
                
                #removing title article child 
                for child in article.find_all(["h2","h1"]):
                    child.decompose()
                    
                body=article.div.text
                
            else:
                body=article.p.text
            body = unidecode.unidecode(body)    
        except:
            #article could be without body
            body=None
        
        #hashmap[id]={'title':title,'body':body}
        list.append({'title':title,'body':body,'time':time,'timestamp':timestamp})


    #json_hasmap = json.dumps(hashmap,indent=4)
    return list

'''
obj = open('../data/data.json', 'w')
obj.write(json_hasmap)
obj.close()

'''
    
    
