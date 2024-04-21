"""idk pylink wants me to add a module docstring"""
import os
import sys
import time
import json

from tqdm import tqdm
from srctools import bsp
from tkinter import filedialog as fd

jsonFolder = os.path.join(os.getcwd(), "..", 'Assets')
jsonassets = []


def init():
    """Searches asset folder for asset configs, and adds the file path to a list."""
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
    """Starting UI to select a mode."""
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
            sys.exit()
    else:
        clear()
        start()


# def add():
# TODO: Implement add function

def find():
    """Searches for assets in a map."""
    mapf = bsp.BSP(fd.askopenfilename())
    paklist = mapf.pakfile.namelist()
    foundassets = search(paklist)


def search(paklist):
    """Searches for assets in asset configs and checks if they are in the map."""
    foundassets = []
    print("Searching for assets...")
    pbar = tqdm(range(len(jsonassets)))
    for i in pbar:
        pbar.set_description(f"Searching {jsonassets[i]}")
        with open(jsonassets[i], 'r', encoding="UTF-8") as f:
            json_obj = json.load(f)
            asset_paths = json_obj['assetPaths']
            for path in asset_paths:
                if path in paklist and jsonassets[i] not in foundassets:
                    time.sleep(.1)
                    print(f"Found {json_obj['assetName']}")
                    foundassets.append(jsonassets[i])
    return foundassets


def clear():
    """Natively clears the console."""
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    elif os.name == "java":
        os.system("clear")


init()
