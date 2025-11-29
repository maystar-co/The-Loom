import threading
from scraper import scraper
from listener import listner
import asyncio


async def run_async_function():
    await listner()

if __name__ == "__main__":
    t1 = threading.Thread(target=scraper)
    t2 = threading.Thread(target=asyncio.run, args=(run_async_function(),))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Main Thread Collapsed")
    # ctrl+c won't terminate the program because of GIL (global interpreter lock) on threads.
