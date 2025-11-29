import requests
import json
import time
from datetime import datetime
import re

session = requests.session()
proxies = {"http": "socks5h://apt-posts-tor:9050", "https": "socks5h://apt-posts-tor:9050"}
session.proxies = proxies

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "content-type": "application/json",
}

def searchDump(obj):
    with open("config/keywords.txt", "r") as r:
        keywords = [line.strip() for line in r.readlines()]
    with open("result/keyworded-result.json", "a+") as w:
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            matches = re.findall(pattern, obj["post_title"], re.IGNORECASE)
        
            if matches:
                print("Matching Keyword:", keyword)
                obj["apt-posts-keyword"] = keyword
                json.dump(obj, w, ensure_ascii=False)
                w.write("\n")

def jsonDump(objects, timestamp):
    if timestamp is not None:
        dt_to_compare = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        # dt_to_compare = "2023-12-30 22:51:09.960659"

    with open("result/new_posts.json", "a") as dump:
        for obj in objects:
            dt_from_data = datetime.strptime(obj["discovered"], "%Y-%m-%d %H:%M:%S.%f")
            
            if timestamp is None or dt_to_compare < dt_from_data:
                searchDump(obj)
                json.dump(obj, dump)
                dump.write('\n')

def fetch_posts(url):
    res = session.get(url, headers=headers)
    
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        print(res.status_code)

if __name__ == '__main__':
    URL = "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json"
    last_timestamp = None

    while True:
        jsonData = fetch_posts(URL)
        
        # Check if new data is fetched
        if jsonData:
            jsonDump(jsonData, last_timestamp)
            last_timestamp = jsonData[-1]["discovered"]
            print(f"Updated last timestamp: {last_timestamp}")

        print("Sleeping for 1 and a half hours")
        time.sleep(90 * 60)
