from pathlib import Path,PureWindowsPath
from inputs import get_gamepad
from catherineParser import init
from inputRecorder import recordInputs
from tkinter import *

import time
import json
import tkinter
import os

toggle_play = ["BTN_TR"]
toggle_record = ["BTN_TL"]
config = {}
stages = ['Underground','Torture','Quadrangle','Clock Tower','Spiral Corridor','Cathedral']

def get_openings():
    list_of_openings = []
    for filename in os.listdir(os.getcwd()+'\\files\\commands'):
        if ".json" in filename:
            list_of_openings.append(filename)
    return list_of_openings

def launch_gui():
    root = tkinter.Tk()
    root.title("Catherine dummy alpha")

    checkbox_frame = Frame(root).grid(row=0,column=0)
    # Create checkboxes based on files
    list_of_openings = get_openings()
    column_index=0
    for i in range(len(list_of_openings)):
        if i%5 == 0: 
            column_index = column_index+1
        Checkbutton(checkbox_frame,text=list_of_openings[i]).grid(row=column_index,column=i%5)
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
