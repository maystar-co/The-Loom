from telethon.sync import TelegramClient
from telethon import functions, events
from telethon.tl.functions.messages import GetHistoryRequest
import json
from datetime import date
from datetime import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv(".env")

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

client = TelegramClient("new-anon", api_id, api_hash)

with open("config/telegramInvite.txt", "r") as file:
    links = [line.strip() for line in file.readlines()]

# JSON serializer for storing date formats into JSON files


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return list(obj)


def SearchKeyword(object):
    file_path = "result/Keyworded-Result.json"
    with open("config/keywords.txt", "r") as file:
        keywords = [line.strip() for line in file.readlines()]
    with open(file_path, "a+") as file:
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            matches = re.findall(pattern, str(object), re.IGNORECASE)

            if matches:
                print("Match found:", object)
                print("Matching Keyword:", keyword)

                # Update the object with the matching keyword
                object["keyword"] = keyword

                # Save the matched information to a JSON file
                json.dump(object, file, default=json_serial)
                file.write("\n")


# Event Listener Func for fetchting new messages
@client.on(events.NewMessage(chats=links))
async def new_message_handler(event):
    chat = await event.get_chat()
    print(event)
    channel_messages = {}
    channel_name = chat.title

    # Create a JSON filename for the channel
    filename = "result/messages.json"
    channel_messages = {
        "channelName": channel_name,
        "date": event.date.isoformat(),
        "id": event.id,
        "text": event.message.text,
        "out": event.out,
        "from_scheduled": event.from_scheduled,
        "via_bot_id": event.via_bot_id,
        "from_id": event.from_id,
        "fwd_from": event.fwd_from,
        "ttl_period": event.ttl_period,
        "mentioned": event.mentioned,
        "media_unread": event.media_unread,
        "silent": event.silent,
        "post": event.post,
        "from_id": event.from_id,
        "reply_to_msg_id": event.reply_to_msg_id,
        "reply_markup": event.reply_markup.stringify() if event.reply_markup else None,
    }
    with open(filename, "a+") as file:
        json.dump(channel_messages, file, default=json_serial)
        file.write("\n")

    SearchKeyword(channel_messages)


# Func to fetch past Messages
async def fetch(link):
    await client.start()
    await client(functions.channels.JoinChannelRequest(link))
    offset_id = 0
    limit = 100
    total_messages = 0
    total_count_limit = 300  # Note : if total_count_limit = 0 means fetching all messages in a group that could take tons of time.
    my_channel = await client.get_entity(link)
    channelName = my_channel.title

    while True:
        print(
            "[+] Current Offset ID is:", offset_id, "; Total Messages:", total_messages
        )
        history = await client(
            GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        if not history.messages:
            break
        messages = history.messages
        with open(f"result/messages.json", "a+", encoding="utf-8") as w:
            for message in messages:
                message_data = {
                    "channelName": channelName,
                    "date": message.date.isoformat(),
                    "id": message.id,
                    "text": message.message,
                    "out": message.out,
                    "from_scheduled": message.from_scheduled,
                    "via_bot_id": message.via_bot_id,
                    "from_id": message.from_id,
                    "fwd_from": message.fwd_from,
                    "ttl_period": message.ttl_period,
                    "mentioned": message.mentioned,
                    "media_unread": message.media_unread,
                    "silent": message.silent,
                    "post": message.post,
                    "from_id": message.from_id,
                    "reply_to_msg_id": message.reply_to_msg_id,
                    "reply_markup": message.reply_markup.stringify()
                    if message.reply_markup
                    else None,
                }
                json.dump(message_data, w, default=json_serial)
                w.write("\n")
                total_messages += 1
                SearchKeyword(message_data)

        offset_id = history.messages[-1].id
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break  # break the loop if total messages is fetched.

    print(f"[+] Retrieved {total_messages} messages so far...")


if __name__ == "__main__":
    for link in links:
        try:
            with client:
                client.loop.run_until_complete(fetch(link))
                print(f"[+] Joined {link} successfully!")

        except Exception as e:
            print(f"An Error InCountered {link}. Reason: {e}")
            with open("config/Invalid.txt", "w") as file:
                file.write(f"An Error InCountered [{link}]. Reason: {e} \n")

    with client:
        client.run_until_disconnected()

    print("[+] Results are stored in /result")
