# 🤖 Hardware Setup — Humanoid Robot

> **This document explains every wire and connection in the robot.**
> Even if you've never built a robot before, you'll understand this by the end!

---

## 📋 Table of Contents

- [What's Inside the Robot?](#whats-inside-the-robot)
- [Parts List](#parts-list)
- [How Everything Connects](#how-everything-connects)
  - [Raspberry Pi → PCA9685 Servo Driver](#1-raspberry-pi--pca9685-servo-driver)
  - [Servo Motors (Eyes & Jaw)](#2-servo-motors-eyes--jaw)
  - [Power Supply](#3-power-supply)
  - [USB Microphone](#4-usb-microphone)
  - [Speaker (Audio Jack)](#5-speaker-audio-jack)
- [Wiring Diagram](#wiring-diagram)
- [Pinout Reference](#pinout-reference)
- [Quick-Reference Table](#quick-reference-table)
- [Credits](#credits)

---

## 🧠 What's Inside the Robot?

Think of the robot's brain like a tiny computer — that's the **Raspberry Pi 4**. It tells the eyes and jaw when to move, listens through a microphone, and talks through a speaker. The **PCA9685** is a helper chip that controls all the motors so the Raspberry Pi doesn't get overloaded.

```
[ Microphone ] ──USB──┐
[ Speaker ]  ──3.5mm──┤
                       ├──► Raspberry Pi 4 ──I2C──► PCA9685 ──PWM──► Servo Motors
[ 5V Power ] ─────────┘                                │
                                              [ 5V Power for Servos ]
```

---

## 🛒 Parts List

| # | Part | Quantity | What it does |
|---|------|----------|--------------|
| 1 | Raspberry Pi 4 | 1 | The brain — runs all the code |
| 2 | PCA9685 16-Channel PWM Driver | 1 | Controls all servo motors |
| 3 | Servo Motor (for eye blinking) | 3 | Opens and closes the eyelids |
| 4 | Servo Motor (for jaw movement) | 1 | Opens and closes the mouth |
| 5 | USB Microphone | 1 | Listens to what you say |
| 6 | Speaker (3.5mm audio jack) | 1 | Lets the robot talk back |
| 7 | 5V Power Supply | 2 | Powers the Pi and the servos separately |
| 8 | Jumper Wires (Female-to-Female) | Several | Connect everything together |

---

## 🔌 How Everything Connects

### 1. Raspberry Pi → PCA9685 Servo Driver

The Raspberry Pi talks to the PCA9685 using a communication method called **I2C** — it only needs 4 wires!

> 💡 **Simple explanation:** I2C is like a telephone line. The Pi is the boss, and the PCA9685 picks up the call and moves the motors.

| Wire Color | Raspberry Pi Pin | PCA9685 Pin | Purpose |
|------------|-----------------|-------------|---------|
| 🔴 Red | Pin 1 (3.3V) | VCC | Power for the chip's brain |
| ⚫ Black | Pin 6 (Ground) | GND | Completes the circuit (return path) |
| 🟡 Yellow | Pin 3 (BCM 2 / SDA) | SDA | Sends data |
| 🟢 Green | Pin 5 (BCM 3 / SCL) | SCL | Keeps data in sync (clock) |

---

### 2. Servo Motors (Eyes & Jaw)

Servo motors plug directly into the **PCA9685 board** using the PWM headers along the bottom edge. Each servo has 3 wires:

- 🔴 **Red** → V+ (Positive power)
- ⚫ **Brown/Black** → GND (Ground)
- 🟡 **Yellow/Orange** → PWM signal (tells the motor what angle to move to)

| Servo | PCA9685 Channel | Function |
|-------|----------------|----------|
| Eye Servo 1 | Channel 0 | Left eye blink |
| Eye Servo 2 | Channel 1 | Right eye blink |
| Eye Servo 3 | Channel 2 | Upper eyelid control |
| Jaw Servo | Channel 3 | Jaw open / close |

> 💡 **Simple explanation:** Imagine the PCA9685 is a TV remote. Each channel is a button, and each servo is a TV. Press button 0 → Eye 1 moves!

---

### 3. Power Supply

The robot needs **two separate power supplies**:

#### ⚡ Power for the Raspberry Pi
- Use an official **5V USB-C power adapter** (at least 3A recommended)
- Plug it directly into the **USB-C port** on the Raspberry Pi 4

#### ⚡ Power for the Servo Motors (via PCA9685)
- Use a **5V–6V DC power supply**
- Connect to the **V+** and **GND** screw terminals on the PCA9685 board
- Do **NOT** power servos from the Raspberry Pi's GPIO pins — they draw too much current and can damage the Pi

> ⚠️ **Important:** Always power servos from a separate supply. The Raspberry Pi is sensitive!

---

### 4. USB Microphone

This is the simplest connection in the whole build!

- Plug the USB microphone directly into any **USB-A port** on the Raspberry Pi 4
- The Raspberry Pi will automatically detect it — no setup needed

> 💡 **Simple explanation:** It works just like plugging a USB mouse into a laptop.

---

### 5. Speaker (Audio Jack)

- Plug the speaker's **3.5mm audio jack** into the **audio output port** on the Raspberry Pi 4
- This is the small round port on the side of the Pi (same size as a phone headphone jack)

> 💡 **Simple explanation:** It's exactly like plugging headphones into your phone.

---

## 🗺️ Wiring Diagram

The diagram below shows the full wiring between the Raspberry Pi and the PCA9685 servo driver. A separate 5V–6V supply connects to the servo power terminals.

![Wiring Diagram — Raspberry Pi to PCA9685](https://raw.githubusercontent.com/ayushshah-xo/Humanoid-Robot-/main/docs/wiring-diagram.png)

*Full wiring overview: Raspberry Pi 4 → PCA9685 via I2C (4 wires). Servo power supplied separately via DC jack connector.*

---

## 📌 Pinout Reference

The image below shows exactly which pins on the Raspberry Pi are used and how they map to the PCA9685.

![Raspberry Pi Pinout → PCA9685 Connection](https://raw.githubusercontent.com/ayushshah-xo/Humanoid-Robot-/main/docs/pinout-diagram.png)

| Pi GPIO Pin # | BCM Name | PCA9685 Label | Wire Color |
|--------------|----------|---------------|------------|
| Pin 1 | 3.3V Power | VCC | 🔴 Red |
| Pin 6 | Ground | GND | ⚫ Black |
| Pin 3 | BCM 2 (SDA) | SDA | 🟡 Yellow |
| Pin 5 | BCM 3 (SCL) | SCL | 🟢 Green |

---

## 📊 Quick-Reference Table

All connections at a glance:

| Component | Connection Point | Interface | Notes |
|-----------|-----------------|-----------|-------|
| PCA9685 Servo Driver | Raspberry Pi GPIO (Pins 1, 3, 5, 6) | I2C | Default I2C address: 0x40 |
| Eye Servo 1 | PCA9685 Channel 0 | PWM | Left eye blink |
| Eye Servo 2 | PCA9685 Channel 1 | PWM | Right eye blink |
| Eye Servo 3 | PCA9685 Channel 2 | PWM | Upper eyelid |
| Jaw Servo | PCA9685 Channel 3 | PWM | Jaw open/close |
| USB Microphone | Raspberry Pi USB-A Port | USB | Auto-detected |
| Speaker | Raspberry Pi 3.5mm Jack | Analog Audio | Plug-and-play |
| Pi Power Supply | Raspberry Pi USB-C | 5V / 3A+ | Official adapter recommended |
| Servo Power Supply | PCA9685 V+ / GND terminals | 5V–6V DC | Separate from Pi power |

---

## 👤 Credits

This hardware setup document is part of the **Humanoid Robot** open-source project.

**Created by:** Ayush Shah
**GitHub:** [@ayushshah-xo](https://github.com/ayushshah-xo)
**Project Repository:** [Humanoid-Robot-](https://github.com/ayushshah-xo/Humanoid-Robot-)

---

> 📁 *This file lives at `docs/hardware-setup.md` in the repository.*
> 💬 *Have questions or found an issue? Open an issue on GitHub — contributions are welcome!*
