from ntscraper import Nitter
import time
import datetime
import json
import re


def searchDump(tweet):
    obj = {}
    with open("config/keywords.txt", "r") as r:
        keywords = [line.strip() for line in r.readlines()]
    with open("result/keyworded-result.json", "a+") as w:
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            matches = re.findall(pattern, tweet["text"], re.IGNORECASE)
        
            if matches:
                print("Match found:", tweet["text"])
                print("Matching Keyword:", keyword)

                # Update the obj dictionary with matched information
                obj["twitter-nitter"] = tweet
                obj["nitter-keyword"] = keyword
                json.dump(obj, w, ensure_ascii=False)
                w.write("\n")

def tweetDump(tweet):
    with open("result/all_tweets.json", "a+") as dump:
        json.dump(tweet, dump)
        dump.write('\n')

def main(user):
    #Calculate Yesterday's Date.
    current_time = datetime.datetime.now()
    offset = datetime.timedelta(days=1)
    since_date = current_time - offset
    formatted_since_date = since_date.strftime("%Y-%m-%d")
    print(formatted_since_date)
    print(user)


    tweets = scraper.get_tweets(user, mode='user', since=formatted_since_date)
    if tweets:
        for tweet in tweets["tweets"]:
            searchDump(tweet)
            tweetDump(tweet)
        print("-----------------------------------------------------------------------------------------------------------------------------------")

def randomInstance():
    return scraper.get_random_instance()


if __name__=='__main__':
    while True:
        scraper = Nitter()
        with open("config/users.txt", "r") as read:
            users = [line.strip() for line in read.readlines()]
        for user in users:
            try:
                main(user)
            except Exception as e:
                print(e)
                print("Main Thread Collapsing")
                time.sleep(10)
                main(user)
                print("Main Thread Saved")
        
        print("#Sleeping for 24hrs")
        time.sleep(24*60*60)