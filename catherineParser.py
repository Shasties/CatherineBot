import json
import time
from keySender import PressKey,ReleaseKey,dk
config = {
	"Up": "W",
	"Down": "S",
	"Left": "A",
	"Right": "D",
	"Grab": "LBRACKET",
	"Drop": "RBRACKET"
}

### Commands
# Move
def Move(direction):
	PressKey(dk[config[direction]])
	time.sleep(.2) # Replace with a better condition
	ReleaseKey(dk[config[direction]])

# Push/Pull
def Action(direction,pull=None):
	# If pulling - ensure you are grabbing the right block
	if pull:
		PressKey(dk[config[pull]])
		ReleaseKey(dk[config[pull]])
		PressKey(dk[config["Grab"]])
		PressKey(dk[config[direction]])
	else:
		PressKey(dk[config[direction]])
		PressKey(dk[config["Grab"]])
	time.sleep(.2)
	ReleaseKey(dk[config[direction]])
	ReleaseKey(dk[config["Grab"]])

# Convert String Commands to Functions
moveKeys = ["Up","Down","Left","Right"]
pullKeys = ["Pull Up", "Pull Down","Pull Left", "Pull Right"]
pushKeys = ["Push Up", "Push Down", "Push Left", "Push Right"]

### Interpreter
def init(filePath):
	data = json.load(open(filePath))
	time.sleep(3)
	for c in data['Main']:
		try:
			if c in moveKeys:
				Move(c)
			elif c in pullKeys:
				pass
			elif c in pushKeys:
				Action(c.split(" ")[-1])
		except Exception as e:
			print("Ahhh")
			print(e)

