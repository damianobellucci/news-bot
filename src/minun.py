import time
import json
from bs4 import BeautifulSoup
import requests
import unidecode
from datetime import datetime, timedelta

debug = True

current_date = datetime.today().strftime('%Y/%m/%d')
print(current_date)

# this function create the correct url for scraping, with updated date
def build_url():
    file_config = open("./data/config.json")
    config = json.load(file_config)
    url = config["url"]
    return url

def format_time(string_time):
    info_time = string_time
    info_time = info_time[:-5]
    date = info_time[:-9]
    final_time = date + " - " + info_time[len(info_time) - 8 :]
    return final_time

def scrape():
    url = build_url()
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    # filter articles blocks
    blocks = soup.find_all("section", {"class": "lb-post lb-type-HTML lb-tagName-"})
    list = []
    for block in blocks:
        soup = BeautifulSoup(str(block), "html.parser")
        id = soup.section["id"]
        article = soup.find("div", {"class": "lb-body"})
        # timestamp of article
        time = soup.find("time")["datetime"][:-5]
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        time = time + timedelta(hours=1)
        time_string = format_time(time.ctime())
        timestamp = datetime.timestamp(time)
        time = {
            "month": time.month,
            "day": time.day,
            "hour": time.hour,
            "minute": time.minute,
            "second": time.second,
        }
        # eliminate empty div
        for child in article.find_all(["div"]):
            soup = BeautifulSoup(str(child), "html.parser")
            if not len(soup.text):
                child.decompose()
        try:
            if article.h2 != None:
                title = article.h2.text
            else:
                title = article.h1.text
            # title = unidecode.unidecode(title)
        # some blocks in starting html could have class of articles
        except:
            title = "None title"
            break
        try:
            if article.div != None:
                # removing title article child
                for child in article.find_all(["h2", "h1"]):
                    child.decompose()
                body = article.div.text
            else:
                body = article.p.text
            # body = unidecode.unidecode(body)
        except:
            # article could be without body
            body = "None body"
        list.append(
            {
                "title": title,
                "body": body,
                "time": time,
                "time_string": time_string,
                "timestamp": timestamp,
            }
        )
    return list

def format_message(title, body, date):
    msg = f"{title}\n\n{body}\n\n{date}"
    return msg

def send_messages(messages):
    file_config = open("./data/config.json")
    config = json.load(file_config)
    token = config["token-bot-telegram"]
    channel_id = config["channel_id-telegram"]
    delay = config["delay"]
    url = (
        config["url-telegram"]
        .replace("{token}", token)
        .replace("{channel_id}", channel_id)
    )
    for info_msg in messages:
        message = format_message(
            info_msg["title"], info_msg["body"], info_msg["time_string"]
        )
        res = requests.get(f"{url}{message}")
        print(res)
        time.sleep(delay)

def run():
    # init timestamp frm backup
    obj = open("./data/last-timestamp.json")
    config_timestamp = json.load(obj)
    obj.close()
    last_timestamp = config_timestamp["last-timestamp"]
    print("---------------------------------")
    # obtain list of scraped news with meta info
    news = scrape()
    print("scrape lunghezza", len(news))
    # obtain news only after a certaint timestamp
    news = list(filter(lambda el: el["timestamp"] > last_timestamp, news))
    # print('filtered',len(news))
    if len(news):
        # news must be sent ordered by time
        news = sorted(news, key=lambda el: el["timestamp"])
        print("sorted", len(news))
        # send news to group by bot
        send_messages(news)
        # update timestamp
        for el in news:
            if debug:
                continue
            if el["timestamp"] > last_timestamp:
                last_timestamp = el["timestamp"]
                # update config file for backup timestamp
                config_timestamp["last-timestamp"] = last_timestamp
                obj = open("./data/last-timestamp.json", "w")
                obj.write(json.dumps(config_timestamp, indent=4))
                obj.close()
        print("last timestamp", last_timestamp)

run()