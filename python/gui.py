# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 00:49:27 2021

@author: Tarandeep
"""

import PySimpleGUI as sg
import json

#create layout

def gui_method(): 
    
    layout_gui = [
        [
            sg.Text("This form requires files listed below to calculate model that returns the lowest distance.")
        ],
        [
            sg.Text("File locations left blank will use default values.")
        ],
        [
            sg.Text("Select Excel Layout", size=(30,1)),
            sg.In(size=(25, 1), enable_events=True, key="layout"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Select Specifications File", size=(30,1)),
            sg.In(size=(25, 1), enable_events=True, key="specs"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Select Sales Data File", size=(30,1)),
            sg.In(size=(25, 1), enable_events=True, key="salesData"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Select Store Orders", size=(30,1)),
            sg.In(size=(25, 1), enable_events=True, key="storeOrder"),
            sg.FileBrowse(),
        ], 
        [
            sg.Text("Select Order Lines Location", size=(30,1)),
            sg.In(size=(25, 1), enable_events=True, key="orderLinesLocation"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Export File Location", size=(30,1)),
            sg.In(size=(25, 1), enable_events=True, key="exportLocation"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("What range of weeks would you like to look at?")
        ],
        [
            sg.Text("Starting Week", size=(30,1)),
            sg.InputText(size=(5,1), key="startWeek")
        ],
        [
            sg.Text("Ending Week", size=(30,1)),
            sg.InputText(size=(5,1), key="endWeek")
        ],
        [
            sg.Text("Space Allocation Parameters:")
        ],
        [
            sg.Text("Max Spaces per SKU", size=(30,1)),
            sg.InputText(size=(5,1), key="maxSpaces")
        ],
        [
            sg.Text("Total Spaces in Layout", size=(30,1)),
            sg.InputText(size=(5,1), key="totalSpaces")
        ],
        [
            sg.Text("Total number of SKUs", size=(30,1)),
            sg.InputText(size=(5,1), key="totalSKU")
        ],
        [
            sg.Text("Determine SKU List to Calculate")
        ],
        [
            sg.Checkbox("Random", default=False, key="random"),
            sg.Checkbox("COI", default=False, key="coi"),
            sg.Checkbox("Weight", default=False, key="weight"),
            sg.Checkbox("ABC (across)", default=False, key="across"),
            sg.Checkbox("ABC (vertical)", default=False, key="vertical")
        ],
        [
            sg.Submit(), sg.Cancel()
        ]
        
        ]
    
    
    window = sg.Window("Metro SKU Assignment Tool").Layout(layout_gui)
    while True:
        event, values = window.Read() # Run the window until an "event" is triggered
        if event == "Submit":
            window.close() 
            return values
        elif event is None or event == "Cancel":
            window.close() 
            return None   
