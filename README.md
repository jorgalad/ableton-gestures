

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
- Ableton Live 
- Poetry (for managing dependencies)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jorgalad/ableton-gestures.git
cd gesture-controlled-ableton
```

### 2. Install dependencies with Poetry

```bash
poetry install
```

### 3. Run the project

Ensure your webcam is connected and then run the project:

```bash
poetry run python ableton_gestures.py
```

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



## Thanks
- Daniel Jones ([ideoforms](https://github.com/ideoforms)) 
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide)

## Support or Questions?
- [Subject Sound](http://www.courses.subjectsound.com)