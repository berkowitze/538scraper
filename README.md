# 538 Scraper

## About
This tool can be used to get desktop and/or email notifications when specified text on specified websites is updated (it was made for 538, but will work for any site).

The sites to be scraped are managed in a JSON file. Stick the script onto a server or computer that's on a lot of the time, and add a cronjob to run it every few minutes for the best experience!

## Installation
1. Download the git repo: `git clone https://github.com/berkowitze/538scraper`

2. Go into the folder: `cd 538scraper`

3. Create a Python 3.7+ virtual environment: `virtualenv venv` or `virtualenv -p /path/to/python/executable venv`

4. Activate the environment: `source venv/bin/activate`

5. Install required packages: `pip install -r ./requirements.txt`

6. Using the virtual environment executable (in `./venv/bin/python`), run `scrape.py`: `python scrape.py` - it should run.

## How it works/setup
1. The script will go through each dictionary in to_scrape.json and download the content from the 'url' value.

2. The script will then go to the selector specified in the 'selector' value, and grab the text from that html element.

3. If that text is different from the last time the scraper was run, OR the 'name' value has not been seen before, it will be added to the "report".

4. Once all site/selector dictionaries have been processed, you will either be sent a push notification (Mac only) or an email (additional setup required).

5. To get push notifications on a Mac, cahnge NOTIFY to True on line 6 of the script

6. To get emails, go into your .bashrc, .bash_profile, or .profile and add two environment variables (only tested for gmail accounts):
```bash
export fiveEMAIL="youremailhere@gmail.com"
export fiveEMAILPASSWORD="passwordfortheaboveemail"
```

7. Data is saved in data.json for use in the next time `scrape.py` is run.

8. As of now, `to_scrape.json` has two targets, which are Trump's approval and disapproval rating. During election season, I'll add polling numbers.

### Adding to to_scrape.json
There are three components:
- name: A user-friendly descriptor of the text that is being checked
- url: The url to the HTML content to download
- selector: The CSS selector to the specific element to be scraped.

Note 1: The URL may not be the same URL in the URL bar, because 538 uses iframes quite a bit. If the toplevel URL isn't working, find the iframe containing the target element. To do so (in Chrome), press Cmd-Shift-C (Ctrl-Shift-C Windows) to open the page inspector and click the element. Find its parent iframe and use that url instead.

Note 2: To find the CSS selector (in Chrome), press Cmd-Shift-C (Ctrl-Shift-C Windows) to open the page inspector and click the element. In the inspector, the html element will be revealed. Right click on it and select Copy > Copy selector. Paste this into the 'selector' value.

### Running a cron tab
[Here's a tutorial on crontabs](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/)

1. Run `crontab -e`.

2. Add a line for the job: `*/5 * * * * export fiveEMAIL="youremailhere@gmail.com"; export fiveEMAILPASSWORD="yourpasswordhere"; /path/to/538scrape/venv/bin/python /path/to/538scrape/scrape.py`. This will run the scraper every 5 minutes.

Note: The reason you need the environment variables here is that cronjobs don't have access to your normal environment variables (as it's run as sudo and in a different shell).

3. Save and quit.

