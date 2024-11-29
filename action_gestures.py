import cv2
import random 
import time
import threading
import numpy as np 
import rtmidi 

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Open MIDI port for sending CC's 
midiout = rtmidi.MidiOut()
midiout.open_port(0)

# Setup OSC
ip = "127.0.0.1"
to_ableton = 11000
from_ableton = 11001
client = SimpleUDPClient(ip, to_ableton)
dispatcher = Dispatcher()

# Stuff for gesture-beat synchronization
beat_counter = 0
gesture_detected = threading.Event()
current_gesture = None  # Tracks the detected gesture

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)

# Gesture specific Functions
def closed_fist_action():
    print("Closed Fist")
    client.send_message("/live/track/set/solo", [6, 1])

def open_palm_action():
    print("Open Palm")
    random_pitch = random.randint(12, 48)
    client.send_message("/live/clip/set/pitch_coarse", [1, 5, random_pitch])
    
def pointing_up_action():
    print("Point Up")
    client.send_message("/live/track/set/solo", [5, 1])
    client.send_message("/live/track/set/solo", [6, 1])
    client.send_message("/live/clip/fire", [5, 0])
          
def thumb_down_action():
    print("Thumb Down")
    client.send_message("/live/song/stop_all_clips", None)

def thumb_up_action():
    print("Thumb Up")
    client.send_message("/live/track/set/mute", [1, 1])
    client.send_message("/live/track/set/mute", [3, 0])

def victory_action():
    beat_repeat = random.randint(20, 120)
    client.send_message("/live/device/set/parameters/value", [1, 0, 1, 0, 0, 0, 40, beat_repeat, 10, 1, 2, 3, 5, 5, 6, 7, 8, 9, 10, 11])

def i_love_you_action():
    print("Love you")

def gesture_none():
    # Yeah I know, that's kinda ugly
    client.send_message("/live/device/set/parameters/value", [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    client.send_message("/live/clip/set/pitch_coarse", [1, 5, 0])
    client.send_message("/live/track/set/solo", [6, 0])
    client.send_message("/live/track/set/solo", [5, 0])
    client.send_message("/live/track/set/mute", [1, 0])
    client.send_message("/live/track/set/mute", [3, 1])
    
# Gesture to function mapping
gesture_functions = {
    "Closed_Fist": closed_fist_action,
    "Open_Palm": open_palm_action,
    "Pointing_Up": pointing_up_action,
    "Thumb_Down": thumb_down_action,
    "Thumb_Up": thumb_up_action,
    "Victory": victory_action,
    "ILoveYou": i_love_you_action,
}

def send_mod(cc=1, value=0):
    if value > 0 :
        print("Send Mod Value: ", value)
        cc = [0xB0, cc, value]
        midiout.send_message(cc)


# Callback function to process gesture recognition results
def result_callback(result, image, timestamp):
    global current_gesture, last_executed_gesture
    if result.gestures:
        detected_gesture = result.gestures[0][0].category_name
        # Ignore "Unknown" gesture
        if detected_gesture == "Unknown":
            current_gesture = None
            gesture_detected.clear()
            return
        # Set the current gesture and trigger the event
        if detected_gesture != current_gesture:
            print(f"Gesture detected: {detected_gesture}")
            current_gesture = detected_gesture
            gesture_detected.set()
            last_executed_gesture = current_gesture
    else:
        current_gesture = None
        gesture_none()
        gesture_detected.clear()
    
    # Track position when gesture == closed fist
    # Allows to send continuous values based on palm Y positions
    # https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks: 
            if gesture_detected.is_set() and current_gesture == "Closed_Fist":
                wrist = hand_landmarks[0] # This is how you access specific 'points' on the hands, 0 is wrist
                val1 = convert_range(wrist.y, 1.0, 0.0, 0, 127)
                send_mod(1, val1)
    
# Handle beat messages from Ableton
def on_beat_received(address, *args):
    global current_gesture, beat_counter
    beat_counter += 1
    if beat_counter % 4 == 0:  # Every 4 beats corresponds to a 16th note
        # If a gesture is detected, execute its action
        if gesture_detected.is_set() and current_gesture in gesture_functions:
            print(f"Beat received: {args}")
            gesture_functions[current_gesture]()  # Trigger the action
            gesture_detected.clear()  # Reset the gesture flag
            current_gesture = None
    # Reset the counter after a full measure
    if beat_counter >= 16:  # 
        beat_counter = 0

    
# When beat is received, trigger on_beat_received func
dispatcher.map("/live/song/get/beat", on_beat_received)

# Start the OSC server
def start_osc_server():
    server = ThreadingOSCUDPServer((ip, from_ableton), dispatcher)
    server.serve_forever()

osc_thread = threading.Thread(target=start_osc_server, daemon=True)
osc_thread.start()

# Tell Ableton to send beat info
client.send_message("/live/song/start_listen/beat", [])

# The thing that does the recognising
def initialize_recognizer(model_path):
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=result_callback
    )
    return vision.GestureRecognizer.create_from_options(options)

def main():
    model_path = "gesture_recognizer.task"
    recognizer = initialize_recognizer(model_path)

    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            print("Ignoring empty frame.")
            continue

        # MP wants to see RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        # Do the gesture recognition
        recognizer.recognize_async(mp_image, timestamp_ms=int(cv2.getTickCount() / cv2.getTickFrequency() * 1000))
        # Show your face
        cv2.imshow('Gesture Recognition', frame)
        
        if cv2.waitKey(5) & 0xFF == 27:  # Exit on 'Esc'
            break

    cap.release()
    cv2.destroyAllWindows()

main()