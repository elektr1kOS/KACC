"""idk pylint wants me to add a module docstring"""
import os
import sys
import time
import json

from tqdm import tqdm
from srctools import bsp
from tkinter import filedialog as fd

jsonFolder = os.path.join(os.path.dirname(os.getcwd()), 'Assets')
jsonassets = []


def init():
    """Searches asset folder for asset configs, and adds the file path to a list."""
    print("Searching for json files...")
    # Searches the "Assets" folder for files
    jsonlist = os.listdir(jsonFolder)
    # Defines a progress bar
    pbar = tqdm(range(len(jsonlist)))
    # Shows progress bar. 'i' is the current iteration of the progress bar.
    for i in pbar:
        # Changes progress bar description
        pbar.set_description(f"Indexing {jsonlist[i]}")
        # Sleep makes sure print order is correct.
        time.sleep(.1)
        if '.json' in jsonlist[i]:
            # If the file is a json file, add it to a file.
            jsonassets.append(os.path.join(jsonFolder, jsonlist[i]))
    # Sleep for order
    time.sleep(.5)
    print(f"Found and indexed {len(jsonassets)} json files.")
    # Sleep for order
    time.sleep(.2)
    print("Completed.")
    # Windows troubleshooting moment
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
    # Checks if the input is valid
    # TODO: Change this to use while loop like used in find() function.
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
    # Defines bsp file.
    mapf = bsp.BSP(fd.askopenfilename())
    # Gets the pack file of the map. In ZipFile object.
    paklist = mapf.pakfile.namelist()
    # See search function for more info.
    foundassets = search(paklist)
    print("Generating credits...")
    # Defines progress bar
    pbar = tqdm(range(len(foundassets)))
    creditlist = []
    for i in pbar:
        # Using with automatically closes opened file when finished.
        with open(foundassets[i], 'r', encoding="UTF-8") as f:
            json_obj = json.load(f)
            # Check credit type. 0 is Don't credit, 1 is preferred, 2 is required.
            if json_obj['creditType'] != "0":
                if json_obj['creditType'] == "1":
                    # Keeps looping until a valid input is given.
                    while manualcredit not in ['y', 'n', 'yes', 'no']:
                        manualcredit = input(f"""Looks like {json_obj['assetName']} has the credit type set to preferred.
                        Would you like to credit {json_obj['assetAuthor']}? [Y/N]""").lower()
                # If user decides to credit, or the asset is required.
                if manualcredit in ['y', 'yes'] or json_obj['creditType'] == "2":
                    creditlist.append(foundassets[i])
    # TODO: Implement credit list generation.

def search(paklist):
    """Searches for assets in asset configs and checks if they are in the map."""
    foundassets = []
    print("Searching for assets...")
    # Defines progress bar
    pbar = tqdm(range(len(jsonassets)))
    for i in pbar:
        pbar.set_description(f"Searching {jsonassets[i]}")
        # Searches a json file for asset paths.
        with open(jsonassets[i], 'r', encoding="UTF-8") as f:
            json_obj = json.load(f)
            asset_paths = json_obj['assetPaths']
            # Loops through asset paths in json file.
            for path in asset_paths:
                # Checks if json asset path is in map pak file and if it's already been found.
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
