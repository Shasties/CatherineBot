from pathlib import Path,PureWindowsPath
from inputs import get_gamepad
#from catherineParser import init
#from inputRecorder import recordInputs
from tkinter import *

import time
import json
import tkinter
import os
import json
import random

toggle_play = ["BTN_TR"]
toggle_record = ["BTN_TL"]
config = {}
stages = ['Underground','Torture','Quadrangle','Clock Tower','Spiral Corridor','Cathedral']

def getSelected(buttons):
    selected_buttons = []
    for opening in buttons:
        if (buttons[opening]['Value'].get()) == 1:
            selected_buttons.append(opening)
    print(random.choice(selected_buttons))

def get_openings():
    list_of_openings = {}
    for stage in stages:
        list_of_openings[stage] = []
    for filename in os.listdir(os.getcwd()+'/files/commands'):
        myfile = os.getcwd()+'/files/commands/'+filename
        if ".json" in myfile:
            with open(myfile) as f:
                data = json.load(f)
                list_of_openings[data['Stage']].append(data['Name'])
    return list_of_openings

def launch_gui():
    root = tkinter.Tk()
    root.title("Catherine dummy alpha")

    checkbox_frame = Frame(root).grid(row=0,column=0)
    openings_buttons = {}
    # Create checkboxes based on files
    list_of_openings = get_openings()
    column_index=0
    for stage in list_of_openings.keys():
        # Print name of Stage
        Label( root, text = stage).grid(row=column_index,column=0)
        # List openings
        for i in range(len(list_of_openings[stage])):
            opening_name = list_of_openings[stage][i]
            openings_buttons[opening_name] = {}
            if i%5 == 0: 
                column_index = column_index+1
            openings_buttons[opening_name]['Value'] = tkinter.IntVar()
            openings_buttons[opening_name]['Button'] = Checkbutton(checkbox_frame,text=list_of_openings[stage][i],variable=openings_buttons[opening_name]['Value'])
            openings_buttons[opening_name]['Button'].grid(row=column_index,column=i%5)
        column_index = column_index + 1

    # Allow User to set toggle button
    Button(checkbox_frame, text ="Configure Toggle", command= lambda: getSelected(openings_buttons)).grid(row=column_index,column=0)

    root.mainloop()

def main():
	while 1:
		events = get_gamepad()
		for event in events:
			if event.code in toggle_play and event.state == 0:
				command_file = Path("./files/commands/Temp.json")
				command_path = PureWindowsPath(command_file)
				init(command_path)
			elif event.code in toggle_record and event.state == 0:
				print("recording")
				recordedInputs = recordInputs()
				print("finished recording")
				for item in recordedInputs:
					# Mirror inputs for P2
					if item['State'] == 'Left':
						item['State'] = "Right"
					elif item['State'] == 'Right':
						item['State'] = "Left"
				config['Style'] = "Recorded"
				config['Main'] = recordedInputs
				output_file = Path("./files/commands/"+config['Name']+".json")
				print("Writing")
				with open(output_file,'w') as f:
					json.dump(config,f,sort_keys=True, indent=4)


if __name__ == "__main__":
	launch_gui()
