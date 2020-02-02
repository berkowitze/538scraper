import json
import requests
import os
from bs4 import BeautifulSoup as BS

NOTIFY = False  # send a desktop notification on change (Mac only)

# if either environment variable is not set, email won't be sent
# as of now, password must be to EMAIL account (didn't want to send updates to
# other people)
# NOTE: This has only been tested for gmail accounts as of now
# NOTE: Assuming gmail, you must also enable "less secure apps":
#       https://myaccount.google.com/lesssecureapps
EMAIL  = os.environ.get('fiveEMAIL') 
EMAIL_PASS = os.environ.get('fiveEMAILPASSWORD')

fav_url = 'https://fivethirtyeight.com/wp-content/themes/espn-fivethirtyeight/assets/images/favicon.ico?v=1.0.22'

# cd into project directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

with open('to_scrape.json') as f:
    to_scrape = json.load(f)

with open('data.json') as f:
    old_data = json.load(f)

# populate a url -> html dictionary
# this makes it so unique urls are only scraped once, saving time
names = set()
site_html = {}
for site in to_scrape:
    assert site['name'] not in names, \
        'Cannot have duplicate names in to_scrape.json'
    
    site_html[site['url']] = None

# download urls to html then a beautifulsoup object
for url in site_html:
    resp = requests.get(url)
    if not resp.ok:
        print(f'Error scraping {url}')
        continue

    html = resp.content.decode()
    site_html[url] = BS(html, 'html.parser')

# go through sites and pull out data matching selectors
new_data = {}
for site in to_scrape:
    html = site_html[site['url']]
    elems = html.select(site['selector'])
    if len(elems) != 1:
        print(f'No or ambiguous data for {site["name"]}')
        continue

    new_data[site['name']] = elems[0].text

# find data added or updated since last run and add to report
report = ''
for key in new_data:
    if key not in old_data:
        report += f'{key}: {new_data[key]}\n'
    elif new_data[key] != old_data[key]:
        report += f'{key}: {old_data[key]} -> {new_data[key]}\n'

# set old data to new data
with open('data.json', 'w') as f:
    json.dump(new_data, f, sort_keys=True, indent=2)

if report:
    if NOTIFY:
        from pync import Notifier
        Notifier.notify(report,
                        title='538 Updated',
                        open='https://fivethirtyeight.com',
                        appIcon=fav_url)

    if EMAIL and EMAIL_PASS:
        import yagmail
        yag = yagmail.SMTP(EMAIL, EMAIL_PASS)
        yag.send(to=EMAIL,
                 subject='538 Updated',
                 contents=[report])

