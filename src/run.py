import time
from send import send_messages
from scrape import scrape
import json


#init timestamp frm backup
obj= open('../data/last-timestamp.json')
config_timestamp = json.load(obj)
obj.close()
last_timestamp=config_timestamp['last-timestamp']


while True:

    print("---------------------------------")

    #obtain list of scraped news with meta info
    news = scrape()

    print('scrape lunghezza',len(news))
    #obtain news only after a certaint timestamp
    news = filter(lambda el: el['timestamp'] > last_timestamp, news)

    print('filtered',len(news))


    if len(news):
        #news must be sent ordered by time
        news = sorted(news, key=lambda el: el['timestamp'])

        print('sorted',len(news))

        #send news to group by bot
        send_messages(news)

        #update timestamp

        for el in news:
            if el['timestamp']>last_timestamp:
                last_timestamp = el['timestamp']

                #update config file for backup timestamp
                config_timestamp['last-timestamp']=last_timestamp
                obj = open('../data/last-timestamp.json', 'w')
                obj.write(json.dumps(config_timestamp,indent=4))
                obj.close()

        

        print('last timestamp',last_timestamp)

    #wait until next iteration
    time.sleep(20)