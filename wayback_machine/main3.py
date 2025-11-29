import csv
import re
import requests
import json
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def read_csv_to_list(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        final_list = sum(list(csv_reader), [])
    return final_list

def increment_archive_url(base_url, start_datetime_str):
    start_datetime = datetime.strptime(start_datetime_str, "%Y%m%d%H%M%S")
    new_datetime = start_datetime + timedelta(minutes=10)
    new_datetime_str = new_datetime.strftime("%Y%m%d%H%M%S")
    return f"{base_url}{new_datetime_str}/{base_url.split('/')[-1]}"

def generate_wayback_urls(base_url, start_datetime_str, end_datetime_str):
    urls = []
    while start_datetime_str < end_datetime_str:
        new_url = increment_archive_url(base_url, start_datetime_str)
        urls.append(new_url+end_url)
        start_datetime_str = new_url.split("/")[-2]
    return urls

def crawl_urls(urls):
    crawled_links = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a'):
                    crawled_links.append(link.get('href'))
        except RequestException as e:
            pass  
    return list(set(crawled_links))

def fix_broken_links(links):
    fixed_links = []
    for link in links:
        if isinstance(link, str):  # Check if link is a string
            clean_link = re.sub(r"[^\w/:@?\.~#&=+$%]", "", link)
        
        # Check if link already has the full format (https://web.archive.org/...)
        if "web.archive.org" in clean_link:
            fixed_links.append(clean_link)
        else:
            if clean_link.startswith("/web/"):
                fixed_links.append(f"https://web.archive.org{clean_link}")
            else:
                pass

    # Remove comments and "expand/close"
    filtered_links = [link for link in fixed_links if not link.startswith("#")]
    return filtered_links

def write_list_to_csv(links, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

def scrape_urls(start_urls):
    for url in start_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                visible_text = soup.get_text(separator=" ",strip=True)
                save_text(visible_text)
            
        except RequestException as e:
            pass
        
def save_text(text):
    with open('raw_data.txt', 'a', encoding='utf-8') as f:
        f.write(text)

def sensitiveInfo(content):
    regexIp = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    fingerprint_regex = r'\b[0-9a-fA-F]{40,64}\b'
    regex_port = r'port\s*[=:]?\s*(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d{1}|6553[0-5])\b'
    ipv6_regex = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
    password_regex= r'(?:password|passcode)[:=]\s*(.*)'

    
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
            hash_matches["Archived_Hashes "+hash_name] = hash_values

    emails = re.findall(regex_email, content, re.IGNORECASE)
    if emails:
        data = {"Archived_Emails": emails}
        yield json.dumps(data)

    ips = re.findall(regexIp, content, re.IGNORECASE)
    if ips:
        data = {"Archived_IPs": ips}
        yield json.dumps(data)

    ipsV6 = re.findall(ipv6_regex, content, re.IGNORECASE)
    if ipsV6:
        data = {"Archived_IPsV6": ipsV6}
        yield json.dumps(data)

    fingerprints = re.findall(fingerprint_regex, content, re.IGNORECASE)
    if fingerprints:
        data = {"Archived_Fingerprints": fingerprints}
        yield json.dumps(data)

    ports = re.findall(regex_port, content, re.IGNORECASE)
    if ports:
        data = {"Archived_Ports": ports}
        yield json.dumps(data)

    passwords = re.findall(password_regex, content, re.IGNORECASE)
    if passwords:
        data = {"Archived_Passwords": passwords}
        yield json.dumps(data)

    if hash_matches:
        for hash_name, hash_values in hash_matches.items():
            data = {hash_name: hash_values}
            yield json.dumps(data)

def write_json_lines(output_file, content):
    with open(output_file, 'a') as file:
        for line in content:
            file.write(line + '\n')

if __name__ == "__main__":
    yesterday = datetime.now() - timedelta(days=1350)
    today = datetime.now()
    
    start_datetime_str = yesterday.strftime("%Y%m%d%H%M%S")
    end_datetime_str = today.strftime("%Y%m%d%H%M%S")

    base_url = "https://web.archive.org/web/"
    end_url = "https://www.bobble.ai/en/home"
    urls = generate_wayback_urls(base_url, start_datetime_str, end_datetime_str)
    
    write_list_to_csv(urls, "wayback_urls.csv")
    
    start_urls = read_csv_to_list("wayback_urls.csv")
    crawled_links = crawl_urls(start_urls)
    
    cleaned_links = fix_broken_links(crawled_links)
    
    scrape_urls(cleaned_links)
    with open('raw_data.txt', 'r') as file:
        content = file.read()
        json_lines = sensitiveInfo(content)
        write_json_lines('result/sensitive_info.json', json_lines)
    
