import json
import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class Minun:
    def __init__(self):
        self.debug = True
        self.path_status = "./data/status.json"
        self.path_config = "./data/config.json"
        self.last_timestamp = self.get_status()["last_timestamp"]
        self.config = self.get_config()
        return

    def get_config(self):
        file_config = open(self.path_config)
        config = json.load(file_config)
        file_config.close()
        return config

    def build_url(self):
        current_date = datetime.today().strftime("%Y/%m/%d")
        url = self.config["url"].replace("{date}", current_date)
        return url

    def format_time(self, string_time):
        info_time = string_time
        info_time = info_time[:-5]
        date = info_time[:-9]
        final_time = date + " - " + info_time[len(info_time) - 8 :]
        return final_time

    def scrape(self):
        url = self.build_url()
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
            time_string = self.format_time(time.ctime())
            timestamp = datetime.timestamp(time)
            time = {
                "month": time.month,
                "day": time.day,
                "hour": time.hour,
                "minute": time.minute,
                "second": time.second,
            }
            # delete empty div
            for child in article.find_all(["div"]):
                soup = BeautifulSoup(str(child), "html.parser")
                if not len(soup.text):
                    child.decompose()
            try:
                if article.h2 != None:
                    title = article.h2.text
                else:
                    title = article.h1.text
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

    def format_message(self, title, body, date):
        msg = f"{title}\n\n{body}\n\n{date}"
        return msg

    def send_messages(self, messages):
        file_config = open(self.path_config)
        config = json.load(file_config)
        token = config["token_bot_telegram"]
        channel_id = config["channel_id_telegram"]
        delay = config["delay"]
        url = (
            config["url_telegram"]
            .replace("{token}", token)
            .replace("{channel_id}", channel_id)
        )
        for info_msg in messages:
            message = self.format_message(
                info_msg["title"], info_msg["body"], info_msg["time_string"]
            )
            res = requests.get(f"{url}{message}")
            if self.debug:
                print(res.status_code)
            time.sleep(delay)

    def get_status(self):
        obj = open(self.path_status)
        status = json.load(obj)
        obj.close()
        return status

    def set_status(self, status):
        print(status)
        obj = open(self.path_status, "w")
        obj.write(json.dumps(status, indent=4))
        obj.close()

    def start(self):
        # obtain list of scraped news with meta info
        news = self.scrape()
        print(f"number of articles: {len(news)}")
        # obtain news only after a certaint timestamp
        news = list(filter(lambda el: el["timestamp"] > self.last_timestamp, news))
        print(f"number of new articles: {len(news)}")
        if not len(news):
            return
        # news must be sent ordered by time
        sorted_news = sorted(news, key=lambda el: el["timestamp"])
        # send news to group by bot
        self.send_messages(sorted_news)
        # update status last article timestamp
        print(sorted_news)
        if self.debug:
            return
        self.set_status({"last_timestamp": sorted_news[-1]["timestamp"]})


minun = Minun()
minun.start()
