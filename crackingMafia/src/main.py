import requests
from bs4 import BeautifulSoup
import json
import time
import re


URL = "https://crackingmafia.is/forums/databases.84/"
baseurl = "https://crackingmafia.is/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "content-type": "application/json",
}

def search_keyword(obj):
    with open("config/keywords.txt", "r") as r:
        keywords = [line.strip() for line in r.readlines()]
    with open("result/keyworded-result.json", "a+") as w:
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            matches1 = re.findall(pattern, obj["crackmafia-title"], re.IGNORECASE)
            matches2 = re.findall(pattern, obj["crackmafia-content"], re.IGNORECASE)

            if matches1 or matches2:
                url = 'http://192.168.29.138:5000/classify'
                headers = {'Content-Type': 'application/json'}
                data = {
                    'text': f'{obj["crackmafia-content"]}'
                }
                response = requests.post(url, headers=headers, json=data)
                res = response.json()
                print(res)
                if res["score"] > 50 and res["classification"] != "General":
                    obj["paste-confidence"] = res["score"]
                    obj["paste-classfication"] = res["classification"]
                    obj["entities"] = res["entities"]
                    print("Matching Keyword:", keyword)

                    # Update the searchdump dictionary with matched information
                    obj["crackmafia-keyword"] = keyword
                    json.dump(obj, w, ensure_ascii=False)
                    w.write("\n")   

# def jsonObjDump(obj):
#     with open("result/all_cracking_posts.json", "a+") as w:
#         json.dump(obj, w)
#         w.write('\n')

def fetch_content(links):
    for link in links:
        if link not in fetched_links:
            jsonobj = {}
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('h1', class_="p-title-value")
                author = soup.find("h4", class_="message-name")
                date = soup.find('time', class_="u-dt")
                content = soup.find('div', class_="bbWrapper")

                jsonobj["crackmafia-title"] = title.get_text(strip=True) if title else ''
                jsonobj["crackmafia-author"] = author.get_text(strip=True) if author else ''
                jsonobj["crackmafia-date"] = date.get_text(strip=True) if date else ''
                jsonobj["crackmafia-content"] = content.get_text(strip=True) if content else ''
                jsonobj["crackmafia-link"] = link
                search_keyword(jsonobj)
                # jsonObjDump(jsonobj)
                fetched_links.add(link)
            else:
                print(response.status_code)

def fetch_links(url):
    links = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_lists = soup.select(".structItem-title")
        for title in title_lists:
            a_tags = title.find('a')
            if a_tags:
                links.append(f'{baseurl}{a_tags["href"]}')
    else:
        print(response.status_code)
    return links


if __name__ == '__main__':
    fetched_links = set()
    while True:
        links = fetch_links(URL)
        fetch_content(links=links)
        print("Data fetched. Sleeping for 1 hour.")
        time.sleep(3600)
