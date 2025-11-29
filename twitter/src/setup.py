import os
import subprocess

try:
    os.mkdir("result")
    print("[+] Created 'telegram' Directory")
except FileExistsError:
    pass

try:
    os.mkdir("config")
    print("[+] Created 'telegram' Directory")
except FileExistsError:
    pass

print("[+] Installing Required Packages")
subprocess.check_call(["pip", "install", "ntscraper", "tqdm"])
