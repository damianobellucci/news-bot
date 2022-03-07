import requests
import time
import json


def send_messages(messages):

    file_config= open('../data/config.json')
    config = json.load(file_config)
    
    token = config['token-telegram-bot']
    channel_id = config['channel_id-telegram']
        

    url = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id=@"+channel_id+"&text="

    for el in messages:
        #info_time = el['time']
        # text_time = "Data: "+str(info_time['month'])+"/"+str(info_time['day'])+" - Orario: "+str(info_time['hour'])+":"+str(info_time['minute'])
        
        message =el['title']+'\n\n'+el['body']+'\n\n'+el['time_string']

        #sending messages to group
        requests.get(url+message)
        #send in timestamp order (latency)
        time.sleep(0.2)
