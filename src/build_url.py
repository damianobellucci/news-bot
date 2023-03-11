from datetime import datetime
import json

#this function create the correct url for scraping, with updated date
def build_url():
    file_config= open('./data/config.json')
    config = json.load(file_config)
    url = config["url"]
    return url
