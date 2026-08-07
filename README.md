# Gesture-Controlled Hill Climb

Control Hill Climb Racing (or any game with arrow keys) using hand gestures!

## Gestures:
- ✊ Fist (all fingers closed) → BRAKE (Left Arrow)
- ✋ Open palm (all fingers open) → GAS (Right Arrow)

## Setup Instructions
1. Install Python 3.10.11
2. In terminal run to create a virtual environment
```py -3.10 -m venv .venv```
3. Activate  it ```.\.venv\Scripts\Activate.ps1```

(Verify the Python version: ```python --version```
It should show: Python 3.10.11)

4. Install dependencies:
   ```pip install -r requirements.txt```
5. Run the script:
   ```python gesture_control.py```

6. Open your Hill Climb Racing game/emulator and play with gestures.

Press **q** to quit the program.



# Build a Standalone .exe
The project can be packaged into a standalone Windows executable using PyInstaller.

1. Install PyInstaller, Make sure the virtual environment is activated:
```python -m pip install pyinstaller```
2. Build Using the `.spec` File The repository includes `gesture_control.spec`, which contains the PyInstaller configuration and includes the required MediaPipe modules.

Run:
pyinstaller --clean gesture_control.spec

3. Run the Executable
After a successful build, the executable will be located at:
dist/
└── gesture_control/
    └── gesture_control.exe

Run it with:
.\dist\gesture_control\gesture_control.exe

The executable can be run without manually executing gesture_control.py.

Note: If the project or virtual environment is moved to a different location, rebuild the executable using the .spec file from the new project location.
