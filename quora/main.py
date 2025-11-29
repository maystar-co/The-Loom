import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import re

#if invalid use different account  
email = "ayjanalodu@gmail.com"
password = "Admin@123"

#saves  the cookies 
def login_quora(email, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open Quora login page
    driver.get('https://www.quora.com')
    
    time.sleep(2)
    # Find and fill the email and password fields
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    time.sleep(2)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    time.sleep(2)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)  
    driver.refresh()
    cookies = driver.get_cookies()
    driver.quit()
    with open("cookies.json", "w") as file:
        json.dump(cookies, file, indent=4)

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def are_cookies_valid(driver):
    driver.get("https://www.quora.com/")
    try:
        if driver.find_element(By.NAME, "email"):
            return False
    except:
        return True

def set_cookies():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.quora.com/")
    time.sleep(1)

    with open('cookies.json', 'r') as file:
        cookies = json.load(file)
    
    for cookie in cookies:
        # Remove 'sameSite' attribute if it exists (Selenium may not support it)
        if 'sameSite' in cookie:
            del cookie['sameSite']
        driver.add_cookie(cookie)

    driver.refresh()
    if not are_cookies_valid(driver):
        # If cookies are not valid, implement code to obtain new session cookies here
        login_quora(email,password)
        set_cookies()

    return driver

def answer_links_scraper(driver):
    with open("keywords.txt", "r") as file:
        keywords = file.readlines()

    keywords = [keyword.strip() for keyword in keywords]

    for keyword in keywords:
        search_query = urllib.parse.quote(keyword)
        url = f"https://www.quora.com/search?q={search_query}&type=answer"
    
        driver.get(url)
    
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.q-box.qu-borderBottom'))
        )

        links = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            answer_links = driver.find_elements(By.CSS_SELECTOR, 'a.q-box')
            
            for link in answer_links:
                url = link.get_attribute('href')
                if url and '/answer/' in url:
                    links.add(url)
            
            scroll_to_bottom(driver)
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        with open("quora_answer_links.txt", "a") as file:
            for link in links:
                file.write(link + "\n")
        
    scrapetext(driver)

    driver.quit()

def scrapetext(driver):
    
    try:
        with open("quora_answer_links.txt", "r") as file:
            questions = file.readlines()

        for question_url in questions:
            driver.get(question_url.strip())  
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "q-box")))

            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')

            answer_texts = []

            # Extract all text content from different types of answer containers
            for tag, class_name in [('p', 'q-text qu-display--block qu-wordBreak--break-word qu-textAlign--start'),
                                    ('li', 'q-relative'),
                                    ('ol', 'q-box'),
                                    ('div', 'q-text qu-wordBreak--break-word'),
                                    ('div', 'q-box spacing_log_answer_content puppeteer_test_answer_content')]:
                content_divs = soup.find_all(tag, class_=class_name)
                for i, div in enumerate(content_divs):
                    text = div.get_text(separator=' ', strip=True)
                    answer_texts.append(f"{text}\n")
            
            # Write all answers to the raw_data.txt file
            with open("raw_data.txt", "a", encoding="utf-8") as raw_file:
                raw_file.write(f"Answers from: {question_url}\n\n")
                raw_file.write("\n".join(answer_texts))
                raw_file.write("\n\n")

    finally:
        driver.quit()


def sensitiveInfo(content):
    regexIp = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    fingerprint_regex = r'\b[0-9a-fA-F]{40,64}\b'
    regex_port = r'port\s*[=:]?\s*(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d{1}|6553[0-5])\b'
    ipv6_regex = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
    password_regex= r'(?:password|passcode)[:= ]\s*(.*)'

    
    hashes = {
        "MySQL323": r'\b[0-9a-fA-F]{16}\b',
        "MySQL4_5": r'\b[0-9a-fA-F]{40}\b',
        "NTLM": r'\b[0-9a-fA-F]{32}\b',
        "SHA1": r'\b[0-9a-fA-F]{40}\b',
        "SHA2_224": r'\b[0-9a-fA-F]{56}\b',
        "SHA2_256": r'\b[0-9a-fA-F]{64}\b',
        "SHA2_512": r'\b[0-9a-fA-F]{128}\b',
        "MD4": r'\b[0-9a-fA-F]{32}\b',
        "Domain_Cached_Credentials_MS_Cache": r'\b[0-9a-fA-F]{32}:[0-9]+\b',
        "sha512crypt_regex": r'\$6\$[0-9a-zA-Z./]{1,16}\$[0-9a-zA-Z./]+',
        "apache_md5_regex": r'\$apr1\$[0-9a-zA-Z]+\$[0-9a-zA-Z./]+',
        "dcc2_regex": r'\$DCC2\$[0-9]+#[a-zA-Z0-9]+#[0-9a-fA-F]+',
        "md5": r'\b[0-9a-fA-F]{32}\b',
        "lm": r'\b[0-9a-fA-F]{16}\b',
        "oracle": r'\b[0-9a-fA-F]{16}:[0-9]+\b',
        "bcrypt": r'\$2a\$[0-9]{2}\$[0-9a-zA-Z./]+:[0-9a-zA-Z./]+',
        "sha1": r'\b[0-9a-fA-F]{40}\b',
        "chap": r'\b[0-9a-fA-F]{32}:[0-9a-fA-F]{48}:[0-9a-fA-F]{2}\b',
        "half_md5": r'\b[0-9a-fA-F]{16}\b',
        "AIX_smd5": r'{smd5}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
        "AIX_ssha256": r'{ssha256}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
        "AIX_ssha512": r'{ssha512}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
        "AIX_ssha1": r'{ssha1}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
        "LastPass_LastPass_sniffed4": r'[0-9a-fA-F]{32}:[0-9]+:[^:]+',
        "GRUB2": r'grub\.pbkdf2\.sha512\.[0-9]+\.[0-9a-fA-F]+',
        "IPMI2_RAKP_HMAC_SHA1": r'[0-9a-fA-F]{64}',
        "sha256crypt": r'\$5\$rounds=[0-9]+\$.{16}\$[0-9a-zA-Z/.]+',
        "Kerberos_5_etype_23_AS_REQ_Pre_Auth": r'\$krb5pa\$23\$[^$]+\$[^$]+\$[0-9a-fA-F]+',
        "Drupal7": r'\$S\$[0-9a-zA-Z./]+',
        "Sybase_ASE": r'0x[0-9a-fA-F]+',
        "Citrix_NetScaler_SHA1": r'[0-9a-fA-F]{40}',
    }

    hash_matches = {}
    for hash_name, hash_regex in hashes.items():
        hash_values = re.findall(hash_regex, content, re.IGNORECASE)
        if hash_values:
            hash_matches["Hashes "+hash_name] = hash_values

    emails = re.findall(regex_email, content, re.IGNORECASE)
    if emails:
        data = {"Emails": emails}
        yield json.dumps(data)

    ips = re.findall(regexIp, content, re.IGNORECASE)
    if ips:
        data = {"IPs": ips}
        yield json.dumps(data)

    ipsV6 = re.findall(ipv6_regex, content, re.IGNORECASE)
    if ipsV6:
        data = {"IPsV6": ipsV6}
        yield json.dumps(data)

    fingerprints = re.findall(fingerprint_regex, content, re.IGNORECASE)
    if fingerprints:
        data = {"Fingerprints": fingerprints}
        yield json.dumps(data)

    ports = re.findall(regex_port, content, re.IGNORECASE)
    if ports:
        data = {"Archived_Ports": ports}
        yield json.dumps(data)

    passwords = re.findall(password_regex, content, re.IGNORECASE)
    if passwords:
        data = {"Passwords": passwords}
        yield json.dumps(data)

    if hash_matches:
        for hash_name, hash_values in hash_matches.items():
            data = {hash_name: hash_values}
            yield json.dumps(data)

def write_json_lines(output_file, content):
    with open(output_file, 'a') as file:
        for line in content:
            file.write(line + '\n')


def find_sensitive_info():
    with open('raw_data.txt', 'r') as file: 
            content = file.read()
            json_lines = sensitiveInfo(content)
            write_json_lines('result/sensitive_info.json', json_lines)


#running the code 
driver=set_cookies()
answer_links_scraper(driver)
find_sensitive_info()
