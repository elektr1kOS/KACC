"""IDK pylint wants me to add a module docstring"""
import datetime
import json
import os
import shutil
import time
import webbrowser

from tkinter import Listbox
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import askyesno
from PIL import Image
from ttkbootstrap import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.dialogs import *
from srctools import bsp
import datetime

# Global Variables
jsonFolder = os.path.join(os.path.dirname(__file__), "Assets")
jsonassets = []


def kaccinit():
    """Searches asset folder for asset configs, and adds the file path to a list."""
    initprogress = Toplevel(title="Initializing KACC")
    initprogress.resizable(False, False)

    Label(initprogress, text="Searching for JSON files...").pack(pady=10, padx=10)

    jsonprobar = Progressbar(initprogress, style="striped")
    jsonprobar.pack(pady=10, padx=10, fill=X, expand=True)

    # Searches the "Assets" folder for files
    jsonassets.clear()
    jsonlist = os.listdir(jsonFolder)
    for i, file in enumerate(jsonlist):
        jsonprobar.step(100 / len(jsonlist))
        jsonassets.append(os.path.join(jsonFolder, indexThrJson(jsonlist, currentiter=i)))
    # Sleep for order
    time.sleep(.1)
    if len(jsonassets) == 0:
        Messagebox.show_error(
            message="No json files found in the 'Assets' folder.\nFor this program to function, you need to "
                    "define each asset in it's own json file.\nA simple way of fixing this is by creating an "
                    "asset either using the add asset function, or writing a json file yourself\nPlease refer "
                    "to the documentation for more information.",
            title="No json files found")
    else:
        print(f"Found and indexed {len(jsonassets)} json files.")
    initprogress.destroy()
    return jsonassets


def deleteJsonAsset(queueditem, guifunction):
    os.remove(queueditem)
    time.sleep(0.02)
    guifunction()
    return


def kaccfind():
    """Searches for assets in a map."""
    if not jsonassets:
        return FileNotFoundError("No json files found in the 'Assets' folder.")
    searchingwin = Toplevel(title="Searching for assets")
    searchingwin.resizable(False, False)

    infolabel = Label(searchingwin, text="Waiting on map to be selected...", font=("Inter", 20))
    infolabel.pack(pady=10, padx=10)

    console = Listbox(searchingwin)
    console.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def consolep(text):
        console.insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] - {text}")
        return

    searchingwin.mainloop()

    # Gets the pack file of the map. In ZipFile object.
    consolep("Waiting for map to be selected...")
    selectedmap = askopenfilename(defaultextension=".bsp", filetypes=[("BSP map file", ".bsp")], title="Select a map")
    consolep(f"Selected map: {selectedmap}")
    paklist = bsp.BSP(selectedmap).pakfile.namelist()
    consolep(f"Found {len(paklist)} files in map.")

    # See search function for more info.
    foundassets = []
    infolabel.config(text=f"Searching {selectedmap} and comparing to assets...")
    consolep(f"Searching {selectedmap} and comparing to assets...")
    currentasset = Label(infolabel, text=f"Comparing ", font=("Inter", 10))
    for index, asset in enumerate(jsonassets):
        currentasset.config(text=f"Comparing {os.path.basename(asset)}")
        consolep(f"Comparing {os.path.basename(asset)}")
        # Searches a json file for asset paths.
        with open(asset, 'r', encoding="UTF-8") as f:
            json_obj = json.load(f)
            asset_paths = json_obj['assetPaths']
            # Loops through asset paths in json file.
            for path in asset_paths:
                # Checks if json asset path is in map pak file and if it's already been found.
                if path in paklist and asset not in foundassets:
                    time.sleep(.1)
                    print(f"Found {json_obj['assetName']}")
                    foundassets.append(asset)
    # Determines the credit type of the assets found.
    creditlist = getcredittype(foundassets)
    generateCredits(creditlist)


def ask_multiple_choice_question(prompt, options_dict, buttons, buttoncommands, wintitle):
    multiprompt = Toplevel()
    multiprompt.title(wintitle)
    multiprompt.resizable(False, False)
    if prompt:
        Label(multiprompt, text=prompt, font=('Inter', 15)).pack(padx=20, pady=10)
    v = IntVar()
    radiosscroll = ScrolledFrame(multiprompt)
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


def guijsonlist(guiwindow, guifunction):
    jsonassetslist = ScrolledFrame(guiwindow)
    jsonassetslist.pack(fill=X, pady=5, padx=5)
    kaccinit()
    for i in jsonassets:
        createAssetGUIItem(i, jsonassetslist, guifunction)
    return


def createAssetGUIItem(currentitem, guiframe, guifunction):
    with open(currentitem, 'r', encoding='UTF-8') as f:
        json_obj = json.load(f)
        itemframe = Frame(guiframe, style="secondary")
        itemframe.pack(fill=X)
        itemframe.bind("<Enter>", lambda event: itemframe.config(bootstyle="primary"))
        itemframe.bind("<Leave>", lambda event: itemframe.config(bootstyle="secondary"))
        for child in itemframe.winfo_children():
            child.bind("<Enter>", lambda event: itemframe.config(bootstyle="primary"))
            child.bind("<Leave>", lambda event: itemframe.config(bootstyle="secondary"))
        Label(itemframe, text=json_obj['assetName'], font=('Inter', 12), justify=LEFT).pack(anchor="w", pady=5,
                                                                                            padx=5, side=LEFT)
        editicon = Image.open(os.path.join(os.path.dirname(__file__), "res", "googleicon_edit.png"))
        editimg = ImageTk.PhotoImage(editicon)
        Button(itemframe, text=" ", image=editimg, style="dark",
               command=lambda: manageAsset(assetfile=os.path.basename(currentitem))).pack(side=RIGHT, padx=5)
        deleteicon = Image.open(os.path.join(os.path.dirname(__file__), "res", "googleicon_delete.png"))
        deleteimg = ImageTk.PhotoImage(deleteicon)
        Button(itemframe, text=" ", image=deleteimg, style="dark",
               command=lambda: deleteJsonAsset(currentitem, guifunction)).pack(side=RIGHT, padx=5)
    return


def indexThrJson(jsonlist, currentiter):
    """Checks if given file is json, and appends to jsonassets."""
    if '.json' in jsonlist[currentiter]:
        # If the file is a json file, add it to a file.
        return jsonlist[currentiter]
    return


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
    with open(asksaveasfile(defaultextension=".txt",
                            filetypes=[('Text File', '.txt')]).name, 'a', encoding='UTF-8') as f:
        for author, assets in authorassets.items():
            f.write(creditformat.format(assetname=", ".join(assets), authorname=author).join("\n"))
        if askyesno("Open file?", "Done! The credits document has been generated. \nWould you like to open it in the "
                                  "default text editor?"):
            os.startfile(f.name)
    return


def manageAsset(assetfile, refreshlist):
    newassetwin = Toplevel(title="Add a new asset")
    newassetwin.geometry("400x500")
    newassetwin.resizable(False, True)

    # Placeholder vars
    pl_assetname = ""
    pl_authorname = ""
    pl_description = ""
    pl_paths = []
    pl_credittype = ""

    if assetfile is not None:
        with open(os.path.join(jsonFolder, assetfile), 'r', encoding='UTF-8') as f:
            json_obj = json.load(f)
            pl_assetname = json_obj['assetName']
            pl_authorname = json_obj['assetAuthor']
            pl_description = json_obj['assetDesc']
            pl_paths = json_obj['assetPaths']
            pl_credittype = json_obj['creditType']

    # Header of Popup
    header = Label(newassetwin, text="Add a new asset to the database", font=('Inter', 15))
    header.pack(padx=10, pady=10)
    # Frame that contains all fields
    assetfields = ScrolledFrame(newassetwin)
    assetfields.pack(padx=15, fill=BOTH, expand=True)
    # Error text, only shows if a field is empty
    errortext = Label(assetfields, text="Please fill out all fields.", font=('Inter', 12))
    # Asset Name Entry
    nameentry = Frame(assetfields)
    nameentry.pack(pady=8, fill=X)
    # assetname var that holds the asset name
    assetnamevar = StringVar()
    Label(nameentry, text="Asset Name", font=('Inter', 12), justify=LEFT).pack(anchor="w", pady=5)
    nameentrybox = Entry(nameentry, textvariable=assetnamevar)
    nameentrybox.pack(fill=X, expand=True)
    if pl_assetname:
        nameentrybox.insert(0, pl_assetname)
        assetnamevar.set(pl_assetname)
    # Author Name Entry
    authorentry = Frame(assetfields)
    authorentry.pack(pady=8, fill=X)
    # authorname var that holds the author name
    authorname = StringVar()
    Label(authorentry, text="Author Name", font=('Inter', 12), justify=LEFT).pack(anchor="w", pady=5)
    authorentrybox = Entry(authorentry, textvariable=authorname)
    authorentrybox.pack(fill=X, expand=True)
    if pl_authorname:
        authorentrybox.insert(0, pl_authorname)
        authorname.set(pl_authorname)
    # Asset Description Entry
    descriptionentry = Frame(assetfields)
    descriptionentry.pack(pady=8, fill=X)
    Label(descriptionentry, text="Asset Description", font=('Inter', 12), justify=LEFT).pack(anchor="w", pady=5)
    descriptiontextbox = Text(descriptionentry, height=5)
    descriptiontextbox.pack(fill=X, expand=True)
    if pl_description:
        descriptiontextbox.insert("1.0", pl_description)

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
    Label(assetpathsentry, text="Asset Paths", font=('Inter', 12), justify=LEFT).pack(anchor="w", pady=5)
    # Acts as group to host list and buttons
    pathslistboxframe = Frame(assetpathsentry)
    pathslistboxframe.pack(fill=X, expand=True)
    # Entry for paths
    pathslistboxentry = Entry(pathslistboxframe)
    pathslistboxentry.pack(fill=X, expand=True, pady=5)
    # Actual List Box
    pathslistbox = Listbox(pathslistboxframe)
    pathslistbox.pack(fill=X, expand=True, side=LEFT)
    if pl_paths:
        for i in pl_paths:
            pathslistbox.insert(pathslistbox.size(), i)
    # Frame of Buttons
    pathsbuttonsframe = Frame(pathslistboxframe)
    pathsbuttonsframe.pack(fill=Y, side=LEFT)
    # Add buttons
    Button(pathsbuttonsframe, text="+", command=addpath).pack(pady=5)
    Button(pathsbuttonsframe, text="-", command=removepath).pack(pady=5)
    # Credit Type Entry
    credittypeentry = Frame(assetfields)
    credittypeentry.pack(pady=8, fill=X)
    # credittype var that holds the credit type
    credittype = StringVar()
    Label(credittypeentry, text="Credit Type", font=('Inter', 12), justify=LEFT).pack(anchor="w", pady=5,
                                                                                      expand=True, fill=BOTH)
    credittyperadios = Frame(credittypeentry)
    credittyperadios.pack(fill=X, expand=True)
    creditradionone = Radiobutton(credittyperadios, text="None", variable=credittype, value="none")
    creditradionone.pack(anchor="w", pady=5, padx=5)
    if pl_credittype == "none":
        creditradionone.invoke()
    creditradioopt = Radiobutton(credittyperadios, text="Preferred but not Required", variable=credittype,
                                 value="optional")
    creditradioopt.pack(anchor="w", pady=5, padx=5)
    if pl_credittype == "optional":
        creditradioopt.invoke()
    creditradioreq = Radiobutton(credittyperadios, text="Required", variable=credittype, value="required")
    creditradioreq.pack(anchor="w", pady=5, padx=5)
    if pl_credittype == "required":
        creditradioreq.invoke()
    if pl_credittype:
        credittype.set(pl_credittype)
    # Frame of Buttons
    buttonframe = Frame(newassetwin)
    buttonframe.pack(anchor="s", pady=10, padx=5)

    # Import file button

    def importfile():
        jsonPath = askopenfilename(parent=newassetwin, defaultextension=".json", filetypes=[("JSON file", ".json")],
                                   title="Select a file")
        if jsonPath:
            shutil.copy(jsonPath, os.path.join(jsonFolder, os.path.basename(jsonPath)))
            newassetwin.destroy()
            refreshlist()

    Button(buttonframe, text="Import", command=importfile).pack(side=LEFT, padx=5)
    # Search other assets button
    Button(buttonframe, text="Search on GitHub",
           command=lambda: webbrowser.open(
               "https://github.com/TotallyKenzo/KACC/discussions/categories/resources")).pack(side=LEFT, padx=5)

    # Submit button
    def assetsubmit():
        print(assetnamevar.get())
        print(authorname.get())
        print(pathslistbox.size())
        print(credittype.get())
        if assetnamevar.get() and authorname.get() and pathslistbox.size() != 0 and credittype.get():
            newasset = {
                "assetName": assetnamevar.get(),
                "assetAuthor": authorname.get(),
                "assetDesc": descriptiontextbox.get("1.0", "end-1c"),
                "assetPaths": list(pathslistbox.get(0, "end")),
                "creditType": credittype.get()
            }
            if assetfile is None:
                outputfromdiag = Querybox.get_string(prompt="Please enter a name for the json file.",
                                                     title="Name your file", parent=newassetwin)
                if outputfromdiag.endswith(".json"):
                    filename = outputfromdiag
                else:
                    filename = f"{outputfromdiag}.json"
            else:
                filename = assetfile
            with open(os.path.join(jsonFolder, filename), 'w', encoding='UTF-8') as newData:
                json.dump(newasset, newData, indent=4)
            newassetwin.destroy()
            refreshlist()
        else:
            errortext.pack()
            pass

    Button(buttonframe, text="Submit", command=assetsubmit).pack(side=LEFT, padx=5)

    newassetwin.mainloop()


def getcredittype(mapassets):
    creditlist = []
    for i in range(len(mapassets)):
        with open(mapassets[i], 'r', encoding='UTF-8') as f:
            json_obj = json.load(f)
            credit_type = json_obj['creditType']
            manualcredit = False
            if credit_type != 'none':
                if credit_type == 'optional':
                    manualcredit = Messagebox.yesno(title=f'Confirm credit for "{json_obj["assetName"]}"',
                                                    message=f'"{json_obj["assetName"]}" has the credit type set to '
                                                            f'preferred.\nWould you'
                                                            f'like to credit {json_obj["assetAuthor"]}?')
                if manualcredit or credit_type == 'required':
                    creditlist.append(mapassets[i])
    return creditlist


def clearConsole():
    """Natively clears the console."""
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    elif os.name == "java":
        os.system("clear")
    return
