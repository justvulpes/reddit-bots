import json
import pickle
import os

from pprint import pprint

from riotwatcher import RiotWatcher

watcher = RiotWatcher(os.environ["DEV_KEY"])


def make_dict():
    """Create a dictionary from data."""
    d = {}
    with open("champion_id") as f:
        for l in f:
            name, champ_id = l.strip().split(",")
            d[name] = int(champ_id)
            d[int(champ_id)] = name


def get_champ_dict():
    """Get dict from file using pickle. Dict has keys and values as champion id-s/names."""
    with open('champs.txt', "rb") as f:
        return pickle.loads(f.read())


def get_free_champs(w, region="NA1"):
    """Get the free champions from the current rotation using NA1 as the default region."""
    data = w.champion.all(region, free_to_play=True)["champions"]
    free_champs = []
    for champ in data:
        free_champs.append(get_champ_dict()[champ['id']])
    return free_champs


def main():
    """Run the script."""
    print(get_free_champs(watcher))
    # a = watcher.static_data.champion("EUN1", get_champs()["Kayle"], tags="spells")
    # a = watcher.static_data.champions("EUN1", tags="all")
    # pprint(watcher.static_data.champion("EUN1", get_champ_dict()["Brand"], tags="recommended"))

if __name__ == '__main__':
    main()
