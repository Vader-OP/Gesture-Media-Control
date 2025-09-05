# Gesture Media Controller

Control your media (volume, play/pause, next/previous track) using hand gestures detected via your webcam. This project uses **Mediapipe** for hand tracking, **OpenCV** for webcam and overlay rendering, and **PyAutoGUI** to simulate media key presses.

A custom overlay shows your webcam feed in a designated box and displays a confirmation message whenever an action is triggered.

---

## Features

- Volume Up / Volume Down  
- Next Track / Previous Track  
- Play / Pause  
- Webcam feed integrated into a custom overlay  
- Confirmation text displayed in a top-right box  

---

## Requirements

- **Python 3.8 – 3.11** (this code may **not work** on older or newer versions)  
- Windows OS with a working webcam  

### Python Dependencies

```text
opencv-python >= 4.7.0
mediapipe >= 0.10.0
pyautogui >= 0.9.54
numpy >= 1.24.0
pillow >= 10.0.0
