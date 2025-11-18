#!.env/bin/python3

import requests
from bs4 import BeautifulSoup

IANA_URL = "https://www.iana.org"
IANA_ROOT_DB_URL = f"{IANA_URL}/domains/root/db"

def get_tld_whois_server(link):
    r = requests.get(IANA_URL + link)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find("b", string="WHOIS Server:")
    if tag is None:
        return None
    return tag.next_sibling.strip() or None

def get_tld_list():
    r = requests.get(IANA_ROOT_DB_URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    tlds = []
    for link in soup.select(".domain.tld a"):
        tlds.append((
            link.text,
            link['href'],
        ))
    return tlds

def compile_list():
    conf = []
    for tld, tld_page in get_tld_list():
        whois_server = get_tld_whois_server(tld_page)
        if whois_server is None:
            print(f"[!] No whois server found for {tld}")
            continue
        regex = f"\\{tld}$ {whois_server}"
        conf.append(regex)
        print(f"[*] Found whois server for {tld}: {whois_server}")
    with open('whois.conf', 'w') as f:
        for line in conf:
            print(line)
            f.writeline(line)

if __name__ == '__main__':
    compile_list()
