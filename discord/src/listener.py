import asyncio
import json
import logging
import os
import websockets
import websockets.exceptions
from dotenv import load_dotenv
import requests
import re

# Configuring the logging

logging.basicConfig(level=logging.INFO)


load_dotenv(".env")

token = os.getenv("TOKEN")


discord_ws_url = "wss://gateway.discord.gg/?v=10&encoding-json"

headers = {
    "Authorization": token,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "content-type": "application/json",
}


# Searches for a keyword in JSON object


def SearchKeyword(object):
    with open("config/keyword.txt", "r") as r:
        keywords = [line.strip() for line in r.readlines()]

    for keyword in keywords:
        pattern = rf'\b{re.escape(keyword)}\b'
        matches = re.findall(pattern, object['content'], re.IGNORECASE)

        if matches:
            print("Match found:", object['content'])
            print("Matching Keyword:", keyword)

            # You can save the matched information to a result JSON file if needed
            jsonDump(object, "keyword", keyword)


# Decides Where to Dump JSON Messages (keyworded-result or messages)


def jsonDump(object, path, key):
    guild_id = object["guild_id"]
    channel_id = object["channel_id"]
    writeObject = {}

    server_response = requests.get(
        f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers
    )

    channel_response = requests.get(
        f"https://discord.com/api/v10/channels/{channel_id}", headers=headers
    )

    if server_response.status_code == 200 and channel_response.status_code == 200:
        guild_data = server_response.json()
        channel_data = channel_response.json()

    else:
        print("Cannot retrive Guild_ID and Channel_ID")
    channel_name = channel_data["name"]
    guild_name = guild_data["name"]
    writeObject["Server-Name"] = guild_name
    writeObject["Discord-Channel-Name"] = channel_name
    writeObject["Discord_object"] = object

    if path == "message":
        writeObject["Discord-keyword"] = key

        with open("result/messages.json", "a+") as w:
            json.dump(writeObject, w)

            w.write("\n")

    elif path == "keyword":
        writeObject["Discord-keyword"] = key

        with open("result/Keyworded-Result.json", "a+") as w:
            json.dump(writeObject, w)

            w.write("\n")


async def heartbeat(ws, interval, last_sequence):
    while True:
        await asyncio.sleep(interval)

        payload = {"op": 1, "d": last_sequence}

        await ws.send(json.dumps(payload))

        logging.info("Heartbeat packet sent.")


async def identify(ws):
    print("Identify")

    identify_payload = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"},
        },
    }

    await ws.send(json.dumps(identify_payload))
    logging.info("Identification sent.")


async def on_message(ws):
    print("Message Call")
    last_sequence = None
    while True:
        event = json.loads(await ws.recv())
        logging.info(f"Event received: {event}")
        op_code = event.get("op", None)

        if op_code == 10:
            interval = event["d"]["heartbeat_interval"] / 1000
            asyncio.create_task(heartbeat(ws, interval, last_sequence))

        elif op_code == 0:
            last_sequence = event.get("s", None)
            event_type = event.get("t")

            if event_type == "MESSAGE_CREATE":
                message = event["d"]["content"]
                logging.info(f"Message received from Discord: {message}")
                jsonDump(event["d"], "message", "null")
                SearchKeyword(event["d"])

        elif op_code == 9:
            logging.info("Invalid session. Starting a new session...")
            await identify(ws)


async def listner():
    while True:
        try:
            async with websockets.connect(discord_ws_url) as ws:
                await identify(ws)
                await on_message(ws)

        except websockets.exceptions.ConnectionClosed as e:
            print("Error")
            logging.error(
                f"WebSocket connection closed unexpectedly: {e}. Reconnecting..."
            )
            await asyncio.sleep(5)
            continue


