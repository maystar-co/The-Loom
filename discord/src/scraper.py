import requests
import json
from dotenv import load_dotenv
import os
import re

load_dotenv(".env")
token = os.getenv("TOKEN")

headers = {
    "Authorization": token,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "content-type": "application/json",
}

guildIds = []

# search for a keyword in object and store it separetly
def SearchKeyword(object, servername, channelname):
    dumpObject = {}
    with open("config/keyword.txt", "r") as r:
        keywords = [line.strip() for line in r]
    with open("result/Keyworded-Result.json", "a+") as w:
        for obj in object:
            pattern = rf'\b(?:{"|".join(keywords)})\b'
            for keyword in keywords:
                pattern = rf'\b{re.escape(keyword)}\b'
                matches = re.findall(pattern, obj['content'], re.IGNORECASE)
                
                if matches:
                    print("Match found:", obj['content'])
                    print("Matching Keyword:", keyword)
                    dumpObject["Server-Name"] = servername
                    dumpObject["Discord-Channel-Name"] = channelname
                    dumpObject["Discord_object"] = obj
                    dumpObject["Discord-keyword"] = keyword
                    json.dump(dumpObject, w)
                    w.write('\n')


# Get guild id by which get all the channels in current server
def getGuildId(targetGuildName):
    url = "https://discord.com/api/v10/users/@me/guilds"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        guilds = response.json()
        for guild in guilds:
            if guild["name"] == targetGuildName:
                print("[+] Collecting Guild ID")
                return guild["id"]
    else:
        print("[-] Failed to fetch GUILD ID")

# get ids of all channels in the guild
def getGuildChannels(guild_id):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("[+] Collecting Channel IDs")
        return response.json()
    else:
        print("[-] request rejected for retreiving channel ids")


def get_messages(channel_id, before=None):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    params = {
        "limit": 100,  # Maximum number of messages per request
        "before": before,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        print(f"Failed to retrieve messages. Status code: {response.status_code}")

        return None


def retrieve_all_messages(channel_id):
    all_messages = []
    last_message_id = None

    while True:
        messages = get_messages(channel_id, before=last_message_id)
        if not messages:
            break

        all_messages.extend(messages)

        if len(messages) < 100:
            # If we received fewer than 100 messages, it means we've reached the end

            break

        else:
            # Set the last_message_id for the next iteration

            last_message_id = messages[-1]["id"]

    return all_messages


def normalize_output(messages, guild, channel):
    output_dump = {}

    with open("result/messages.json", "a+") as file:
        for message in messages:
            output_dump["Server-Name"] = guild
            output_dump["Discord-Channel-Name"] = channel
            output_dump["Discord_object"] = message
            output_dump["Discord-keyword"] = "null"
            json.dump(output_dump, file)
            file.write("\n")


def scraper():
    with open("config/list.txt", "r") as r:
        links = r.readlines()
        lines = [line.strip() for line in links]

    for link in lines:
        guild_id = getGuildId(link)
        channels = getGuildChannels(guild_id)

        for channel in channels:
            if channel["type"] == 0:
                channelName = channel["name"]
                messages = retrieve_all_messages(channel["id"])
                normalize_output(messages, link, channelName)
                SearchKeyword(messages, link, channelName)

    print("[+] Results are stored in /discord")
