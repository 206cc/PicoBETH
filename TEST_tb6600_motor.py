# TB6600&MOTOR TEST v1.4 https://github.com/206cc/PicoBETH
# YouTube Example https://youtu.be/7eG5W6a95h0

# This program is a standalone test to check if the TB6600 stepper motor driver and the 57 stepper motor are functioning properly.
# Wiring
# TB6600 DIR- <-> Raspberry Pi Pico GPIO 2
# TB6600 DIR+ <-> Raspberry Pi Pico GPIO 3
# TB6600 PUL- <-> Raspberry Pi Pico GPIO 4
# TB6600 PUL+ <-> Raspberry Pi Pico GPIO 5
# TB6600 A+   <-> MOTOR Red wire (As indicated on the actual label)
# TB6600 A-   <-> MOTOR Green wire (As indicated on the actual label)
# TB6600 B+   <-> MOTOR Yellow wire (As indicated on the actual label)
# TB6600 B-   <-> MOTOR Blue wire (As indicated on the actual label)
# TB6600 VCC  <-> 19V3A +
# TB6600 GND  <-> 19V3A -
#
# Set To Fast Mode
# TB6600 SW1  SW2  SW3  SW4  SW5  SW6 
#        ON   OFF  OFF  OFF  OFF  OFF
#
# Test Results: The 57 stepper motor will rotate one full turn clockwise and then one full turn counterclockwise

# 此為單獨測試TB6600步進馬達控制器及57步進馬達是否正常的程式
# 接線方式
# TB6600 DIR- <-> Raspberry PICO GPIO 2
# TB6600 DIR+ <-> Raspberry PICO GPIO 3
# TB6600 PUL- <-> Raspberry PICO GPIO 4
# TB6600 PUL+ <-> Raspberry PICO GPIO 5
# TB6600 A+   <-> MOTOR RED 紅線 (依實際標示為準)
# TB6600 A-   <-> MOTOR GREEN 綠線 (依實際標示為準)
# TB6600 B+   <-> MOTOR YELLOW 黃線 (依實際標示為準)
# TB6600 B-   <-> MOTOR BLUE 藍線 (依實際標示為準)
# TB6600 VCC  <-> 19V3A +
# TB6600 GND  <-> 19V3A -
#
# 設定成快速模式 
# TB6600 SW1  SW2  SW3  SW4  SW5  SW6 
#        ON   OFF  OFF  OFF  OFF  OFF
#
# 測試結果: 57步進馬達會正轉一圈後再逆轉一圈

import time
import machine
from machine import Pin

MOTOR_SPEED = 100    # microsecond 微秒

DIR_POS = machine.Pin(3, machine.Pin.OUT)  # DIR+
DIR_NEG = machine.Pin(2, machine.Pin.OUT)  # DIR-
PUL_POS = machine.Pin(5, machine.Pin.OUT)  # PUL+
PUL_NEG = machine.Pin(4, machine.Pin.OUT)  # PUL-

def set_direction(forward=True):
    if forward:
        DIR_POS.value(1)
        DIR_NEG.value(0)
    else:
        DIR_POS.value(0)
        DIR_NEG.value(1)

def step_once(delay_us):
    PUL_POS.value(1)
    PUL_NEG.value(0)
    time.sleep_us(delay_us)
    PUL_POS.value(0)
    PUL_NEG.value(1)
    time.sleep_us(delay_us)

def forward(delay, steps):
    print("Forward")
    set_direction(False)
    for _ in range(steps):
        step_once(delay)

def backward(delay, steps):
    print("Backward")
    set_direction(True)
    for _ in range(steps):
        step_once(delay)

forward(MOTOR_SPEED, 1600)
time.sleep(1)
backward(MOTOR_SPEED, 1600)
