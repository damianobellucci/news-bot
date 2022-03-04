from scrape import scrape
import requests
import time
import json


def send_messages():

    file_config= open('../data/config.json')
    config = json.load(file_config)
    
    token = config['token-telegram-bot']
    channel_id = config['channel_id-telegram']
        

    url = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id=@"+channel_id+"&text="

    messages = scrape()


    for el in messages:
        message = el['title']+'\n'+el['body']
        #send in timestamp order
        time.sleep(0.5)
        requests.get(url+message)
