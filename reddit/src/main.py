import praw
import time
import os
from datetime import datetime, date
import json
import re
from dotenv import load_dotenv
import requests

load_dotenv(".env")
token = os.getenv("TOKEN")

# Reddit app credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

# List of subreddits to monitor
subreddit_names = ['netsec', 'cybersecurity']

# Directory to store the last fetched timestamp
cache_dir = 'cache'
os.makedirs(cache_dir, exist_ok=True)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return list(obj)

def search_keyword(obj):
    with open("config/keywords.txt", "r") as r:
        keywords = [line.strip() for line in r.readlines()]
    # print(keywords)
    with open("result/keyworded-result.json", "a+") as file:
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            match1 = re.findall(pattern, obj["Subreddit-title"], re.IGNORECASE)
            match2 = re.findall(pattern, obj["Subreddit-self-post-content"], re.IGNORECASE)

            if match1 or match2:
                url = 'http://192.168.29.138:5000/classify'
                headers = {'Content-Type': 'application/json'}
                data = {
                    'text': f'{obj["Subreddit-title"]}'
                }
                response = requests.post(url, headers=headers, json=data)
                res = response.json()
                print(res)
                if res["score"] > 50 and res["classification"] != "General":

                    print("Matching Keyword:", keyword)
                    obj["reddit-confidence"] = res["score"]
                    obj["reddit-classfication"] = res["classification"]
                    obj["reddit-entities"] = res["entities"]
                    # Update the object with the matching keyword
                    obj["reddit-keyword"] = keyword

                    # Save the matched information to a JSON file
                    json.dump(obj, file, default=json_serial)
                    file.write("\n")

def subredditDump(obj):
    with open("result/all_subreddit.json", "a+") as w:
        json.dump(obj, w, default=json_serial)
        w.write('\n')

#return last fetched timestamps of subreddits
def get_last_fetched_timestamp(subreddit_name):
    cache_file = os.path.join(cache_dir, f'{subreddit_name}_last_fetched.txt')
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            return float(file.read())
    else:
        # If the file doesn't exist, return a timestamp far in the past
        print("Returning 2024 Timestamp")
        return time.mktime(datetime(2024, 1, 1).timetuple())

# Stores the last reddit post timestamp
def update_last_fetched_timestamp(subreddit_name, timestamp):
    cache_file = os.path.join(cache_dir, f'{subreddit_name}_last_fetched.txt')
    
    with open(cache_file, 'w') as file:
        file.write(str(timestamp))

#Fetch New Posts
def fetch_new_posts(subreddit_name):
    print("fetch new posts")
    subreddit = reddit.subreddit(subreddit_name)
    last_fetched_timestamp = get_last_fetched_timestamp(subreddit_name)
    print(last_fetched_timestamp)

    for submission in subreddit.new(limit=None):
        obj = {}
        # Check if the post is newer than the last fetched timestamp
        if submission.created_utc > last_fetched_timestamp:
            obj["Subreddit-name"] = submission.name
            obj["Subreddit-title"] = submission.title
            obj["Subreddit-author"] = submission.author
            obj["Subreddit-url"] = submission.url
            obj["Subreddit-permalink"] = submission.permalink
            obj["Subreddit-submission-id"] = submission.id
            obj["Subreddit-self-post-content"] = submission.selftext
            obj["Subreddit-no-of-comments"] = submission.num_comments
            obj["Subreddit-Score"] = submission.score
            obj["Subreddit-upvote-ratio"] = submission.upvote_ratio
            obj["Subreddit-created-utc"] = submission.created_utc
            obj["Subreddit-time"] = submission.created
            obj["Subreddit-flair"] = submission.link_flair_text
            obj["Subreddit-is-self-post"] = submission.is_self
            obj["Subreddit-is-original-content"] = submission.is_original_content
            obj["Subreddit-is-video"] = submission.is_video
            obj["Subreddit-awards"] = submission.total_awards_received

            search_keyword(obj)
            subredditDump(obj)

    # Update the last fetched timestamp
    update_last_fetched_timestamp(subreddit_name, time.time())

if __name__ == "__main__":
    print("Initailize reddit object")
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    print("Created Reddit object")
    while True:
        for subreddit_name in subreddit_names:
            fetch_new_posts(subreddit_name)

        # Sleep for 3 hours
        print("Sleeping for 3 hours")
        time.sleep(3 * 60 * 60)
