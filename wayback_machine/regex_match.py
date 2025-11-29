# from datetime import datetime, timedelta
# import re
# import json

# result=[]
# def sensitiveInfo(content):
#     data={}
#     regexIp = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
#     regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     fingerprint_regex = r'\b[0-9a-fA-F]{40,64}\b'
#     regex_port = r'port\s*[=:]?\s*(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d{1}|6553[0-5])\b'    
#     ipv6_regex = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
#     password_regex = r'(?:password|passcode)\s*[:=]?\s*(\S+)'
#     api_key_regex = r'^(?=.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d)[0-9a-zA-Z]{32,128}$'


#     hashes = {
#     "MySQL323": r'\b[0-9a-fA-F]{16}\b',
#     "MySQL4_5": r'\b[0-9a-fA-F]{40}\b',
#     "NTLM": r'\b[0-9a-fA-F]{32}\b',
#     "SHA1": r'\b[0-9a-fA-F]{40}\b',
#     "SHA2_224": r'\b[0-9a-fA-F]{56}\b',
#     "SHA2_256": r'\b[0-9a-fA-F]{64}\b',
#     "SHA2_512": r'\b[0-9a-fA-F]{128}\b',
#     "MD4": r'\b[0-9a-fA-F]{32}\b',
#     "Domain_Cached_Credentials_MS_Cache": r'\b[0-9a-fA-F]{32}:[0-9]+\b',
#     "sha512crypt_regex": r'\$6\$[0-9a-zA-Z./]{1,16}\$[0-9a-zA-Z./]+',
#     "apache_md5_regex" : r'\$apr1\$[0-9a-zA-Z]+\$[0-9a-zA-Z./]+',
#     "dcc2_regex" : r'\$DCC2\$[0-9]+#[a-zA-Z0-9]+#[0-9a-fA-F]+',
#     "md5": r'\b[0-9a-fA-F]{32}\b',
#     "lm": r'\b[0-9a-fA-F]{16}\b',
#     "oracle": r'\b[0-9a-fA-F]{16}:[0-9]+\b',
#     "bcrypt": r'\$2a\$[0-9]{2}\$[0-9a-zA-Z./]+:[0-9a-zA-Z./]+',
#     "sha1": r'\b[0-9a-fA-F]{40}\b',
#     "chap": r'\b[0-9a-fA-F]{32}:[0-9a-fA-F]{48}:[0-9a-fA-F]{2}\b',
#     "half_md5": r'\b[0-9a-fA-F]{16}\b',
#     "AIX_smd5": r'{smd5}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
#     "AIX_ssha256": r'{ssha256}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
#     "AIX_ssha512": r'{ssha512}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
#     "AIX_ssha1": r'{ssha1}[0-9a-zA-Z/.]+\$[0-9a-zA-Z/.]+',
#     "LastPass_LastPass_sniffed4": r'[0-9a-fA-F]{32}:[0-9]+:[^:]+',
#     "GRUB2": r'grub\.pbkdf2\.sha512\.[0-9]+\.[0-9a-fA-F]+',
#     "IPMI2_RAKP_HMAC_SHA1": r'[0-9a-fA-F]{64}',
#     "sha256crypt": r'\$5\$rounds=[0-9]+\$.{16}\$[0-9a-zA-Z/.]+',
#     "Kerberos_5_etype_23_AS_REQ_Pre_Auth": r'\$krb5pa\$23\$[^$]+\$[^$]+\$[0-9a-fA-F]+',
#     "SAP_CODVN_B_BCODE": r'USER\$[0-9A-F]+',
#     "SAP_CODVN_B_BCODE_from_RFC_READ_TABLE": r'[0-9A-F]{24}',
#     "SAP_CODVN_F_G_PASSCODE": r'USER\$[0-9A-F]+',
#     "SAP_CODVN_F_G_PASSCODE_from_RFC_READ_TABLE": r'[0-9A-F]{24}',
#     "Drupal7": r'\$S\$[0-9a-zA-Z./]+',
#     "Sybase_ASE": r'0x[0-9a-fA-F]+',
#     "Citrix_NetScaler_SHA1": r'[0-9a-fA-F]{40}',
# }

#     hash_matches = {}
#     for hash_name, hash_regex in hashes.items():
#         hash_matches[hash_name] = re.findall(hash_regex, content, re.IGNORECASE)


#     emails = re.findall(regex_email, content,re.IGNORECASE)
#     ips= re.findall(regexIp, content, re.IGNORECASE)
#     ipsV6= re.findall(ipv6_regex, content, re.IGNORECASE)
#     fingerprints= re.findall(fingerprint_regex, content, re.IGNORECASE)
#     ports= re.findall(regex_port, content, re.IGNORECASE)
#     passwords= re.findall(password_regex, content, re.IGNORECASE)
#     # api_key= re.findall(api_key_regex, content, re.IGNORECASE)
    

#     if not (ips or emails or fingerprints or ports or passwords):
#         print("no sensitive info found")
#     else:
        
#         data = { 
#     "IPs": ips,
#     "IPsV6": ipsV6,
#     "Fingerprints": fingerprints, 
#     "Emails": emails,
#     "Ports": ports,
#     "Passwords": passwords,
    
# }
        
#         json_data = json.dumps(data)

#         for hash_name, hash_values in hash_matches.items():
#             data[hash_name] = hash_values
#         json_data = json.dumps(data, indent=4)
#         print(json_data)
    

# with open('raw_data.txt', 'r') as file:
#     content = file.read()
#     sensitiveInfo(content)


import re
import json

def sensitiveInfo(content):
    data = {}
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
        "SAP_CODVN_B_BCODE": r'USER\$[0-9A-F]+',
        "SAP_CODVN_B_BCODE_from_RFC_READ_TABLE": r'[0-9A-F]{24}',
        "SAP_CODVN_F_G_PASSCODE": r'USER\$[0-9A-F]+',
        "SAP_CODVN_F_G_PASSCODE_from_RFC_READ_TABLE": r'[0-9A-F]{24}',
        "Drupal7": r'\$S\$[0-9a-zA-Z./]+',
        "Sybase_ASE": r'0x[0-9a-fA-F]+',
        "Citrix_NetScaler_SHA1": r'[0-9a-fA-F]{40}',
    }

    # hash_matches = {}
    # for hash_name, hash_regex in hashes.items():
    #     hash_values = re.findall(hash_regex, content, re.IGNORECASE)
    #     if hash_values:
    #         hash_matches["Archived_Hashes "+hash_name] = hash_values

    # emails = re.findall(regex_email, content, re.IGNORECASE)
    # if emails:
    #     data["Archived_Emails"] = emails

    # ips = re.findall(regexIp, content, re.IGNORECASE)
    # if ips:
    #     data["Archived_IPs"] = ips

    # ipsV6 = re.findall(ipv6_regex, content, re.IGNORECASE)
    # if ipsV6:
    #     data["Archived_IPsV6"] = ipsV6

    # fingerprints = re.findall(fingerprint_regex, content, re.IGNORECASE)
    # if fingerprints:
    #     data["Archived_Fingerprints"] = fingerprints

    # ports = re.findall(regex_port, content, re.IGNORECASE)
    # if ports:
    #     data["Archived_Ports"] = ports

    # passwords = re.findall(password_regex, content, re.IGNORECASE)
    # if passwords:
    #     data["Archived_Passwords"] = passwords

    # if data or hash_matches:
    #     alerts=json.dumps({**data, **hash_matches}, indent=2)
    hash_matches = {}
    for hash_name, hash_regex in hashes.items():
        hash_values = re.findall(hash_regex, content, re.IGNORECASE)
        if hash_values:
            hash_matches["Archived_"+hash_name] = hash_values

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

with open('file.txt', 'r') as file:
    content = file.read()
    alerts=sensitiveInfo(content)
    write_json_lines('alerts.json',alerts)
