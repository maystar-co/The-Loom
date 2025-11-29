import requests
from bs4 import BeautifulSoup
import time
import json
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "content-type": "application/json",
}

session = requests.session()
proxies = {"http": "socks5h://paste-tor:9050", "https": "socks5h://paste-tor:9050"}
session.proxies = proxies


url = "https://pastebin.com/archive"
baseurl = "https://pastebin.com"

def search_keyword(title, author, date, content):
    searchdump = {}
    content = content.replace("\n", "")
    with open("config/keyword.txt", "r") as r:
        keywords = [line.strip() for line in r.readlines()]
    with open("result/keyworded-result.json", "a+") as w:
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            matches = re.findall(pattern, content, re.IGNORECASE)
            
            if matches:
                url = 'http://192.168.29.138:5000/classify'
                headers = {'Content-Type': 'application/json'}
                data = {
                    'text': f'{content}'
                }
                response = requests.post(url, headers=headers, json=data)
                res = response.json()
                print(res)
                print("Matching Keyword:", keyword)
                if res["score"] > 50 and res["classification"] != "General":
                    searchdump["paste-confidence"] = res["score"]
                    searchdump["paste-classfication"] = res["classification"]
                    searchdump["paste-entities"] = res["entities"]

                    # Update the searchdump dictionary with matched information
                    searchdump["paste-code"] = title
                    searchdump["paste-content"] = content
                    searchdump["paste-author"] = author
                    searchdump["paste-date"] = date
                    searchdump["paste-keyword"] = keyword
                    json.dump(searchdump, w, ensure_ascii=False)
                    w.write("\n")


def get_content(links, initial_links):
    # with open("result/content.json", "a+") as file:
    for link in links:
        # jsonDump = {}
        try:
            res = session.get(link, headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            title = link[-8:]
            date = soup.find("div", {"class": "date"}).get_text(strip=True) if title else ''
            author = soup.find("div", {"class": "username"}).get_text(strip=True) if title else ''
            content = soup.find("div", {"class": "source"}).get_text(strip=True) if title else ''

            if author:
                # jsonDump["paste-code"] = title
                # jsonDump["paste-content"] = content
                # jsonDump["paste-author"] = author
                # jsonDump["paste-date"] = date
                # jsonDump["paste-keyword"] = "null"

                # json.dump(jsonDump, file, ensure_ascii=False)
                # file.write("\n")

                search_keyword(title, author.replace("\n", ""), date.replace("\n", ""), content.replace("\n", ""))
                # Check if the link is new and print it
                if link not in initial_links:
                    print(f"New link found: {link}")
                    initial_links.add(link)
            else:
                pass
        except requests.RequestException as e:
            print(f"Error fetching URL: {link}. Error: {e}")


def get_links(url):
    links = []
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table_links = soup.select("table a")
        for l in table_links:
            link = f"{baseurl}{l['href']}"
            links.append(link)

    except requests.RequestException as e:
        print(f"Error fetching URL: {url}. Error: {e}")
    return links


if __name__ == "__main__":

    initial_links = set()
    while True:
        links = get_links(url)
        for link in links:
            if "archive" in link:
                links.remove(link)
        print(f"Found {len(links)} links in home page")
        get_content(links, initial_links)
        time.sleep(3600)