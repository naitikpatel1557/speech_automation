🎙️ Technick Automation Assistant

A fully thread-safe, local AI voice assistant for Windows built with Python.

Technick is a lightweight, responsive desktop assistant designed to automate daily tasks, control system hardware, and manage media entirely hands-free. Wrapped in a sleek, dark-mode Tkinter User Interface, it uses multi-threading to ensure the voice engine and graphical interface run simultaneously without ever freezing or crashing the Windows audio buffer.

✨ Key Features
-> Advanced System Control: Instantly toggle Windows Wi-Fi and Bluetooth on or off via integrated PowerShell and command-line scripts.
-> Smart Media Management: Adjust or mute system volume (via pyautogui) and screen brightness (via screen-brightness-control) using natural language commands. Voice feedback is meticulously timed to complete before volume adjustments occur.
-> Automated Messaging: Send WhatsApp messages completely hands-free using pywhatkit integration, complete with error-handling for offline states.
-> Rapid App Launcher: Quickly open essential developer tools and applications like Visual Studio Code, Android Studio, Command Prompt, and Google Chrome.
-> Thread-Safe UI: Features a custom Tkinter dashboard that displays real-time listener status (Listening, Recognizing, Executing) without blocking the pyttsx3 text-to-speech engine.

🛠️ Tech Stack & Libraries
Core: Python 3
Interface: Tkinter, Threading
Voice & Audio: SpeechRecognition, pyttsx3, pyaudio
Automation: pyautogui, pywhatkit, screen-brightness-control
System Integration: os, subprocess, Windows PowerShell

Created by: Naitik | TECHNICK-TN
