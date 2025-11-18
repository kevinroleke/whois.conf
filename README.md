# whois.conf

An up-to-date `/etc/whois.conf` for the `whois` CLI (Marco d'Itri, GNU GPL).
Automatically generated every day from scraping IANA root DB.

## Why this exists
1. Run `whois zerogon.consulting`
2. Realize that your bleeding edge Linux distribution doesn't include whois servers for any post-2013 gTLDs
3. Google "updated whois.conf"
4. Realize all the results are old with the latest from 2017

## TLDs without whois
For TLDs without a whois server listed by IANA, we check if an RDAP server is listed.
If so, use a [whois-to-rdap proxy](https://github.com/kevinroleke/whois-to-rdap).
If not, leave blank.

## Usage
```bash
# Clone repo
git clone https://github.com/kevinroleke/whois.conf.git
cd whois.conf

# Install dependencies
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

# Run and update whois.conf
python scrape_iana.py
sudo cp whois.conf /etc/whois.conf

# Test
whois zerogon.consulting # now we get results from updated whois server or RDAP proxy for new gTLDs
```
