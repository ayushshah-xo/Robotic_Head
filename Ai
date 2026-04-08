import time
import math
import random
import requests
import threading
import subprocess
import socket
import speech_recognition as sr
from adafruit_servokit import ServoKit
from groq import Groq

# ─── Hardware Setup ───────────────────────────────────────────
kit = ServoKit(channels=16)
for ch in [0, 4, 5]:
    kit.servo[ch].set_pulse_width_range(500, 2500)

JAW_CLOSED = 61
JAW_OPEN   = 108
BROW_DOWN  = 30
BROW_UP    = 120

# ─── API Key ──────────────────────────────────────────────────
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxx"  # paste your Groq key here

# ─── Servo Movement ───────────────────────────────────────────
def move_jaw(open=True, duration=0.12, steps=40):
    jaw_start = JAW_CLOSED if open else JAW_OPEN
    jaw_end   = JAW_OPEN   if open else JAW_CLOSED
    for i in range(steps + 1):
        t = i / steps
        e = -(math.cos(math.pi * t) - 1) / 2
        kit.servo[0].angle = jaw_start + e * (jaw_end - jaw_start)
        time.sleep(duration / steps)

def move_brows(up=True, duration=0.15, steps=40):
    left_start  = BROW_DOWN if up else BROW_UP
    left_end    = BROW_UP   if up else BROW_DOWN
    right_start = BROW_UP   if up else BROW_DOWN
    right_end   = BROW_DOWN if up else BROW_UP
    for i in range(steps + 1):
        t = i / steps
        e = -(math.cos(math.pi * t) - 1) / 2
        kit.servo[4].angle = left_start  + e * (left_end  - left_start)
        kit.servo[5].angle = right_start + e * (right_end - right_start)
        time.sleep(duration / steps)

def neutral():
    kit.servo[0].angle = JAW_CLOSED
    kit.servo[4].angle = BROW_DOWN
    kit.servo[5].angle = BROW_UP

# ─── Blink Loop ───────────────────────────────────────────────
brow_lock = threading.Lock()

def blink_loop():
    while True:
        time.sleep(random.uniform(2.5, 3.5))
        with brow_lock:
            move_brows(up=True,  duration=0.15)
            time.sleep(0.1)
            move_brows(up=False, duration=0.15)

blink_thread = threading.Thread(target=blink_loop)
blink_thread.daemon = True
blink_thread.start()

# ─── Speak ────────────────────────────────────────────────────
def speak(text):
    print(f"Sukuna: {text}")
    stop_flag = [False]

    def jaw_loop():
        while not stop_flag[0]:
            move_jaw(open=True,  duration=0.12)
            time.sleep(0.05)
            move_jaw(open=False, duration=0.12)
            time.sleep(0.1)

    t = threading.Thread(target=jaw_loop)
    t.daemon = True
    t.start()

    subprocess.run(["espeak", "-v", "en", "-s", "150", "-p", "30", "-w", "/tmp/sukuna.wav", text])
    subprocess.run(["aplay", "-D", "hw:2,0", "/tmp/sukuna.wav"])

    stop_flag[0] = True
    t.join()
    neutral()

# ─── Internet Check ───────────────────────────────────────────
def is_connected():
    try:
        r = requests.get("https://www.google.com", timeout=5)
        if r.status_code == 200:
            print("Internet: Connected")
            return True
    except:
        pass
    print("Internet: Not connected")
    return False

# ─── Groq (Online) ────────────────────────────────────────────
def ask_groq(question):
    try:
        print("Internet found, asking Groq...")
        client = Groq(api_key=GROQ_API_KEY)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=100,
            messages=[
                {"role": "system", "content": "You are Sukuna, a powerful and direct being. Answer every question in 1-2 short sentences only. Never be wordy."},
                {"role": "user",   "content": question}
            ]
        )
        return chat.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        return None

# ─── Ollama (Offline) ─────────────────────────────────────────
def ask_ollama(question):
    try:
        print("No internet, asking Ollama...")
        r = requests.post("http://localhost:11434/api/generate",
            json={"model": "tinyllama",
                  "prompt": f"Answer in 2 sentences: {question}",
                  "num_predict": 60,
                  "stream": False},
            timeout=60)
        return r.json()["response"]
    except Exception as e:
        print(f"Ollama error: {e}")
        return "I cannot answer right now."

# ─── Smart Ask (auto switch) ──────────────────────────────────
def ask(question):
    if is_connected():
        answer = ask_groq(question)
        if answer:
            return answer
        print("Groq failed, falling back to Ollama...")
        return ask_ollama(question)
    else:
        print("No internet, using Ollama...")
        return ask_ollama(question)

# ─── Listen ───────────────────────────────────────────────────
def listen():
    r = sr.Recognizer()
    r.energy_threshold = 150
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.8
    mic = sr.Microphone(device_index=1)
    print("Listening... (speak now)")
    with mic as source:
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
            text = r.recognize_google(audio).lower()
            print(f"Heard: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand")
            return ""
        except sr.WaitTimeoutError:
            print("Timeout")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

# ─── Main Loop ────────────────────────────────────────────────
print("Sukuna starting...")
neutral()
speak("Sukuna is ready.")

while True:
    input("Press ENTER then say your question...")
    time.sleep(0.5)
    question = listen()
    if question:
        speak("Let me think.")
        answer = ask(question)
        speak(answer)
    neutral()
