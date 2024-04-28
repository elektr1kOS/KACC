"""idk pylint wants me to add a module docstring"""
import os
import shutil
import sys
import time
import json

from tkinter import Listbox
from tqdm import tqdm
from srctools import bsp
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import askyesno
from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledFrame
import webbrowser
import runpy

# FIXME: Currently changed since we are in src/. Change on release.
jsonFolder = "tests/Assets"


def ask_multiple_choice_question(prompt, options_dict, buttons, buttoncommands, wintitle):
    multiprompt = Window(title=wintitle, themename="darkly")
    multiprompt.resizable(False, False)
    if prompt:
        Label(multiprompt, text=prompt, font=('Inter', 15)).pack(padx=20, pady=10)
    v = IntVar()
    radiosscroll = ScrolledFrame(multiprompt, autohide=True)
    radiosscroll.pack(padx=10, pady=10, fill=BOTH, expand=True)
    for i, (key, option) in enumerate(options_dict.items()):
        Radiobutton(radiosscroll, text=option, variable=v, value=i).pack(anchor="w", pady=7, padx=10)
    buttons_frame = Frame(multiprompt)
    buttons_frame.pack(anchor="s", pady=15)
    for i, option in enumerate(buttons):
        Button(buttons_frame, text=option, command=buttoncommands[i]).pack(anchor="s", padx=10, side=LEFT)
    Button(buttons_frame, text="Submit", command=multiprompt.destroy).pack(anchor="s", padx=10, side=LEFT)
    multiprompt.mainloop()
    return list(options_dict.keys())[v.get()]


def indexThrJson(jsonlist, currentiter):
    """Checks if given file is json, and appends to jsonassets."""
    if '.json' in jsonlist[currentiter]:
        # If the file is a json file, add it to a file.
        return jsonlist[currentiter]
    return


def comparePakFile(jsonassets, currentiter, paklist):
    foundassets = []
    with open(jsonassets[currentiter], 'r', encoding="UTF-8") as f:
        json_obj = json.load(f)
        asset_paths = json_obj['assetPaths']
        # Loops through asset paths in json file.
        for path in asset_paths:
            # Checks if json asset path is in map pak file and if it's already been found.
            if path in paklist and jsonassets[currentiter] not in foundassets:
                time.sleep(.1)
                print(f"Found {json_obj['assetName']}")
                foundassets.append(jsonassets[currentiter])
    return foundassets


def generateCredits(creditlist):
    creditformat = ""
    authorassets = {}
    with open("config.json", 'r', encoding='UTF-8') as f:
        config_obj = json.load(f)
        creditformats_dict = {key: value['displayName'] for key, value in config_obj['creditformats'].items()}
        creditselection = ask_multiple_choice_question(prompt="Select how you want the credits to be formatted:",
                                                       options_dict=creditformats_dict,
                                                       buttons=["Want something custom?"],
                                                       buttoncommands=[
                                                           lambda: webbrowser.open("google.com", autoraise=True)],
                                                       wintitle="Select Credit Format"
                                                       )
        creditformat = config_obj['creditformats'][creditselection]['format']
    formattedcredits = []
    for i in creditlist:
        with open(i, 'r', encoding='UTF-8') as f:
            json_obj = json.load(f)
            assetauthor = json_obj['assetAuthor']
            assetname = json_obj['assetName']
            if assetauthor in authorassets:
                authorassets[assetauthor].append(assetname)
            else:
                authorassets[assetauthor] = [assetname]
    # TODO: Implement generating file.
    with open(asksaveasfile(defaultextension=".txt",
                            filetypes=[('Text File', '.txt')]).name, 'a', encoding='UTF-8') as f:
        for author, assets in authorassets.items():
            f.write(creditformat.format(assetname=", ".join(assets), authorname=author).join("\n"))
        if askyesno("Open file?", "Done! The credits document has been generated. \nWould you like to open it in the "
                                  "default text editor?"):
            os.startfile(f.name)
    return


def createAsset():
    def assetsubmit():
        if assetname.get() and authorname.get() and pathslistbox.size() > 0 and credittype.get():
            newasset = {
                "assetName": assetname.get(),
                "assetAuthor": authorname.get(),
                "assetDescription": descriptiontextbox.get("1.0", "end-1c"),
                "assetPaths": list(pathslistbox.get(0, "end")),
                "creditType": credittype.get()
            }
            with open(os.path.join(jsonFolder,
                                   f"{Querybox.get_string(prompt="Please enter a name for the json file. Don't include '.json'")}.json"),
                      'w', encoding='UTF-8') as f:
                json.dump(newasset, f, indent=4)
            newassetwin.destroy()
        else:
            errortext.pack()
            pass

    newassetwin = Window(title="Create a new asset", themename="darkly")
    newassetwin.resizable(False, False)
    # Header of Popup
    header = Label(newassetwin, text="Add a new asset to the database", font=('Inter', 12))
    header.pack(padx=10, pady=10)
    # Frame that contains all fields
    assetfields = Frame(newassetwin)
    assetfields.pack(padx=15, fill=BOTH, expand=True)
    # Error text, only shows if a field is empty
    errortext = Label(assetfields, text="Please fill out all fields.", font=('Inter', 9), foreground="red")
    # Asset Name Entry
    nameentry = Frame(assetfields)
    nameentry.pack(pady=8, fill=X)
    # assetname var that holds the asset name
    assetname = StringVar()
    Label(nameentry, text="Asset Name", font=('Inter', 9)).pack(anchor="w", pady=5, expand=True, fill=BOTH)
    Entry(nameentry, textvariable=assetname).pack(fill=X, expand=True)
    # Author Name Entry
    authorentry = Frame(assetfields)
    authorentry.pack(pady=8, fill=X)
    # authorname var that holds the author name
    authorname = StringVar()
    Label(authorentry, text="Author Name", font=('Inter', 9)).pack(anchor="w", pady=5, expand=True, fill=BOTH)
    Entry(authorentry, textvariable=authorname).pack(fill=X, expand=True)
    # Asset Description Entry
    descriptionentry = Frame(assetfields)
    descriptionentry.pack(pady=8, fill=X)
    Label(descriptionentry, text="Asset Description", font=('Inter', 9)).pack(anchor="w", pady=5, expand=True,
                                                                              fill=BOTH)
    descriptiontextbox = Text(descriptionentry, height=5)
    descriptiontextbox.pack(fill=X, expand=True)

    # Asset Paths Entry
    def addpath():
        boxentry_string = pathslistboxentry.get()
        if boxentry_string:
            pathslistbox.insert(pathslistbox.size(), boxentry_string)
            pathslistboxentry.delete(0, "end")

    def removepath():
        selection = pathslistbox.curselection()
        if selection:
            pathslistbox.delete(selection)

    assetpathsentry = Frame(assetfields)
    assetpathsentry.pack(pady=8, fill=X)
    Label(assetpathsentry, text="Asset Paths", font=('Inter', 9)).pack(anchor="w", pady=5, expand=True, fill=BOTH)
    # Acts as group to host list and buttons
    pathslistboxframe = Frame(assetpathsentry)
    pathslistboxframe.pack(fill=X, expand=True)
    # Entry for paths
    pathslistboxentry = Entry(pathslistboxframe)
    pathslistboxentry.pack(fill=X, expand=True, pady=5)
    # Actual List Box
    pathslistbox = Listbox(pathslistboxframe)
    pathslistbox.pack(fill=X, expand=True, side=LEFT)
    # Frame of Buttons
    Frame(pathslistboxframe).pack(fill=Y, side=LEFT)
    # Add buttons
    Button(pathslistboxframe, text="+", command=addpath).pack(pady=5)
    Button(pathslistboxframe, text="-", command=removepath).pack(pady=5)
    # Credit Type Entry
    credittypeentry = Frame(assetfields)
    credittypeentry.pack(pady=8, fill=X)
    # credittype var that holds the credit type
    credittype = StringVar()
    Label(credittypeentry, text="Credit Type", font=('Inter', 9)).pack(anchor="w", pady=5, expand=True, fill=BOTH)
    credittyperadios = Frame(credittypeentry)
    credittyperadios.pack(fill=X, expand=True)
    Radiobutton(credittyperadios, text="None", variable=credittype, value="none").pack(anchor="w", pady=5)
    Radiobutton(credittyperadios, text="Preferred but not Required", variable=credittype, value="optional").pack(
        anchor="w", pady=5)
    Radiobutton(credittyperadios, text="Required", variable=credittype, value="required").pack(anchor="w", pady=5)
    # Frame of Buttons
    buttonframe = Frame(newassetwin)
    buttonframe.pack(anchor="s", pady=10, padx=5)

    # Import file button

    def importfile():
        jsonPath = askopenfilename(parent=newassetwin, defaultextension=".json", filetypes=[("JSON file", ".json")],
                                   title="Select a file")
        if jsonPath:
            shutil.copy(jsonPath, os.path.join(jsonFolder, os.path.basename(jsonPath)))

    Button(buttonframe, text="Import", command=importfile).pack(side=LEFT, padx=5)
    # Search other assets button
    Button(buttonframe, text="Search on GitHub",
           command=lambda: webbrowser.open(
               "https://github.com/TotallyKenzo/KACC/discussions/categories/resources")).pack(side=LEFT, padx=5)
    # Submit button
    Button(buttonframe, text="Submit", command=assetsubmit).pack(side=LEFT, padx=5)

    newassetwin.mainloop()


def getPakList():
    selectedbsp = bsp.BSP(askopenfilename(defaultextension=".bsp",
                                          filetypes=[("BSP map file", ".bsp")],
                                          title="Select a map"
                                          ))
    return selectedbsp.pakfile.namelist()


def getcredittype(jsonassets):
    creditlist = []
    for i in range(len(jsonassets)):
        with open(jsonassets[i], 'r', encoding='UTF-8') as f:
            json_obj = json.load(f)
            credit_type = json_obj['creditType']
            manualcredit = False
            if credit_type != 'none':
                if credit_type == 'optional':
                    manualcredit = askyesno(f'Confirm credit for "{json_obj["assetName"]}"',
                                            f'"{json_obj["assetName"]}" has the credit type set to preferred.\nWould you '
                                            f'like to credit {json_obj["assetAuthor"]}?')
                if manualcredit or credit_type == 'required':
                    creditlist.append(jsonassets[i])
    return creditlist


# def add():
# TODO: Implement add function


def clearConsole():
    """Natively clears the console."""
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    elif os.name == "java":
        os.system("clear")
    return
