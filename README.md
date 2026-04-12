<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Mono&size=13&duration=2500&pause=800&color=6EE7B7&center=true&vCenter=true&width=500&lines=Raspberry+Pi+4+%C2%B7+Servo+Motors+%C2%B7+Python;Speech+Recognition+%C2%B7+Text-to-Speech;CAD+Design+%C2%B7+3D+Printed+Parts;Real-time+AI+%C2%B7+Facial+Expressions" alt="Stack ticker" />

<br/>

# 🤖 Humanoid Robot

**An open-source AI-powered robot with real-time voice conversation, expressive servo-driven facial animations, and a fully 3D-printed chassis — built on Raspberry Pi 4.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi-4-C51A4A?style=flat-square&logo=raspberry-pi&logoColor=white)](https://raspberrypi.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ayushshah-xo/Humanoid-Robot-?style=flat-square&color=facc15)](https://github.com/ayushshah-xo/Humanoid-Robot-/stargazers)

</div>

---

## What is this?

A fully functional humanoid robot built from scratch — mechanical design, embedded hardware, and AI software — by a student. It listens to you, thinks, responds aloud, and moves its face to match.

No cloud subscriptions. No black-box kits. Every part designed, printed, and coded by hand.

<br/>

<div align="center">

| <img src="assets/images/robot-main.jpeg" width="240" alt="Robot front view" /> | <img src="assets/images/cad-design.png" width="240" alt="CAD design" /> | <img src="assets/images/diagram.png" width="240" alt="System diagram" /> |
|:---:|:---:|:---:|
| **Built Robot** | **CAD Design** | **System Flow** |

</div>

---

## Features

| | |
|---|---|
| 🎤 **Voice I/O** | Listens via mic, responds via speaker |
| 🧠 **AI Brain** | Online + offline conversation modes |
| 😐 **Facial Expressions** | Servo-driven eyes, eyebrows, and mouth |
| ⚡ **Real-time** | Low-latency speech-to-response pipeline |
| 🧩 **Modular** | Swap hardware or swap AI model independently |
| 🖨️ **3D Printed** | Every structural part is printable and remixable |

---

## How it works

```
You speak
   ↓
Speech Recognition  ──── converts audio to text
   ↓
AI Model  ──────────────  generates a response
   ↓
Text-to-Speech  ─────────  synthesizes audio
   ↓
Speaker output  +  Servo animation  (synced mouth movement)
```

The servo controller runs in a separate thread so facial animation stays in sync with audio playback without blocking the main pipeline.

---

## Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi 4 | Main compute |
| Servo motors (×3) | Face actuation |
| Servo driver board | PCA9685 |
| USB microphone | Speech input |
| Speaker + amplifier | Audio output |
| 5V regulated supply | Motor power |
| 3D printed chassis | Structure |

> Wiring guide and GPIO pin map are in [`docs/hardware-setup.md`](docs/hardware-setup.md)

---

## Getting started

**Requirements:** Python 3.9+, Raspberry Pi OS (64-bit recommended)

```bash
# 1. Clone
git clone https://github.com/ayushshah-xo/Humanoid-Robot-.git
cd Humanoid-Robot-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure (copy and edit)
cp config.example.yaml config.yaml

# 4. Run
python3 main.py
```

> **First time?** See [`docs/quickstart.md`](docs/quickstart.md) for a step-by-step walkthrough including hardware connection and audio device setup.

---
## Libraries

Two kinds of dependencies power this project — Python packages and system-level tools.

**Python packages** — installed via pip:

| Package | Purpose |
|---|---|
| `adafruit-circuitpython-servokit` | PCA9685 servo driver control |
| `groq` | Online AI via Groq (Llama 3) |
| `SpeechRecognition` | Converts microphone audio to text |
| `pyaudio` | Raw audio stream for the mic |
| `requests` | HTTP calls to Groq and Ollama |
| `pyyaml` | Reads `config.yaml` at startup |

```bash
pip install -r requirements.txt
```

**System packages** — installed via apt:

| Package | Purpose |
|---|---|
| `espeak` | Offline text-to-speech engine |
| `python3-pyaudio` | PyAudio system binding |
| `portaudio19-dev` | Audio I/O backend |
| `alsa-utils` | Audio device control (`aplay`, `alsamixer`) |

```bash
sudo apt install espeak python3-pyaudio portaudio19-dev alsa-utils
```

**Offline AI engine** — Ollama runs locally on the Pi as a fallback when there is no internet:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama
```

> The robot automatically switches between Groq (online) and Ollama (offline) — no manual intervention needed.

---
## Folder structure
<p align="center">
  <img src="assets/images/Folder_Structure.png" width="800"/>
</p>

> ⚠️ config.yaml holds your API key — it is blocked by .gitignore and will never be pushed to GitHub. Only edit config.example.yaml when changing config structure.
---

## CAD & 3D printing

All structural files are in [`/cad`](cad/). Designed to be:

- Printed on any FDM printer (PLA recommended)
- Assembled with standard M3 hardware
- Modular — replace individual parts without reprinting everything

---

## Roadmap

- [ ] Face recognition — recognize known people
- [ ] Emotion AI — adapt expression to conversation tone
- [ ] Mobile app — wireless control and monitoring
- [ ] Locomotion — basic autonomous movement

---

## Contributing

Issues, pull requests, and forks are welcome.

If you improve a module or add a new one, open a PR — this project is meant to be remixed.

---

## Author

**Ayush Shah** — [github.com/ayushshah-xo](https://github.com/ayushshah-xo)
**Will Cogley** — https://github.com/will-cogley

---

<div align="center">

If this project helped you or inspired you — a ⭐ goes a long way.

</div>
