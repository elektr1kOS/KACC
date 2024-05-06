"""
GUI version of KACC.
"""

from kacc import *

def refreshguilist():
    for child in assetslists.winfo_children():
        child.destroy()
    guijsonlist(assetslists, refreshguilist)
    return


mainguiwin = Window(title="Kenzo's Awesome Credits Checker", themename="darkly")
mainguiwin.resizable(False, False)

headerframe = Frame(mainguiwin)
headerframe.pack(fill=X, pady=10, padx=10)

Label(headerframe, text="Kenzo's Awesome Credits Checker", font=("Inter", 20)).pack()

existingassets = Frame(mainguiwin)
existingassets.pack(fill=X, pady=10, padx=10)

addbutton = Button(existingassets, text="Add Asset", command=lambda: manageAsset(assetfile=None,
                                                                                 refreshlist=refreshguilist))
addbutton.pack(padx=10, pady=10, fill=X, expand=True)

assetslists = Frame(existingassets)
assetslists.pack(fill=X)

guijsonlist(assetslists, refreshguilist)

Separator(mainguiwin).pack(fill=X, padx=5, pady=5)

Button(mainguiwin, text="Search a map file", command=lambda: kaccfind()).pack(fill=X, padx=10, pady=10)

mainguiwin.mainloop()