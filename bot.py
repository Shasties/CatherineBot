from pathlib import Path,PureWindowsPath
from catherineParser import init


def launch_gui():
	pass
	# TODO
	# List files under ./files/commands
		# Allow User to select Commands to Load or Record their own 
def main():
	command_file = Path("./files/commands/Esky.json")
	command_path = PureWindowsPath(command_file)
	init(command_path)


if __name__ == "__main__":
	main()
