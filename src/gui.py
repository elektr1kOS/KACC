'''
GUI version of KACC.
'''

from srctools import bsp
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import askyesno
from ttkbootstrap import *
import json
import os

win = Window('KACC (GUI version)', 'darkly')

jsonFolder = os.path.join(os.getcwd(), 'Assets')
jsonassets = []
creditlist = []

def find():
    '''
    Search for assets in map.
    '''
    f = askopenfilename(defaultextension='.bsp', filetypes=[('BSP map file', '.bsp')])
    if f:
        mapf = bsp.BSP(f)
        paklist = mapf.pakfile.namelist()
        foundassets = search(paklist)
        print('Generating credits...')
        
        progressbar.config(maximum=len(foundassets))
        for index, item in foundassets:
            progressbar.config(value=index + 1)
            
            with open(item, 'r', encoding='UTF-8') as f:
                json_obj = json.load(f)
                credit_type = json_obj['creditType']
                manualcredit = False
                if credit_type != 'none':
                    if credit_type == 'optional':
                        manualcredit = askyesno(f'Looks like {json_obj["assetName"]} has the credit type set to preferred.\nWould you like to credit {json_obj["assetAuthor"]}?')
                    if manualcredit or json_obj['creditType'] == 'required':
                        creditlist.append(item)
                        
        print(creditlist)
        
isJson = lambda f: os.path.splitext(f)[1] == '.json'

progressbar = Progressbar(win, length = 200, style=(STRIPED, INFO))
progressbar.pack(side=BOTTOM, expand=True, fill=X, anchor=S, padx=5, pady=5)

def add():
    #TODO: implement add
    raise NotImplementedError('TODO: implement add()')
    
def search(paklist: list[str]):
    '''
    Search for assets in asset configs and see if they're in the map.
    '''
    foundassets = []
    progressbar.config(maximum=len(jsonassets))
    for index, item in enumerate(jsonassets):
        progressbar.config(value=index + 1)
        with open(jsonassets[index], 'r', encoding='UTF-8') as jsfile:
            json_obj = json.load(jsfile)
            asset_paths = json_obj['assetPaths']
            
            for path in asset_paths:
                if path in paklist and item not in foundassets:
                    foundassets.append(item)
    return foundassets

button_panel = Frame(win)
button_panel.pack(side=LEFT, fill=Y, expand=True, anchor=W, padx=5, pady=5)
add_asset_button = Button(button_panel, text='Add asset', command = add)
add_asset_button.pack(side=TOP, padx=5, pady=5, expand=True)

find_asset_button = Button(button_panel, text = 'Find asset', command = find)
find_asset_button.pack(side=TOP, expand=True, padx=5, pady=5)

win.mainloop()