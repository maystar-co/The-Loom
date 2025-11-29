import os
import subprocess

try:
    os.mkdir(f"config")
    print("[+] Created 'config' Directory")
except FileExistsError:
    pass

try:
    os.mkdir(f"result")
    print("[+] Created 'result' Directory")
except FileExistsError:
    pass


print("[+] Installing Required Packages")
subprocess.check_call(["pip", "install", "requests", "beautifulsoup4", "pysocks"])