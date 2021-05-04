# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 00:49:27 2021

@author: Tarandeep
"""

import PySimpleGUI as sg
import json

# create layout


def gui_method():

    bold_method = ('Arial', 12, 'bold')

    layout_gui = [
        [
            sg.Text(
                "This form requires files listed below to calculate model that returns the lowest distance.", font=bold_method)
        ],
        [
            sg.Text("File locations left blank will use default values.")
        ],
        [
            sg.Text("Select Excel Layout", size=(30, 1)),
            sg.In(size=(25, 1), enable_events=True, key="layout"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Select Picklist File", size=(30, 1)),
            sg.In(size=(25, 1), enable_events=True, key="specs"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Select Orders File", size=(30, 1)),
            sg.In(size=(25, 1), enable_events=True, key="orders"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Export File Location", size=(30, 1)),
            sg.In(size=(25, 1), enable_events=True, key="exportLocation"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Location of first SKU Layout", size=(30, 1)),
            sg.In(size=(15, 1), enable_events=True, key="sku1"),
            sg.FolderBrowse(),
            sg.Text("Name of Assignment", size=(20, 1)),
            sg.InputText(size=(15, 1), key="sku1Text")
        ],
        [
            sg.Text("Location of second SKU Layout", size=(30, 1)),
            sg.In(size=(15, 1), enable_events=True, key="sku2"),
            sg.FolderBrowse(),
            sg.Text("Name of Assignment", size=(20, 1)),
            sg.InputText(size=(15, 1), key="sku2Text")
        ],
        [
            sg.Text("Location of third SKU Layout", size=(30, 1)),
            sg.In(size=(15, 1), enable_events=True, key="sku3"),
            sg.FolderBrowse(),
            sg.Text("Name of Assignment", size=(20, 1)),
            sg.InputText(size=(15, 1), key="sku3Text")
        ],        
        [
            sg.Text("Location of fourth SKU Layout", size=(30, 1)),
            sg.In(size=(15, 1), enable_events=True, key="sku4"),
            sg.FolderBrowse(),
            sg.Text("Name of Assignment", size=(20, 1)),
            sg.InputText(size=(15, 1), key="sku4Text")
        ],
        [
            sg.Text("Location of fifth SKU Layout", size=(30, 1)),
            sg.In(size=(15, 1), enable_events=True, key="sku5"),
            sg.FolderBrowse(),
            sg.Text("Name of Assignment", size=(20, 1)),
            sg.InputText(size=(15, 1), key="sku5Text")
        ],
        [
            sg.Text(
                "Aisle Declaration (ex. 1st row, 22nd row, 50th row) ", font=bold_method)
        ],
        [
            sg.Text("Top Aisle", size=(10, 1)),
            sg.InputText(size=(5, 1), key="aisleTop"),
            sg.Text("Cross Aisle", size=(10, 1)),
            sg.InputText(size=(5, 1), key="aisleMiddle"),
            sg.Text("Bottom Aisle", size=(10, 1)),
            sg.InputText(size=(5, 1), key="aisleBottom")
        ],
        [
            sg.Text("Determine SKU List to Calculate", font=bold_method)
        ],
        [
            sg.Checkbox("SKU1", default=True, key="random"),
            sg.Checkbox("SKU2", default=True, key="coi"),
            sg.Checkbox("SKU3", default=True, key="weight"),
            sg.Checkbox("SKU4", default=False, key="across"),
            sg.Checkbox("SKU5", default=False, key="vertical")
        ],
        [
            sg.Submit(), sg.Cancel()
        ]
    ]

    window = sg.Window("Metro SKU Assignment Tool").Layout(layout_gui)
    while True:
        event, values = window.Read()  # Run the window until an "event" is triggered
        if event == "Submit":
            window.close()
            return values
        elif event is None or event == "Cancel":
            window.close()
            return None
