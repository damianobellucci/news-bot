import json
from bs4 import BeautifulSoup
import requests
import unidecode
import json
from datetime import datetime

def scrape():

    file_config= open('../data/config.json')
    config = json.load(file_config)

    res = requests.get(config['url'])
        
    soup = BeautifulSoup(res.text, 'html.parser')

    #filter articles blocks
    blocks = soup.find_all("section", {"class": "lb-post lb-type-HTML lb-tagName-"})


    list = []
    

    for block in blocks:
        soup = BeautifulSoup(str(block), 'html.parser')
        
        id  = soup.section['id']
        
        article = soup.find("div", {"class": "lb-body"})

        #timestamp of article
        time = soup.find("time")['datetime'][:-5]

        time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')

        timestamp = datetime.timestamp(time)

     
        time = {"month":time.month,"day":time.day,"hour":time.hour,"minute":time.minute,"second":time.second}

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
            title='None title'
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
            body='None body'

        list.append({'title':title,'body':body,'time':time,'timestamp':timestamp})
    return list
    