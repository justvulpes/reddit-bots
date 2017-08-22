import json
import pickle
import random

import bs4
import praw
from pprint import pprint
import requests
from textwrap import dedent

from credentials import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT, DEV_KEY

SUBREDDIT = "2007scape"
PETS = {
    "Abyssal orphan": 2560,
    "Baby mole": 3000,
    "Callisto cub": 2000,
    "Hellpuppy": 3000,
    "Jal-nib-rek": 100,
    "Kalphite princess": 3000,
    "Olmlet": 65,
    "Pet chaos elemental": 300,
    "Pet dagannoth prime": 5000,
    "Pet dagannoth rex": 5000,
    "Pet dagannoth supreme": 5000,
    "Pet dark core": 5000,
    "Pet general graardor": 5000,
    "Pet k'ril tsutsaroth": 5000,
    "Pet kraken": 3000,
    "Pet kree'arra": 5000,
    "Pet penance queen": 1000,
    "Pet smoke devil": 3000,
    "Pet snakeling": 4000,
    "Pet zilyana": 5000,
    "Prince black dragon": 3000,
    "Scorpia's offspring": 2000,
    "Skotos": 65,
    "Tzrek-jad": 200,
    "Venenatis spiderling": 2000,
    "Vet'ion jr.": 2000
}

PETS_LOWER = {k.lower(): v for k, v in PETS.items()}


def get_data(use_cached=False, lower=True):
    """Scrape data from the wiki."""
    if use_cached:
        with open('pets_data.pickle', 'rb') as f:
            pet_data = pickle.load(f)
    else:
        data = []
        pet_data = {}
        r = requests.get('http://oldschoolrunescape.wikia.com/wiki/Pet')
        soup = bs4.BeautifulSoup(r.text, "html5lib")
        contents = soup.find(class_='wikitable')
        for table in contents.find_all('tr'):
            cols = [ele.text.strip() for ele in table.find_all('td')]
            data.append([ele for ele in cols if ele])
        for pet in data[1:]:
            pet_data[pet[0]] = (pet[1], pet[2])
        with open('pets_data.pickle', 'wb') as handle:
            pickle.dump(pet_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if lower:
        return {k.lower(): v for k, v in pet_data.items()}
    return pet_data


def main():
    """Run the script."""
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME,
                         password=PASSWORD, user_agent=USER_AGENT)

    rbots = reddit.subreddit(SUBREDDIT)

    for comment in rbots.stream.comments():
        process_comment(comment)


def process_comment(comment):
    """Process an incoming comment.
    @pet <petname>
    """
    call_out = "@pet"
    if comment.body.startswith(call_out):
        comment.refresh()
        if USERNAME in [c.author.name for c in comment.replies.list()]:
            return
        try:
            pet = comment.body.split("@pet")[1].split("<")[1].split(">")[0].lower()
            pet_data = get_data(use_cached=False, lower=True)
            if pet not in PETS_LOWER:
                return
            odds = PETS_LOWER[pet]
            if pet in PETS_LOWER:
                rolls = roll_pet(odds)
                result = f"**It took you {rolls} roll{'' if rolls == 1 else 's'} to get the pet!**"
                source, drop_rate = pet_data[pet]
                drop_rate = drop_rate.replace("\n", " ")  # bug fix
                comment.reply(result + dedent("""

                &nbsp;

                Pet | Source | Drop rate
                ---------|----------|----------
                """ + f"{pet.upper()} | {source} | {drop_rate}"))
                print("Replied to a comment.")
        except Exception as e:  # catch everything blindly
            print(f"Bad call: {e}")


def roll_pet(n):
    """Roll for a pet."""
    count = 1
    while True:
        if random.randint(0, n) == n:
            break
        count += 1
    return count


def pastebin(string):
    """Make a new pastebin with string being the content,
    return url of created pastebin."""
    # defining the api-endpoint
    API_ENDPOINT = "http://pastebin.com/api/api_post.php"

    # data to be sent to api
    data = {'api_dev_key': DEV_KEY,
            'api_option': 'paste',
            'api_paste_code': string}

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    pastebin_url = r.text
    print(f"The pastebin URL is:{pastebin_url}")


if __name__ == '__main__':
    print("Script started!")
    main()
