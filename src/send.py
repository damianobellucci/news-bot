from scrape import scrape
import requests
import time

def send_messages():
    url = "https://api.telegram.org/bot5168034242:AAFd-MnqUnY1lv1EDVqd63YxLeYvcUS3lHY/sendMessage?chat_id=@newschannel1011&text="

    messages = scrape()


    for el in messages:
        message = el['title']+'\n'+el['body']
        time.sleep(0.5)
        requests.get(url+message)
