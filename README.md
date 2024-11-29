

```markdown
# Gesture-Controlled Ableton Live Controller

This project uses computer vision and gesture recognition to control various aspects of an Ableton Live session using hand gestures. The system recognizes predefined hand gestures and maps them to specific actions in Ableton Live through OSC (Open Sound Control) messages.

## Overview

The system utilizes a webcam to capture hand gestures in real-time. These gestures are processed using MediaPipe's gesture recognition model, and the corresponding actions are executed in Ableton Live using OSC and MIDI communication.

The project aims to create a gesture-based interface for controlling Ableton Live, which is often used by musicians and live performers.

## Features

- **Gesture Recognition**: Uses MediaPipe to recognize hand gestures in real-time.
- **OSC Communication**: Sends OSC messages to Ableton Live to control different parameters.
- **MIDI Control**: Sends MIDI CC (Control Change) messages to control music software.
- **Gesture Actions**: Each gesture corresponds to a specific action in Ableton Live (e.g., soloing tracks, changing pitch, stopping clips).
- **Synchronization with Beats**: Gestures are triggered in sync with the beat of the music.

## Requirements

- Python 3.x
- Poetry (for managing dependencies)
- OpenCV (`cv2`) for video capture
- Mediapipe for gesture recognition
- `rtmidi` for MIDI control
- `pythonosc` for OSC communication
- Ableton Live (for receiving OSC messages)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/gesture-controlled-ableton.git
cd gesture-controlled-ableton
```

### 2. Install dependencies with Poetry

```bash
poetry install
```

### 3. Run the project

Ensure your webcam is connected and then run the project:

```bash
poetry run python main.py
```

## Gesture Mapping

Below is the list of hand gestures and their corresponding actions in Ableton Live.

### 1. **Closed Fist**:
   - **Action**: Solos Track 6
   - **OSC Command**: `/live/track/set/solo [6, 1]`
   
   A closed fist gesture triggers the soloing of Track 6 in Ableton Live.

### 2. **Open Palm**:
   - **Action**: Change Pitch Coarse for Clip 1
   - **OSC Command**: `/live/clip/set/pitch_coarse [1, 5, random_pitch]`
   
   An open palm gesture changes the pitch of Clip 1 in Ableton Live to a random value between 12 and 48.

### 3. **Pointing Up**:
   - **Action**: Solos Track 5 and Track 6, and fires Clip 5
   - **OSC Commands**:
     - `/live/track/set/solo [5, 1]`
     - `/live/track/set/solo [6, 1]`
     - `/live/clip/fire [5, 0]`
   
   Pointing upward triggers soloing of Tracks 5 and 6 and fires Clip 5 in Ableton Live.

### 4. **Thumb Down**:
   - **Action**: Stops all clips in the current Ableton Live session
   - **OSC Command**: `/live/song/stop_all_clips None`
   
   A thumbs-down gesture stops all clips in Ableton Live.

### 5. **Thumb Up**:
   - **Action**: Mutes Track 1, Unmutes Track 3
   - **OSC Commands**:
     - `/live/track/set/mute [1, 1]`
     - `/live/track/set/mute [3, 0]`
   
   A thumbs-up gesture mutes Track 1 and unmutes Track 3.

### 6. **Victory**:
   - **Action**: Sends a specific device parameter value change
   - **OSC Command**: `/live/device/set/parameters/value [1, 0, 1, 0, 0, 0, 40, beat_repeat, 10, 1, 2, 3, 5, 5, 6, 7, 8, 9, 10, 11]`
   
   The "victory" gesture triggers a specific device parameter change that is customized using random values.

### 7. **I Love You**:
   - **Action**: Placeholder action for the "I Love You" gesture
   - **Output**: Prints "Love you" to the console
   - **Note**: Currently, no action is sent to Ableton Live for this gesture.

### 8. **No Gesture (None)**:
   - **Action**: Resets all parameters to their default state
   - **OSC Commands**:
     - `/live/device/set/parameters/value [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
     - `/live/clip/set/pitch_coarse [1, 5, 0]`
     - `/live/track/set/solo [6, 0]`
     - `/live/track/set/solo [5, 0]`
     - `/live/track/set/mute [1, 0]`
     - `/live/track/set/mute [3, 1]`
   
   If no gesture is detected, the system will reset all parameters.

## Workflow

1. **Gesture Recognition**: The webcam captures the user's hand movements. MediaPipe processes the video stream and recognizes the gesture in real-time.
2. **OSC Commands**: Once a gesture is detected, an OSC message is sent to Ableton Live to trigger a corresponding action, such as controlling track parameters or firing clips.
3. **MIDI Control**: Some gestures (e.g., "Closed Fist") also control MIDI values, which can be used to send control change messages to external music software.

## Notes

- The project is designed to work with Ableton Live and uses OSC to communicate with it. You need to configure Ableton Live to receive OSC messages on the specified ports.
- The gestures and actions are customizable. You can modify the gesture-action mappings in the `gesture_functions` dictionary.
- You can adjust the sensitivity of the gesture recognition by changing the confidence thresholds in the `initialize_recognizer` function.

## Conclusion

This project demonstrates how to integrate gesture-based controls into a live music setup using Ableton Live. By leveraging the power of MediaPipe for real-time hand gesture recognition and OSC for communication, you can create a more intuitive and immersive control interface for live performances.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Explanation:
- **Overview**: Provides a brief description of what the project is and its key features.
- **Installation**: Instructions for setting up the project using Poetry and running it.
- **Gesture Mapping**: A detailed description of each gesture and the associated Ableton Live actions.
- **Workflow**: Describes the process flow from gesture detection to action execution in Ableton Live.
- **Notes and Conclusion**: Additional context about the project and its customization options.

This README file provides a comprehensive guide to understanding the project, setting it up, and interacting with it.