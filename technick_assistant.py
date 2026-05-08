import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import subprocess
import os 
import screen_brightness_control as sbc
import pyautogui 
import tkinter as tk         
from tkinter import messagebox 
import threading             
import time 

# ==========================================
# 1. Initialize Text-to-Speech Engine
# ==========================================
def speak(audio):
    """Makes the assistant speak safely without Windows muting her in the background."""
    # We create a fresh engine right here every time she speaks!
    engine = pyttsx3.init('sapi5') 
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170) 
    
    # Print what she is saying to your VS Code terminal
    print(f"Technick: {audio}") 
    
    # Make her speak
    engine.say(audio)
    engine.runAndWait()
    
    # A 1-second pause guarantees Windows finishes playing the sound out of your speakers
    # before the code moves on to press any buttons (like Volume Down).
    time.sleep(1) 

def take_command():
    """Listens to the microphone and converts speech to text."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            update_status("Listening...", "#00ffcc") 
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1) 
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            
    except sr.WaitTimeoutError:
        update_status("Waiting for command...", "gray")
        return "none"
    except Exception as e:
        update_status("Microphone Error", "red")
        return "none"

    try:
        update_status("Recognizing...", "yellow")
        query = r.recognize_google(audio, language='en-IN')
        update_status(f"You said: '{query}'", "white")
        
    except Exception:
        update_status("Could not understand audio", "red")
        return "none"
    
    return query.lower()

# ==========================================
# 2. Main Logic (Runs in Background Thread)
# ==========================================
def run_assistant():
    # Say hello!
    speak("Hi, hello!")
    speak("Hello Naitik, I am Technick. My systems are online.")
    update_status("Waiting for command...", "gray")
    
    while True:
        query = take_command()

        if query == "none":
            continue

        # --- Command 1: Check the Time ---
        if 'time' in query:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Boss, the current time is {time_now}")
            speak("Hi, I am listening to you.")

        # --- Command 2: Wikipedia Search ---
        elif 'wikipedia' in query or 'who is' in query or 'what is' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(results)
            except Exception:
                speak("Sorry Boss, I couldn't find any clear information about that.")
            speak("Hi, I am listening to you.")

        # --- Command 3: Send WhatsApp Message ---
        elif 'whatsapp' in query or 'message' in query or 'sumit' in query:
            speak("Opening WhatsApp to send the message. What message should I send?")
            
            msg = take_command()
            
            if msg != "none":
                speak("Sending message...")
                target_number = "+918511715908" 
                try:
                    import pywhatkit
                    pywhatkit.sendwhatmsg_instantly(target_number, msg, wait_time=15, tab_close=True)
                    speak("Message sent successfully.")
                except Exception as e:
                    speak("Sorry, I encountered an error. Please make sure your Wi-Fi is turned on and you are logged into WhatsApp Web.")
            else:
                speak("I didn't catch the message. Canceling WhatsApp.")
            
            speak("Hi, I am listening to you.")

        # --- Command 4: Turn OFF Wi-Fi ---
        elif ('turn off' in query or 'disable' in query) and 'wifi' in query.replace("-", ""):
            speak("Disconnecting Wi-Fi, Boss.")
            try:
                subprocess.run('netsh wlan disconnect', shell=True)
            except Exception:
                speak("I encountered an error trying to turn off the Wi-Fi.")
            speak("Hi, I am listening to you.")

        # --- Command 5: Turn ON Wi-Fi ---
        elif ('turn on' in query or 'enable' in query) and 'wifi' in query.replace("-", ""):
            speak("Reconnecting Wi-Fi, Boss.")
            try:
                subprocess.run('netsh wlan connect name="YOUR_WIFI_NAME"', shell=True)
            except Exception:
                speak("I encountered an error trying to turn on the Wi-Fi.")
            speak("Hi, I am listening to you.")

        # --- Command 6 & 7: Bluetooth ---
        elif ('turn off' in query or 'disable' in query) and 'bluetooth' in query:
            speak("Turning off Bluetooth, Boss.")
            try:
                ps_script = "[Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; $radios = [Windows.Devices.Radios.Radio]::GetRadiosAsync().GetResults(); foreach ($radio in $radios) { if ($radio.Kind -eq 'Bluetooth') { [void]$radio.SetStateAsync('Off').GetResults() } }"
                subprocess.run(["powershell", "-Command", ps_script], shell=True)
            except Exception:
                speak("Error turning off Bluetooth.")
            speak("Hi, I am listening to you.")

        elif ('turn on' in query or 'enable' in query) and 'bluetooth' in query:
            speak("Turning on Bluetooth, Boss.")
            try:
                ps_script = "[Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; $radios = [Windows.Devices.Radios.Radio]::GetRadiosAsync().GetResults(); foreach ($radio in $radios) { if ($radio.Kind -eq 'Bluetooth') { [void]$radio.SetStateAsync('On').GetResults() } }"
                subprocess.run(["powershell", "-Command", ps_script], shell=True)
            except Exception:
                speak("Error turning on Bluetooth.")
            speak("Hi, I am listening to you.")

        # --- Command 8: Open Applications ---
        elif 'open notepad' in query:
            speak("Opening Notepad.")
            os.system("notepad")
            speak("Hi, I am listening to you.")
            
        elif 'open calculator' in query or 'open calc' in query:
            speak("Opening Calculator.")
            subprocess.Popen('calc.exe')
            speak("Hi, I am listening to you.")
            
        elif 'open command prompt' in query or 'open cmd' in query:
            speak("Opening Command Prompt.")
            os.system("start cmd")
            speak("Hi, I am listening to you.")
            
        elif 'open chrome' in query or 'open browser' in query:
            speak("Opening Google Chrome.")
            os.system("start chrome")
            speak("Hi, I am listening to you.")
            
        elif 'open android studio' in query:
            speak("Opening Android Studio.")
            try:
                studio_path = r"C:\Program Files\Android\bin\studio64.exe"
                os.startfile(studio_path)
            except Exception:
                speak("I couldn't find Android Studio.")
            speak("Hi, I am listening to you.")
                
        elif 'open vs code' in query or 'open code' in query:
            speak("Opening Visual Studio Code.")
            os.system("code")
            speak("Hi, I am listening to you.")

        # --- Command 9: Control Brightness ---
        elif 'brightness' in query:
            try:
                if 'increase' in query or 'up' in query:
                    speak("Increasing the brightness.")
                    sbc.set_brightness('+20') 
                elif 'decrease' in query or 'down' in query:
                    speak("Decreasing the brightness.")
                    sbc.set_brightness('-20') 
                else:
                    level = next((int(word) for word in query.split() if word.isdigit()), None)
                    if level is not None:
                        speak(f"Setting brightness to {level} percent.")
                        sbc.set_brightness(level)
            except Exception:
                speak("Error adjusting brightness.")
            speak("Hi, I am listening to you.")

        # --- Command 10: Control Volume ---
        elif 'volume' in query or 'mute' in query or 'unmute' in query:
            try:
                if 'mute' in query and 'unmute' not in query:
                    speak("Muting the volume.")
                    # The sleep() inside speak() ensures she finishes talking before this happens!
                    pyautogui.press('volumemute')
                    
                elif 'unmute' in query:
                    pyautogui.press('volumemute')
                    speak("Unmuting the volume.") 
                    
                elif 'increase' in query or 'up' in query:
                    speak("Increasing the volume.")
                    pyautogui.press('volumeup', presses=10)
                    
                elif 'decrease' in query or 'down' in query:
                    speak("Decreasing the volume.")
                    pyautogui.press('volumedown', presses=10)
                    
                else:
                    level = next((int(word) for word in query.split() if word.isdigit()), None)
                    if level is not None:
                        speak(f"Setting volume to {level} percent.")
                        level = max(0, min(100, level)) 
                        pyautogui.press('volumedown', presses=50) 
                        pyautogui.press('volumeup', presses=(level // 2)) 
            except Exception:
                speak("Error adjusting volume.")
            
            speak("Hi, I am listening to you.")

        # --- Command 11: Sleep/Exit ---
        elif 'good night' in query or 'so jao' in query or 'sleep' in query or 'exit' in query:
            speak("Good night Boss. Shutting down systems.")
            app.quit() # Closes the GUI window safely
            break
            
        else:
            if len(query.strip()) > 2:
                speak("I heard you, but I don't have a command programmed for that yet.")
            update_status("Waiting for command...", "gray")


# ==========================================
# 3. User Interface Setup (Tkinter)
# ==========================================
def update_status(text, color):
    """Updates the text on the UI screen safely."""
    status_label.config(text=text, fg=color)

def start_assistant_thread():
    """Starts the voice assistant in the background when the button is clicked."""
    start_button.config(state=tk.DISABLED, text="Technick is Online", bg="#005580")
    threading.Thread(target=run_assistant, daemon=True).start()

def show_welcome_popup():
    """Shows the greeting popup when the app first opens."""
    messagebox.showinfo("Welcome", "Hi, Hello! I am Technick AI.")

# Create the main window
app = tk.Tk()
app.title("Technick AI Assistant")
app.geometry("500x300")
app.configure(bg="#1e1e1e") # Dark mode background

# App Title Label
title_label = tk.Label(app, text="TECHNICK AI", font=("Helvetica", 26, "bold"), bg="#1e1e1e", fg="#00aaff")
title_label.pack(pady=20)

# Live Status Label
status_label = tk.Label(app, text="System Offline. Click Start.", font=("Helvetica", 14), bg="#1e1e1e", fg="gray")
status_label.pack(pady=20)

# Start Button
start_button = tk.Button(app, text="Start Listening", font=("Helvetica", 14, "bold"), bg="#00aaff", fg="white", 
                         activebackground="#0088cc", activeforeground="white", relief=tk.FLAT, padx=20, pady=10, 
                         command=start_assistant_thread)
start_button.pack(pady=20)

# Trigger the pop-up half a second after the UI opens
app.after(500, show_welcome_popup)

# Run the UI loop
app.mainloop()