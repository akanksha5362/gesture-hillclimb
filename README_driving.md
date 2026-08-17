# Gesture-Controlled Dr. Driving

Control **Dr. Driving** using real-time hand gestures with a webcam!

## Gestures

* ☝️ **Right hand index finger** → STEERING

  * Left → Steer Left
  * Center → Straight
  * Right → Steer Right
* ✊ **Left hand fist** → BRAKE
* ✋ **Left hand open palm** → ACCELERATOR

## Tech Stack

* Python 3.10.11
* OpenCV
* MediaPipe 0.10.10
* NumPy
* ADB
* Android Emulator

## Setup Instructions

1. Install **Python 3.10.11**

2. Create a virtual environment:

```bash
python3.10 -m venv .venv
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Verify Python:

```bash
python --version
```

It should show:

```text
Python 3.10.11
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Make sure your Android Emulator is running and ADB detects it:

```bash
adb devices
```

7. Open **Dr. Driving** and go to the driving screen.

8. Run the gesture controller:

```bash
python gesture_drive.py
```

9. Use your hands to control the game.

Press **Q** to quit the program.

## Controls

```text
Right Hand ☝️
← LEFT | CENTER | RIGHT →

Left Hand ✊ → BRAKE
Left Hand ✋ → ACCELERATOR
```

> **Note:** The ADB touch coordinates are calibrated for the tested **2400 × 1080 Android Emulator** configuration. Different screen resolutions may require recalibration.
