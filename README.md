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
