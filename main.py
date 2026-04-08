import time
import math
import random
import requests
import threading
import subprocess
import socket
import yaml
import speech_recognition as sr
from adafruit_servokit import ServoKit
from groq import Groq

# ─── Load Config ──────────────────────────────────────────────
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

GROQ_API_KEY  = config["groq"]["api_key"]
OUTPUT_CARD   = config["audio"]["output_card"]
INPUT_DEVICE  = config["audio"]["input_device"]
ESPEAK_SPEED  = str(config["audio"]["espeak_speed"])
ESPEAK_PITCH  = str(config["audio"]["espeak_pitch"])
JAW_CLOSED    = config["servo"]["jaw_closed"]
JAW_OPEN      = config["servo"]["jaw_open"]
BROW_DOWN     = config["servo"]["brow_down"]
BROW_UP       = config["servo"]["brow_up"]
GROQ_MODEL    = config["ai"]["groq_model"]
OLLAMA_MODEL  = config["ai"]["ollama_model"]
MAX_TOKENS    = config["ai"]["max_tokens"]
PERSONALITY   = config["ai"]["personality"]
AUDIO_DEVICE  = f"hw:{OUTPUT_CARD},0"

# ─── Hardware Setup ───────────────────────────────────────────
kit = ServoKit(channels=16)
for ch in [0, 4, 5]:
    kit.servo[ch].set_pulse_width_range(500, 2500)

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

    subprocess.run(["espeak", "-v", "en", "-s", ESPEAK_SPEED, "-p", ESPEAK_PITCH, "-w", "/tmp/sukuna.wav", text])
    subprocess.run(["aplay", "-D", AUDIO_DEVICE, "/tmp/sukuna.wav"])

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
            model=GROQ_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": PERSONALITY},
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
            json={"model": OLLAMA_MODEL,
                  "prompt": f"Answer in 2 sentences: {question}",
                  "num_predict": 60,
                  "stream": False},
            timeout=60)
        return r.json()["response"]
    except Exception as e:
        print(f"Ollama error: {e}")
        return "I cannot answer right now."

# ─── Smart Ask ────────────────────────────────────────────────
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
    mic = sr.Microphone(device_index=INPUT_DEVICE)
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
