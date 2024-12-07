# LED Controller with PCA9685

This library allows you to control LEDs using the PCA9685 PWM driver with a microcontroller via I2C. The LEDs are controlled with adjustable brightness, and an example script shows how to cycle through the LEDs sequentially.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Code Explanation](#code-explanation)


## Features

- Control up to 16 LEDs using the PCA9685 PWM driver.
- Adjust brightness levels with precise duty cycles (0-100%).
- Sequential control example to cycle through all channels.
- Easy-to-use `LEDs` class abstraction for managing LED brightness.


## Requirements

- Microcontroller with I2C support (e.g., Raspberry Pi Pico).
- PCA9685 PWM driver module.
- LEDs (up to 16).
- Required libraries:
  - `machine` (standard for MicroPython).
  - `time` (standard for MicroPython).
  - `pca9685` (custom class for controlling the PCA9685).
  - `led` (custom class for controlling LEDs).


## Setup

### Hardware Connections

1. Connect the PCA9685 to your microcontroller using I2C:
   - **SCL (Clock)**: Connect to the appropriate SCL pin on your board (e.g., Pin 1 for Raspberry Pi Pico).
   - **SDA (Data)**: Connect to the appropriate SDA pin on your board (e.g., Pin 0 for Raspberry Pi Pico).
2. Power the PCA9685 module and LEDs:
   - Use an external power supply for LEDs if needed.
   - Ensure the microcontroller shares a common ground with the PCA9685.
3. Connect up to 16 LEDs to the PCA9685 channels.

### Software Setup

1. Install MicroPython on your microcontroller.
2. Upload the following files to your board:
   - `pca9685.py`: Class for controlling the PCA9685.
   - `led.py`: Class for managing LED brightness.
   - `main.py`: Example script for running the LED control sequence.


## Usage

1. Ensure all hardware connections are secure.
2. Run the `main.py` script on your board.

Example output:
- LEDs will sequentially light up with 50% brightness and then turn off, one after another.


## Code Explanation

### PCA9685 Class (`pca9685.py`)

- Low-level interface to the PCA9685 PWM driver.
- Provides methods to set PWM frequency and control individual channels.

### LEDs Class (`led.py`)

- Simplifies control of LEDs connected to the PCA9685.
- Provides methods to:
  - Set brightness with a duty cycle percentage.
  - Turn off LEDs.

### Main Script (`main.py`)

- Demonstrates sequential LED control:
  - Lights up each LED with 50% brightness.
  - Turns off the LED after a brief delay.
