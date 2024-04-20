import os
import time

from tqdm import tqdm
from srctools import game as srcgame, bsp
import json
import zipfile

jsonFolder = os.path.join(os.getcwd(), 'Assets')
jsonassets = []


def init():
    print("Searching for json files...")
    jsonlist = os.listdir(jsonFolder)
    pbar = tqdm(range(len(jsonlist)))
    for i in pbar:
        pbar.set_description(f"Indexing {jsonlist[i]}")
        time.sleep(.1)
        if '.json' in jsonlist[i]:
            jsonassets.append(os.path.join(jsonFolder, jsonlist[i]))
    time.sleep(.5)
    print(f"Found and indexed {len(jsonassets)} json files.")
    time.sleep(.2)
    print("Completed.")
    time.sleep(2)
    clear()
    start()


def start():
    print(
        """Welcome to Kenzo's Awesome Credits Checker!
Select a mode:
[A] Add a new asset
[F] Find an asset in a map
[Q] Quit"""
    )
    mode = input()
    if mode in ["a", "f", "q"]:
        if mode == "a":
            pass
            # add()
            # TODO: Implement add function
        elif mode == "f":
            find()
        elif mode == "q":
            quit()
    else:
        clear()
        start()


# def add():
# TODO: Implement add function

def find():
    mappath = input("Enter the name of the map: ")
    mapf = bsp.BSP(f"D:/Steam/steamapps/common/Portal 2/portal2/maps/{mappath}.bsp")
    paklist = mapf.pakfile.namelist()
    foundassets = search(paklist)
    print(f"Found {len(foundassets)} assets")
    # TODO: Add credits generator and declarer.


def search(paklist):
    foundassets = []
    print("Searching for assets...")
    pbar = tqdm(range(len(jsonassets)))
    for i in pbar:
        pbar.set_description(f"Searching {jsonassets[i]}")
        with open(jsonassets[i], 'r') as f:
            json_obj = json.load(f)
            asset_paths = json_obj['assetPaths']
            for path in asset_paths:
                if path in paklist:
                    print(foundassets)
                    # TODO: Figure out how to check if the asset is already in the list
                    if path not in foundassets:
                        print(f"Found {path}")
                        foundassets.append(jsonassets[i])
    return foundassets

def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    elif os.name == "java":
        os.system("clear")


init()
