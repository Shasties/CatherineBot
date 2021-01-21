from inputs import get_gamepad
import time

controller_events = ["ABS_HAT0X","ABS_HAT0Y","BTN_SOUTH"]
controller_toggle = ["BTN_TL"]

def recordInputs():
    input_list = []
    state_queue = {}
    toggled = False

    for e in controller_events:
        state_queue[e] = time.time()
    # Record inputs until toggle is pressed
    while not toggled:
        events = get_gamepad()
        for event in events:
            current_time = time.time()
            if event.code in controller_events:
                try: # Record how long an event lasted
                    previous_event = state_queue[event.code]
                    input_list.append({"Event": event.code, "Start": previous_event[1], "End": current_time, "State": previous_event[0]})
                    state_queue[event.code] = [event.state,current_time]
                except Exception as e: # Used to initialize state_queue
                    state_queue[event.code] = [event.state,current_time]
            elif event.code in controller_toggle and event.state == 0:
                toggled = True
    return cleanInputs(input_list)

# Event.code[event.state] = Keyword
translate_events = {
    "ABS_HAT0X": {-1: "Left", 1: "Right", 0: "IGNORE"},
    "ABS_HAT0Y": {-1: "Up", 1: "Down", 0: "IGNORE"},
    "BTN_SOUTH": {1: "Grab", 0: "IGNORE"}
}

def cleanInputs(unclean_inputs):
    print(unclean_inputs)
    clean_inputs = []
    for item in unclean_inputs:
        if translate_events[item['Event']][item['State']] != "IGNORE":
            clean_inputs.append(item)

    clean_inputs = sorted(clean_inputs, key=lambda k: k['Start'])
    start_time = clean_inputs[0]['Start']
    for item in clean_inputs:
        item['Start'] = round(item['Start'] - start_time,2)
        item['End'] = round(item['End'] - start_time,2)
        item['State'] = translate_events[item['Event']][item['State']]
    return clean_inputs