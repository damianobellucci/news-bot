from calendar import month
from datetime import datetime
import json

def two_digit_number(num):
    if len(num)==1:
        return ('0'+num)
    return num

#this function create the correct url for scraping, with updated date
def build_url():
    now = datetime.now()
    day = two_digit_number(str(now.day))
    month = two_digit_number(str(now.month))

    file_config= open('../data/config.json')
    config = json.load(file_config)

    url_split = config['url'].split("2022/")
    url = url_split[0]+'2022/'+month+'/'+day+url_split[1][5:]

    return url
