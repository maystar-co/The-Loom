import requests
import json
import time

session = requests.session()
proxies = {"http": "socks5h://apt-groups-tor:9050", "https": "socks5h://apt-groups-tor:9050"}
session.proxies = proxies

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "content-type": "application/json",
}

def jsonDump(object):
    with open("result/links.json", "w") as dump:
        for obj in object:
            if obj["locations"][0]["available"] == True:
                json.dump(obj, dump)
                dump.write('\n')

def fetch_data(url):
    res = session.get(url, headers=headers)
    if res.status_code == 200:
        print("Dispatch")
        # print(res.text)
        return json.loads(res.text)
        
    else:
        print(res.status_code)

if __name__=='__main__':
    URL = "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/groups.json"
    while True:
        jsonData = fetch_data(URL)
        jsonDump(jsonData)
        print("Sleeping")
        time.sleep(90 * 60)