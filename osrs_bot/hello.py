import requests
import bs4

def get_data(use_cached=False, lower=True):
    """Scrape data from the wiki."""
    if use_cached:
        pass
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
    if lower:
        return {k.lower(): v for k, v in pet_data.items()}
    return pet_data


# print(get_data())
