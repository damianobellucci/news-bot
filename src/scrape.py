from bs4 import BeautifulSoup
import requests
import unidecode
from datetime import datetime, timedelta
from build_url import build_url

def format_time(string_time):
    info_time  = string_time
    info_time = info_time[:-5]
    date = info_time[:-9]
    final_time = date + " - " + info_time[len(info_time)-8:]
    return final_time

def scrape():

    url = build_url()

    res = requests.get(url)
        
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
        time= time + timedelta(hours = 1)

        time_string = format_time(time.ctime())
        
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
            #title = unidecode.unidecode(title)
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
            #body = unidecode.unidecode(body)    
        except:
            #article could be without body
            body='None body'

        list.append({'title':title,'body':body,'time':time,'time_string':time_string,'timestamp':timestamp})
    return list
    