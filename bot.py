from pathlib import Path, PureWindowsPath
from inputs import get_gamepad
from catherineParser import init
from inputRecorder import recordInputs
from tkinter import *

import tkinter.messagebox
import time
import json
import tkinter
import os
import json
import random
import keyboard

# Initialize variables


objects = {'Name': "Custom",'Stage':"Underground"}
config = {'Player': '1', 'Controller': 'Xbox', 'Name': 'Custom', 'Stage': '', 
            "Unready": "BTN_SELECT", "Play": "BTN_TR", "Record": "BTN_TL"}
stages = ['Underground', 'Torture', 'Quadrangle',
          'Clock Tower', 'Spiral Corridor', 'Cathedral']
openings_buttons = {}

# Return Names of Selected openings
def getSelected():
    selected_buttons = []
    for opening in openings_buttons:
        if (openings_buttons[opening]['Value'].get()) == 1:
            selected_buttons.append(opening)
    return random.choice(selected_buttons)

# Grab all openings in json files
def getOpenings():
    list_of_openings = {}
    # Every stage has a number of openings
    for stage in stages:
        list_of_openings[stage] = []
        # Get openings from json files
    for filename in os.listdir(os.getcwd()+'\\files\\commands'):
        myfile = os.getcwd()+'\\files\\commands\\'+filename
        if ".json" in myfile:
            with open(myfile) as f:
                data = json.load(f)
                list_of_openings[data['Stage']].append(data['Name'])
    return list_of_openings

# Set toggle button for playbacks
def setPlaybackToggle():
    try:
        events = get_gamepad()
    except:
        print("No gamepad detected; Using keyboard")
        config['Controller'] = 'Keyboard'
    set_toggle = False
    while not set_toggle:
        if config['Controller'] == 'Xbox':
            events = get_gamepad()
            for event in events:
                if event.code != "SYN_REPORT":
                    config['Play'] = event.code
                    set_toggle = True
        else:
            event = keyboard.read_key()
            config['Play'] = event
            set_toggle = True
    print(config['Play'])

# Set toggle button for recording
def setRecordingToggle():
    try:
        events = get_gamepad()
    except:
        print("No gamepad detected; Using keyboard")
        config['Controller'] = 'Keyboard'
    set_toggle = False
    while not set_toggle:
        if config['Controller'] == 'Xbox':
            events = get_gamepad()
            for event in events:
                if event.code != "SYN_REPORT":
                    config['Record'] = event.code
                    set_toggle = True
        else:
            event = keyboard.read_key()
            config['Record'] = event
            set_toggle = True
    print(config['Record'])

# Set toggle button for unreadying
def setUnreadyToggle():
    try:
        events = get_gamepad()
    except:
        print("No gamepad detected; Using keyboard")
        config['Controller'] = 'Keyboard'
    set_toggle = False
    while not set_toggle:
        if config['Controller'] == 'Xbox':
            events = get_gamepad()
            for event in events:
                if event.code != "SYN_REPORT":
                    config['Unready'] = event.code
                    set_toggle = True
        else:
            event = keyboard.read_key()
            config['Unready'] = event
            set_toggle = True
    print(config['Unready'])

# Start GUI
def launch_gui():
    root = tkinter.Tk()
    root.title("Catherine dummy alpha")

    checkbox_frame = Frame(root).grid(row=0, column=0)
    # Create checkboxes based on files
    list_of_openings = getOpenings()
    column_index = 0
    for stage in list_of_openings.keys():
        # Print name of Stage
        Label(root, text=stage,font='Helvetica 14 bold').grid(row=column_index, column=0)
        # List openings
        for i in range(len(list_of_openings[stage])):
            opening_name = list_of_openings[stage][i]
            openings_buttons[opening_name] = {}
            if i % 5 == 0:
                column_index = column_index+1
            openings_buttons[opening_name]['Value'] = tkinter.IntVar()
            openings_buttons[opening_name]['Button'] = Checkbutton(
                checkbox_frame, text=list_of_openings[stage][i], variable=openings_buttons[opening_name]['Value'])
            openings_buttons[opening_name]['Button'].grid(
                row=column_index, column=i % 5)
        column_index = column_index + 1

    # Allow User to set toggle buttons
    Button(checkbox_frame, text="Configure Playback Toggle",
           command=setPlaybackToggle).grid(row=column_index, column=0)
    Button(checkbox_frame, text="Configure Recording Toggle",
           command=setRecordingToggle).grid(row=column_index, column=1)
    Button(checkbox_frame, text="Configure Unready Toggle",
           command=setUnreadyToggle).grid(row=column_index, column=2)

    # Let User customize for recording
    L1 = Label(checkbox_frame, text="Recording Stage: ")
    L1.grid(row=column_index+1,column=0)
    objects['Stage'] = StringVar()
    objects['Stage'].set('Underground')
    Entry(checkbox_frame,bd=5,textvariable=objects['Stage']).grid(row=column_index+1,column=1)

    L2 = Label(checkbox_frame, text="Recording Name: ")
    L2.grid(row=column_index+2,column=0)
    objects['Name'] = StringVar()
    objects['Name'].set('Custom')
    E2 = Entry(checkbox_frame,bd=5,textvariable=objects['Name'])
    E2.grid(row=column_index+2,column=1)

    # Start tracking user input
    Button(checkbox_frame, text="Ready", command=startListening).grid(
        row=column_index+3, column=1)

    root.mainloop()

# Playing an Opening when Toggled
def playback():
    # Get a random opening
    random_opening_name = getSelected()
    print(random_opening_name)
    # Retrieve the file it came from and find commands
    for filename in os.listdir(os.getcwd()+'\\files\\commands'):
        myfile = os.getcwd()+'\\files\\commands\\'+filename
        if ".json" in myfile:
            with open(myfile) as f:
                data = json.load(f)
                if data['Name'] == random_opening_name:
                    #command_file = Path("./files/commands/Temp.json")
                    #command_path = PureWindowsPath(command_file)
                    command_path = PureWindowsPath(myfile)
                    init(command_path)

# Recording an Opening when Toggled
def record():
    print("recording")
    recordedInputs = recordInputs(config)
    print("finished recording")
    for item in recordedInputs:
        # Mirror inputs for P2
        if item['State'] == 'Left':
            item['State'] = "Right"
        elif item['State'] == 'Right':
            item['State'] = "Left"
    config['Style'] = "Recorded"
    config['Main'] = recordedInputs
    config['Stage'] = objects['Stage'].get()
    config['Name'] = objects['Name'].get()
    output_file = Path("./files/commands/"+config['Name']+".json")
    print("Writing")
    with open(output_file, 'w') as f:
        json.dump(config, f, sort_keys=True, indent=4)

# Start listening for user input
def startListening(listening=True):
    tkinter.messagebox.showinfo('Config','Play Toggle: '+config['Play']+"\nRecord Toggle: "+config['Record']+"\nUnready Toggle: "+config['Unready'])
    while listening:
        if config['Controller'] == 'Xbox':
            events = get_gamepad()
            for event in events:
                if event.code == config['Play'] and event.state == 0:
                    playback()
                elif event.code == config['Record'] and event.state == 0:
                    record()
                elif event.code == config['Unready'] and event.state == 0:
                    listening = False
        if config['Controller'] == 'Keyboard':
            event = keyboard.read_key()
            if event == config['Play']:
                playback()
            elif event == config['Record']:
                record()
            elif event == config['Unready']:
                listening = False

if __name__ == "__main__":
    launch_gui()
