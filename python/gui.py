# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 00:49:27 2021

@author: Tarandeep
"""

import PySimpleGUI as sg
import json

#create layout

def gui_method(): 
    
    bold_method = ('Arial', 12, 'bold')
    
    layout_gui = [
        [
            sg.Text("This form requires files listed below to calculate model that returns the lowest distance.", font=bold_method)
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
            sg.Text("What range of weeks would you like to look at?", font=bold_method)
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
            sg.Text("Select store order date to analyze:", font=bold_method)
        ],
        [
            sg.Text("Month", size=(10,1)),
            sg.InputText(size=(5,1), key="salesMonth"),
            sg.Text("Day", size=(10,1)),
            sg.InputText(size=(5,1), key="salesDay"),
            sg.Text("Year", size=(10,1)),
            sg.InputText(size=(5,1), key="salesYear")
        ],
        [
            sg.Checkbox("Would you like to compute Space Allocation Model? If not, previous results will be used.", default=True, key="spaceAllocate"),
        ],
        [
            sg.Text("Space Allocation Parameters:", font=bold_method)
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
            sg.Text("Aisle Declaration (ex. 1st row, 22nd row, 50th row) ", font=bold_method)
        ],
        [
            sg.Text("Top Aisle", size=(10,1)),
            sg.InputText(size=(5,1), key="aisleTop"),
            sg.Text("Cross Aisle", size=(10,1)),
            sg.InputText(size=(5,1), key="aisleMiddle"),
            sg.Text("Bottom Aisle", size=(10,1)),
            sg.InputText(size=(5,1), key="aisleBottom")
        ],
        [
            sg.Text("Determine SKU List to Calculate", font=bold_method)
        ],
        [
            sg.Checkbox("Random", default=True, key="random"),
            sg.Checkbox("COI", default=True, key="coi"),
            sg.Checkbox("Weight", default=True, key="weight"),
            sg.Checkbox("ABC (across)", default=True, key="across"),
            sg.Checkbox("ABC (vertical)", default=True, key="vertical")
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
