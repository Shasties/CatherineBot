from pathlib import Path,PureWindowsPath
from inputs import get_gamepad
from catherineParser import init
from inputRecorder import recordInputs

import time
import json

toggle_play = ["BTN_TR"]
toggle_record = ["BTN_TL"]
config = {
	"Stage": "Quadrangle",
	"Name": "Temp"
}

def launch_gui():
	pass
	# TODO
	# List files under ./files/commands
		# Allow User to select Commands to Load or Record their own 
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
	main()
