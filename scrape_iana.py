#!.env/bin/python3

import requests
from bs4 import BeautifulSoup
import multiprocessing

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
        href = link['href']
        tlds.append((
            href.split('/')[len(href.split('/'))-1].split('.')[0],
            href,
        ))
    return tlds

def process_tld(inp):
    tld = inp[0]
    tld_page = inp[1]
    whois_server = get_tld_whois_server(tld_page)
    if whois_server is None:
        print(f"[!] No whois server found for {tld}")
        return None
    regex = f"\\{tld}$ {whois_server}"
    print(f"[*] Found whois server for {tld}: {whois_server}")
    return regex

def compile_list():
    tlds = get_tld_list()
    pool = multiprocessing.Pool(processes=32)
    conf = pool.map(process_tld, tlds)
    pool.close()
    pool.join()

    with open('whois.conf', 'w') as f:
        for line in conf:
            if line is None:
                continue
            print(line)
            f.write(line + "\n")

if __name__ == '__main__':
    compile_list()
