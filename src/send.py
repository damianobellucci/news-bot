from scrape import scrape
import requests
import time

def send_messages():
    url = "https://api.telegram.org/bot5168034242:AAFd-MnqUnY1lv1EDVqd63YxLeYvcUS3lHY/sendMessage?chat_id=@newschannel1011&text="

    messages_json = scrape()



    url=url+str(messages_json[0:4000])

    requests.get(url)
