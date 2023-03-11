import requests
import time
import json

def format_message(title, body, date):
    msg  = f"{title}\n\n{body}\n\n{date}"
    return msg

def send_messages(messages):
    file_config= open('./data/config.json')
    config = json.load(file_config)
    token = config['token-bot-telegram']
    channel_id = config['channel_id-telegram']
    delay = config["delay"]
    url = config['url-telegram'].replace("{token}",token).replace("{channel_id}",channel_id)
    for info_msg in messages:
        message = format_message(info_msg["title"], info_msg["body"], info_msg["time_string"])
        print(message)
        res = requests.get(f"{url}{message}")
        print(res)
        time.sleep(delay)
