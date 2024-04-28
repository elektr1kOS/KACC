from kacc import *

# Global Variables.
jsonassets = []

for root, dirs, files in os.walk(".", topdown=False, followlinks=True):
    for name in files:
        if name.endswith("Assets"):
            jsonFolder = name
            print(jsonFolder)
            break


def cliinit():
    """Searches asset folder for asset configs, and adds the file path to a list."""
    print("Searching for json files...")
    # Searches the "Assets" folder for files
    jsonlist = os.listdir(jsonFolder)
    pbar = tqdm(range(len(jsonlist)), desc="Search and Indexing json files...")
    for i in pbar:
        jsonassets.append(os.path.join(jsonFolder, indexThrJson(jsonlist, currentiter=i)))
        print(jsonassets)
    # Sleep for order
    time.sleep(.1)
    print(f"Found and indexed {len(jsonassets)} json files.")
    clearConsole()
    clistart()


def clistart():
    """Starting UI to select a mode."""
    print(
        """Welcome to Kenzo's Awesome Credits Checker!
Select a mode:
[A] Add a new asset
[F] Find an asset in a map
[Q] Quit"""
    )
    # Checks if the input is valid
    mode = ""
    while mode not in ["a", "f", "q"]:
        mode = input()
    if mode == "a":
        createAsset()
    elif mode == "f":
        clifind()
    elif mode == "q":
        sys.exit()


def clifind():
    """Searches for assets in a map."""
    # Gets the pack file of the map. In ZipFile object.
    paklist = getPakList()
    # See search function for more info.
    foundassets = clicomparePakFile(paklist)
    print("Generating credits...")
    creditlist = getcredittype(foundassets)
    generateCredits(creditlist)



def clicomparePakFile(paklist):
    """Searches for assets in asset configs and checks if they are in the map."""
    foundassets = []
    print("Searching for assets...")
    # Defines progress bar
    pbar = tqdm(range(len(jsonassets)))
    for i in pbar:
        pbar.set_description(f"Searching {jsonassets[i]}")
        # Searches a json file for asset paths.
        foundassets = comparePakFile(jsonassets, currentiter=i, paklist=paklist)
    return foundassets


cliinit()
