# HX711 TEST https://github.com/206cc/PicoBETH
# DT/DO/RX/DAT: GPIO 26
# SCK/CK/TX/CLK: GPIO 27

import time, _thread, machine
from machine import I2C, Pin

from machine import Pin
from src.hx711 import *

TEST_SECONDS = 60
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"

hx = hx711(Pin(27), Pin(26))
hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_80)

def tension_monitoring():
    i = 1
    while True:
        V0 = []
        RATE = 0
        DRIFT = 0
        v0_arr = []
        t0 = time.ticks_ms()
        while True:
            if val := hx.get_value_noblock():
                V0.append(val)
                if (time.ticks_ms() - t0) > (TEST_SECONDS * 1000):
                    v0_arr = sorted(V0)
                    RATE = int(len(v0_arr)/TEST_SECONDS)
                    DRIFT = (v0_arr[-1]-v0_arr[0]) / 1000
                    print("TEST: "+ str(i) +" ("+ str(TEST_SECONDS) +"s)", end=" ")
                    
                    if RATE < 75:
                        print("RATE: "+ str(RATE) +"Hz "+ RED_COLOR +"FAIL"+ RESET_COLOR, end=" ")
                    else:
                        print("RATE: "+ str(RATE) +"Hz PASSED", end=" ")
                    
                    if DRIFT > 1: 
                        print("DRIFT: "+ "{:4.2f}".format(DRIFT) +"G "+ RED_COLOR +"FAIL"+ RESET_COLOR, end=" ")
                    else:
                        print("DRIFT: "+ "{:4.2f}".format(DRIFT) +"G PASSED", end=" ")
                    
                    print("V0: "+ str(v0_arr[0]))
                    
                    i = i + 1
                    break

print("Start testing...")
tension_monitoring()


