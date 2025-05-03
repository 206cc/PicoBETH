# Copyright 2024 Kuokuo <500119.cpc@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# HX711 TEST v1.3 https://github.com/206cc/PicoBETH
# YouTube Example https://youtu.be/pZT4ccE3bZk

# This program is a standalone test for HX711 RATE and drift during stillness, outputting results once every 10 seconds by default.
# Wiring
# HX711 VCC           <-> Raspberry Pi Pico 5V
# HX711 DT/DO/RX/DAT  <-> Raspberry Pi Pico GPIO 26
# HX711 SCK/CK/TX/CLK <-> Raspberry Pi Pico GPIO 27
# HX711 GND           <-> Raspberry Pi Pico GND
# HX711 E+/RED        <-> NJ5(YZC-133) 20KG Red wire
# HX711 E-/BLK        <-> NJ5(YZC-133) 20KG Black wire
# HX711 A+/GRN        <-> NJ5(YZC-133) 20KG Green wire
# HX711 A-/WHT        <-> NJ5(YZC-133) 20KG White wire
# Test Results: Sampling rate above 75Hz
#               Drift during stillness approximately 0.5 grams, more than 1 gram is considered unqualified
#
# Several factors can significantly affect DRIFT (zero-point drift), including:
# 1. A high-quality HX711 amplifier — I recommend using the original SparkFun version for its reliable and consistent performance.
# 2. A stable load cell — This project strongly recommends the NJ5-manufactured YZC-133, which offers superior stability compared to generic versions.
# 3. A low-ripple power supply — Providing the HX711 with a clean and stable power source is essential for minimizing drift.

# 此為單獨測試HX711 RATE及靜止時張力飄移的測試程式，預設10秒輸出一次結果
# 接線方式
# HX711 VCC           <-> Raspberry PICO 5V
# HX711 DT/DO/RX/DAT  <-> Raspberry PICO GPIO 26
# HX711 SCK/CK/TX/CLK <-> Raspberry PICO GPIO 27
# HX711 GND           <-> Raspberry PICO GND
# HX711 E+/RED        <-> NJ5(YZC-133) 20KG RED(紅線)
# HX711 E-/BLK        <-> NJ5(YZC-133) 20KG BLACK(黑線)
# HX711 A+/GRN        <-> NJ5(YZC-133) 20KG GREEN(綠線)
# HX711 A-/WHT        <-> NJ5(YZC-133) 20KG WHITE(白線)
# 測試結果: REAT(採樣頻率)75Hz以上
#          Difrt(飄移)靜止時約0.5公克，超過1公克為不合格
#
# 影響 DRIFT（零點飄移）的因素有很多，主要包括：
# 1. 高品質的 HX711 放大器 — 建議使用 SparkFun 出廠的原廠版本，品質穩定可靠。
# 2. 穩定的 Load Cell — 本專案強烈建議選用由 NJ5 製造的 YZC-133，穩定性明顯優於其他通用版本。
# 3. 低 Ripple 的電源 — 為 HX711 提供乾淨穩定的電源是降低飄移的關鍵。

import time, machine
from machine import I2C, Pin

from machine import Pin
from src.hx711 import *

TEST_SECONDS = 10
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"

try:
    hx = hx711(Pin(27), Pin(26))
    hx.set_power(hx711.power.pwr_up)
    hx.set_gain(hx711.gain.gain_128)
    hx.set_power(hx711.power.pwr_down)
    hx711.wait_power_down()
    hx.set_power(hx711.power.pwr_up)
    hx711.wait_settle(hx711.rate.rate_80)
except Exception as e:
    print(f"{RED_COLOR}HX711 INIT ERROR: {e}{RESET_COLOR}")
    sys.exit(1)

print(f"Start testing... Please wait for {TEST_SECONDS} seconds.")
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
                print(f"TEST: {i} ({TEST_SECONDS}s)", end=" ")
                
                if rate < 75:
                    print(f"RATE: {rate}Hz {RED_COLOR}FAIL{RESET_COLOR}", end=" ")
                else:
                    print(f"RATE: {rate}Hz PASSED", end=" ")
                
                if drift > 1:
                    fail_drift = fail_drift + 1
                    print(f"DRIFT: {drift:4.2f}G {RED_COLOR}FAIL({fail_drift}/{i}){RESET_COLOR}", end=" ")
    
                else:
                    print(f"DRIFT: {drift:4.2f}G PASSED({fail_drift}/{i})", end=" ")
                
                print(f"V0: {v0_arr[0]}")
                
                i = i + 1
                break
