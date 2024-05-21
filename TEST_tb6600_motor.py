# TB6600&MOTOR TEST v1.1 https://github.com/206cc/PicoBETH
# YouTube Example https://youtu.be/7eG5W6a95h0

# This program is a standalone test to check if the TB6600 stepper motor driver and the 57 stepper motor are functioning properly.
# Wiring
# TB6600 DIR- <-> Raspberry Pi Pico GPIO 2
# TB6600 DIR+ <-> Raspberry Pi Pico GPIO 3
# TB6600 PUL- <-> Raspberry Pi Pico GPIO 4
# TB6600 PUL+ <-> Raspberry Pi Pico GPIO 5
# TB6600 A+   <-> MOTOR Red wire
# TB6600 A-   <-> MOTOR Green wire
# TB6600 B+   <-> MOTOR Yellow wire
# TB6600 B-   <-> MOTOR Blue wire
# TB6600 VCC  <-> 12V3A +
# TB6600 GND  <-> 12V3A -
# TB6600 SW1  SW2  SW3  SW4  SW5  SW6 
#        OFF  ON   OFF  OFF  OFF  OFF
#
# Test Results: The 57 stepper motor will rotate one full turn clockwise and then one full turn counterclockwise

# 此為單獨測試TB6600步進馬達控制器及57步進馬達是否正常的程式
# 接線方式
# TB6600 DIR- <-> Raspberry PICO GPIO 2
# TB6600 DIR+ <-> Raspberry PICO GPIO 3
# TB6600 PUL- <-> Raspberry PICO GPIO 4
# TB6600 PUL+ <-> Raspberry PICO GPIO 5
# TB6600 A+   <-> MOTOR RED(紅線)
# TB6600 A-   <-> MOTOR GREEN(綠線)
# TB6600 B+   <-> MOTOR YELLOW(黃線)
# TB6600 B-   <-> MOTOR BLUE(藍線)
# TB6600 VCC  <-> 12V3A +
# TB6600 GND  <-> 12V3A -
# TB6600 SW1  SW2  SW3  SW4  SW5  SW6 
#        OFF  ON   OFF  OFF  OFF  OFF
#
# 測試結果: 57步進馬達會正轉一圈後再逆轉一圈

import time
import machine
from machine import Pin

MOTO_SPEED = 0.0001

IN1 = machine.Pin(4, machine.Pin.OUT) # 接 PUL-
IN2 = machine.Pin(5, machine.Pin.OUT) # 接 PUL+
IN3 = machine.Pin(2, machine.Pin.OUT) # 接 DIR-
IN4 = machine.Pin(3, machine.Pin.OUT) # 接 DIR+

def setStep(w1, w2, w3, w4):
    IN1.value(w1)
    IN2.value(w2)
    IN3.value(w3)
    IN4.value(w4)

def forward(delay, steps, check, init):
    print("forward")
    for i in range(0, steps):
        
        setStep(1, 0, 1, 0)
        setStep(0, 1, 0, 0)
        setStep(0, 1, 1, 1)
        setStep(1, 0, 1, 0)
        time.sleep(delay)

def backward(delay, steps, check, init):
    print("backward")
    for i in range(0, steps):
        setStep(0, 1, 0, 1)
        setStep(1, 0, 0, 1)
        setStep(1, 0, 1, 0)
        setStep(0, 1, 1, 0)
        time.sleep(delay)

backward(MOTO_SPEED, 1600, 1, 0)
time.sleep(1)
forward(MOTO_SPEED, 1600, 1, 0)