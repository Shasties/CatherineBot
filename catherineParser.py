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
def Move(direction,delay=.2):
	PressKey(dk[config[direction]])
	time.sleep(delay) # Replace with a better condition
	ReleaseKey(dk[config[direction]])

# Push/Pull
def Action(direction,pull=None):
	delay = .6
	# If pulling - ensure you are grabbing the right block
	# I.e. 'Pull Right' needs to face left first
	if pull:
		delay = 1
		PressKey(dk[config[pull]])
		ReleaseKey(dk[config[pull]])
		PressKey(dk[config["Grab"]])
		PressKey(dk[config[direction]])
	else:
		PressKey(dk[config[direction]])
		PressKey(dk[config["Grab"]])
	time.sleep(delay)
	ReleaseKey(dk[config[direction]])
	ReleaseKey(dk[config["Grab"]])

# References for keywords in file
moveKeys = ["Up","Down","Left","Right"]
climbKeys = ["Climb Up", "Climb Down", "Climb Left", "Climb Right"]
turnKeys = ["Turn Up", "Turn Down", "Turn Left", "Turn Right"]
pullKeys = ["Pull Up", "Pull Down","Pull Left", "Pull Right"]
pushKeys = ["Push Up", "Push Down", "Push Left", "Push Right"]

# Simplify turning
inverseDirections = {
	"Up": "Down",
	"Down": "Up",
	"Left": "Right",
	"Right": "Left",
}

### Interpreter
def init(filePath):
	data = json.load(open(filePath))
	pushed_keys = {"Up": False, "Down": False, "Left": False, "Right": False, "Grab": False}
	if data['Style'] == "Manual":
		for c in data['Main']:
			try:
				if c in moveKeys:
					Move(c)
				elif c in climbKeys:
					Move(c.split(" ")[1],delay=.6)
				elif c in turnKeys:
					Move(c.split(" ")[1],delay=.1)
				elif c in pullKeys:
					direction = c.split(" ")[1]
					Action(direction,pull=inverseDirections[direction])
				elif c in pushKeys:
					Action(c.split(" ")[1])
				else:
					print(c+" is not recognized as a command")
				print(c)
			except Exception as e:
				print(e)

	elif data['Style'] == "Recorded":
		print("Reading Recorded file")
		total_time = sorted(data['Main'], key=lambda k: k['End'])[-1]['End']
		start_time = round(time.time(),2)
		print("length of recording: "+str(total_time))
		while time.time() < start_time+total_time:
			timer = round(time.time() - start_time,2)
			for c in data['Main']:
				if timer > c['Start'] and timer < c['End'] and not pushed_keys[c['State']]:
					print("pressing key "+ c['State'])
					PressKey(dk[config[c['State']]])
					pushed_keys[c['State']] = True
				elif timer == c['End'] and pushed_keys[c['State']]:
					print("releasing "+c['State'])
					ReleaseKey(dk[config[c['State']]])
					pushed_keys[c['State']] = False