# HX711 TEST v1.2 https://github.com/206cc/PicoBETH
# YouTube Example https://youtu.be/pZT4ccE3bZk

# This program is a standalone test for HX711 RATE and drift during stillness, outputting results once every 60 seconds by default.
# Wiring
# HX711 VCC           <-> Raspberry Pi Pico 5V
# HX711 DT/DO/RX/DAT  <-> Raspberry Pi Pico GPIO 26
# HX711 SCK/CK/TX/CLK <-> Raspberry Pi Pico GPIO 27
# HX711 GND           <-> Raspberry Pi Pico GND
# HX711 E+/RED        <-> NJ5 20KG Red wire
# HX711 E-/BLK        <-> NJ5 20KG Black wire
# HX711 A+/GRN        <-> NJ5 20KG Green wire
# HX711 A-/WHT        <-> NJ5 20KG White wire
# Test Results: Sampling rate above 75Hz
#               Drift during stillness approximately 0.5 grams, more than 1 gram is considered unqualified

# 此為單獨測試HX711 RATE及靜止時張力飄移的測試程式，預設60秒輸出一次結果
# 接線方式
# HX711 VCC           <-> Raspberry PICO 5V
# HX711 DT/DO/RX/DAT  <-> Raspberry PICO GPIO 26
# HX711 SCK/CK/TX/CLK <-> Raspberry PICO GPIO 27
# HX711 GND           <-> Raspberry PICO GND
# HX711 E+/RED        <-> NJ5 20KG RED(紅線)
# HX711 E-/BLK        <-> NJ5 20KG BLACK(黑線)
# HX711 A+/GRN        <-> NJ5 20KG GREEN(綠線)
# HX711 A-/WHT        <-> NJ5 20KG WHITE(白線)
# 測試結果: REAT(採樣頻率)75Hz以上
#          Difrt(飄移)靜止時約0.5公克，超過1公克為不合格

import time, machine
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

print("Start testing...")
fail_drift = 0
i = 1
while True:
    v0 = []
    rate = 0
    drift = 0
    v0_arr = []
    t0 = time.ticks_ms()
    while True:
        if val := hx.get_value_noblock():
            v0.append(val)
            if (time.ticks_ms() - t0) > (TEST_SECONDS * 1000):
                v0_arr = sorted(v0)
                rate = int(len(v0_arr)/TEST_SECONDS)
                drift = (v0_arr[-1]-v0_arr[0]) / 1000
                print("TEST: "+ str(i) +" ("+ str(TEST_SECONDS) +"s)", end=" ")
                
                if rate < 75:
                    print("RATE: "+ str(rate) +"Hz "+ RED_COLOR +"FAIL"+ RESET_COLOR, end=" ")
                else:
                    print("RATE: "+ str(rate) +"Hz PASSED", end=" ")
                
                if drift > 1:
                    fail_drift = fail_drift + 1
                    print("DRIFT: "+ "{:4.2f}".format(drift) +"G "+ RED_COLOR +"FAIL("+ str(fail_drift) +"/"+ str(i) +")"+ RESET_COLOR, end=" ")
    
                else:
                    print("DRIFT: "+ "{:4.2f}".format(drift) +"G PASSED("+ str(fail_drift) +"/"+ str(i) +")", end=" ")
                
                print("V0: "+ str(v0_arr[0]))
                
                i = i + 1
                break