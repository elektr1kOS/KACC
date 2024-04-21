'''
GUI version of KACC.
'''

from srctools import bsp
from tkinter.filedialog import askopenfile, asksaveasfile
from ttkbootstrap import *
import json
import os

win = Window('KACC (GUI version)', 'darkly')

jsonFolder = os.path.join(os.getcwd(), 'Assets')
jsonassets = []

def find() -> list:
    f = askopenfile(defaultextension='.bsp', filetypes=[('BSP map file', '.bsp')], title='Pick a file to view')
    if f: # prevent errors when user clicks the cancel button
        with f: # auto-close file when done reading
            pass
        
isJson = lambda f: os.path.splitext(f)[1] == '.json'
        
def start_search():
    print('Searching for JSON files...')
    only_json = filter(isJson, os.listdir(jsonFolder))
    progressbar.config(maximum=len(only_json))
    for index, file in enumerate(only_json):
        print(f'Indexing {file} (file #{index})')
        progressbar.config(value = index + 1)
        
        with open(os.path.join(jsonFolder, file), 'r') as jsfile:
            jsonassets.append(json.load(jsfile))

    print(f'Found and indexed {len(jsonassets)} JSON files.')

progressbar = Progressbar(win, length = 200, style=(STRIPED, INFO))
progressbar.pack(side=BOTTOM, expand=True, fill=X, anchor=S, padx=5, pady=5)

def add():
    #TODO: implement add
    raise NotImplementedError('TODO: implement add()')

button_panel = Frame(win)
button_panel.pack(side=LEFT, fill=Y, expand=True, anchor=W, padx=5, pady=5)
add_asset_button = Button(button_panel, text='Add asset', command = add)
add_asset_button.pack(side=TOP, padx=5, pady=5, expand=True)

find_asset_button = Button(button_panel, text = 'Find asset', command = find)
find_asset_button.pack(side=TOP, expand=True, padx=5, pady=5)

win.mainloop()