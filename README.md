# 🤖 Jarvis Control

An Android-based remote PC control system built using **Kotlin** and **Python**.

This project allows a smartphone to control a Windows computer over Wi-Fi with features like live screen streaming, touchpad gestures, typing, app launching, media controls, and more.

---

# ✨ Features

* 🎥 Live screen stream
* 🖱️ Virtual touchpad
* ⌨️ Real-time typing on PC
* 🔊 Volume control
* 💡 Brightness control
* 📂 Open Downloads/Documents
* 📋 Copy / Paste / Cut shortcuts
* 🔄 Alt+Tab app switch
* 📸 Screenshot capture
* 🔒 Lock PC
* ⛔ Shutdown PC
* 🎵 Music control
* 🧮 Open Calculator
* 📝 Open Notepad

---

# 🛠️ Tech Stack

## Android App

* Kotlin
* Android Studio
* OkHttp

## PC Server

* Python
* HTTP Server
* PyAutoGUI
* MSS
* Pillow

---

# ⚙️ How It Works

1. Python server runs on the Windows PC.
2. Android app sends HTTP requests over local Wi-Fi.
3. Server executes commands using PyAutoGUI and Windows utilities.
4. Live screen stream is transferred to the mobile app in real time.

---

# 🚀 Setup

## PC Side

Install dependencies:

```bash
py -3.11 -m pip install pyautogui pillow mss```

Run server:

```bash
py -3.11 server.py
```

---

## Android Side

1. Open project in Android Studio
2. Change PC IP address in `MainActivity.kt`
3. Build APK
4. Install app on Android device

---

# 📦 APK

APK file is available inside the `apk` folder.

---

# 🔐 Security

This project uses a simple secret key system for request validation.

---

# 📡 Network Requirement

Both devices must be connected to the same Wi-Fi network.

---

# 📁 Project Structure

```text
Jarvis-Control
│
├── apk
├── screenshots
├── server.py
├── control.html
└── README.md
```

---

# 👨‍💻 Author

Harshit Sharma

---
