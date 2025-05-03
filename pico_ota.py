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

VERSION = "1.0.12"
VERDATE = "2025-04-24"

import network
import time
import urequests
import uhashlib
import os
import machine
import sys
import gc
import ujson

from machine import I2C, Pin
from src.pico_i2c_lcd import I2cLcd  # from https://github.com/T-622/RPI-PICO-I2C-LCD

OTA = {
    "ssid"     : "",
    "password" : "",
    "ota_url"  : "https://picobeth-ota.206cc.tw",
    "fw_list" : {},
    "ota_list" : {},
    "ota_file" : "pico_ota.py",
    "tmp_file" : "new_main.py",
    "tmp_ota"  : "new_pico_ota.py",
    "main_file": "main.py",
    "wifi_file": "wifi.txt"
}

BUTTON_UP = Pin(13, Pin.IN, Pin.PULL_DOWN)      # Up button 上按鍵
BUTTON_DOWN = Pin(12, Pin.IN, Pin.PULL_DOWN)    # Down button 下按鍵
BUTTON_LEFT = Pin(11, Pin.IN, Pin.PULL_DOWN)    # Left button 左按鍵
BUTTON_RIGHT = Pin(10, Pin.IN, Pin.PULL_DOWN)   # Right button 右按鍵
BUTTON_SETTING = Pin(14, Pin.IN, Pin.PULL_DOWN) # Setting button 設定按鍵
BUTTON_EXIT = Pin(15, Pin.IN, Pin.PULL_DOWN)    # Exit button 取消按鍵

# 2004 i2c LCD
I2C_ADDR     = 0x27
I2C_NUM_COLS = 20
I2C = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
LCD = I2cLcd(I2C, I2C_ADDR, 4, I2C_NUM_COLS)

def logs_cleanup():
    if 'logs.txt' in os.listdir() and os.stat('logs.txt')[6] > 100 * 1024:
        os.rename('logs.txt', 'logs.1.txt')

    if 'sys_log.txt' in os.listdir() and os.stat('sys_log.txt')[6] > 100 * 1024:
        os.rename('sys_log.txt', 'sys_log.1.txt')

# LCD PUTSTR
def lcd_putstr(text, x, y, length):
    text = text[:length]
    text = f'{text :{" "}<{length}}'
    LCD.move_to(x, y)
    LCD.putstr(text)

# errno check
def handle_error(e, func):
    global ERR_MSG
    ERR_MSG[0] = f"{e}/MEM:{gc.mem_free()} bytes"   
    logs_save(ERR_MSG[0], func)
    with open("sys_log.txt", "a") as f:
        sys.print_exception(e, f)

def load_wifi_config():
    lcd_putstr(" == PicoBETH OTA == ", 0, 0, I2C_NUM_COLS)
    try:
        wlan = network.WLAN(network.STA_IF)
    except:
        lcd_putstr("This is not a Pico W", 0, 1, I2C_NUM_COLS)
        lcd_putstr("Need Wi-Fi model    ", 0, 2, I2C_NUM_COLS)
        while True:
            time.sleep(1)
    
    lcd_putstr(f"Ver : {VERSION}", 0, 1, I2C_NUM_COLS)
    lcd_putstr(f"Date: {VERDATE}", 0, 2, I2C_NUM_COLS)
    lcd_putstr(f"Ghub: 206cc/PicoBETH", 0, 3, I2C_NUM_COLS)
    time.sleep(3)
    lcd_putstr(" == Wi-Fi Config == ", 0, 0, I2C_NUM_COLS)
    lcd_putstr("SSID:               ", 0, 1, I2C_NUM_COLS)
    lcd_putstr("PSWD:               ", 0, 2, I2C_NUM_COLS)
    lcd_putstr("                    ", 0, 3, I2C_NUM_COLS)
    global OTA
    try:
        if OTA['wifi_file'] not in os.listdir():
            with open(OTA['wifi_file'], "w") as f:
                f.write("ssid=picobeth\n")
                f.write("password=picobeth\n")
            
        with open(OTA['wifi_file'], "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("ssid="):
                    OTA["ssid"] = line[len("ssid="):]
                elif line.startswith("password="):
                    OTA["password"] = line[len("password="):]
                    
        lcd_putstr(f"{OTA['ssid']}", 6, 1, len(OTA['ssid']))
        lcd_putstr(f"{OTA['password']}", 6, 2, len(OTA['password']))
        lcd_putstr("  [SET to Connect]  ", 0, 3, I2C_NUM_COLS)
        
        while True:
            if BUTTON_SETTING.value():
                connect = connect_wifi()
                if connect == False:
                    lcd_putstr("                    ", 0, 2, I2C_NUM_COLS)
                    lcd_putstr("  [Please Reboot]   ", 0, 3, I2C_NUM_COLS)
                break
            
            time.sleep(0.05)
        
    except Exception as e:
        lcd_putstr("Update Error!", 0, 1, I2C_NUM_COLS)
        lcd_putstr("  [Please Reboot]   ", 0, 3, I2C_NUM_COLS)
        handle_error(e, "load_wifi_config()")
        while True:
            time.sleep(0.05)

def connect_wifi():
    try:
        lcd_putstr("                    ", 0, 3, I2C_NUM_COLS)
        i = 0
        while True:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
            time.sleep(0.5)
            wlan.active(True)
            time.sleep(0.5)

            if not wlan.isconnected():
                lcd_putstr("Connecting to Wi-Fi ", 0, 1, I2C_NUM_COLS)
                lcd_putstr("                    ", 0, 2, I2C_NUM_COLS)
                wlan.connect(OTA["ssid"], OTA["password"])
                timeout = 20
                x = 0
                while not wlan.isconnected() and timeout > 0:
                    lcd_putstr(".", x, 2, 1)
                    time.sleep(0.5)
                    timeout -= 1
                    x = x + 1
            
            if wlan.isconnected():
                lcd_putstr("Wi-Fi Connected!    ", 0, 1, I2C_NUM_COLS)
                lcd_putstr(f"IP:{wlan.ifconfig()[0]}", 0, 2, I2C_NUM_COLS)
                time.sleep(1)
                ota_update()
                return True
                
            else:
                lcd_putstr("Wi-Fi Connect Fail! ", 0, 1, I2C_NUM_COLS)
                lcd_putstr(f"Retrying... {i + 1}/3", 0, 2, I2C_NUM_COLS)
                i = i + 1
                time.sleep(2)
                
                if i >= 3:
                    return False
                    
    except Exception as e:
        handle_error(e, "connect_wifi()")
        return None

def sha1_file(filename):
    try:
        h = uhashlib.sha1()
        with open(filename, 'rb') as f:
            while True:
                data = f.read(512)
                if not data:
                    break
                h.update(data)
        return h.digest().hex()
    
    except Exception as e:
        handle_error(e, "sha1_file()")
        return None

def download_file_stream(url, filename):
    try:
        r = urequests.get(url, stream=True)
        with open(filename, "wb") as f:
            while True:
                chunk = r.raw.read(1024)
                if not chunk:
                    break
                f.write(chunk)
                gc.collect()
        r.close()
        return True
    
    except Exception as e:
        handle_error(e, "download_file_stream()")
        return False

def download_and_load_json(url, filename="list.json"):
    try:
        r = urequests.get(url, stream=True)
        with open(filename, "wb") as f:
            while True:
                chunk = r.raw.read(512)
                if not chunk:
                    break
                f.write(chunk)
                
        r.close()
        with open(filename, "r") as f:
            data = ujson.load(f)
        
        return data

    except Exception as e:
        handle_error(e, "download_and_load_json()")
        return None

def ota_update():
    try:
        global OTA
        lcd_putstr("== OTA FW Install ==", 0, 0, I2C_NUM_COLS)
        lcd_putstr("Checking FW List... ", 0, 1, I2C_NUM_COLS)
        lcd_putstr("                    ", 0, 2, I2C_NUM_COLS)
        lcd_putstr("                    ", 0, 3, I2C_NUM_COLS)
        get_list = f"{OTA['ota_url']}/list.json"
        ota_info = f"{OTA['ota_url']}/ota.json"
        i = 0
        while True:
            OTA["fw_list"] = download_and_load_json(get_list)
            OTA["ota_list"] = download_and_load_json(ota_info)
            if not OTA["fw_list"] or not OTA["ota_list"]:
                lcd_putstr(f"Get Fail - Retry {i + 1}/3", 0, 2, I2C_NUM_COLS)
                i = i + 1
                
                if i > 3:
                    lcd_putstr("Aborted", 0, 2, I2C_NUM_COLS)
                    lcd_putstr("  [Please Reboot]   ", 0, 3, I2C_NUM_COLS)
                    while True:
                        time.sleep(1)
            else:
                break
        
        fw_len = len(OTA['fw_list'])
        lcd_putstr(f"{OTA['fw_list'][0]['name']}", 0, 1, I2C_NUM_COLS)
        lcd_putstr(f"{OTA['fw_list'][0]['date']}", 0, 2, I2C_NUM_COLS)
        lcd_putstr(f"[1/{fw_len}]", 0, 3, 6)
        lcd_putstr("Press SET", 11, 3, 9)
        i = 0
        while True:
            if BUTTON_SETTING.value():
                break
            
            elif BUTTON_RIGHT.value() or BUTTON_LEFT.value():
                if BUTTON_RIGHT.value():
                    i = min(i + 1, fw_len - 1)
                        
                elif BUTTON_LEFT.value():
                    i = max(i - 1, 0)
                     
                lcd_putstr(f"[{i + 1}/{fw_len}]", 0, 3, 6)
                lcd_putstr(f"{OTA['fw_list'][i]['name']}", 0, 1, I2C_NUM_COLS)
                lcd_putstr(f"{OTA['fw_list'][i]['date']}", 0, 2, I2C_NUM_COLS)
                 
            time.sleep(0.05)

        lcd_putstr(f"{OTA['fw_list'][i]['name']}", 0, 1, I2C_NUM_COLS)
        lcd_putstr("Confirm Update?   ", 0, 2, I2C_NUM_COLS)
        lcd_putstr("[Press UP to update]", 0, 3, I2C_NUM_COLS)
        while True:
            if BUTTON_UP.value():
                break
            
            time.sleep(0.05)
                
        lcd_putstr("                    ", 0, 3, I2C_NUM_COLS)
        fw_name = OTA["fw_list"][i]["name"]
        fw_date = OTA["fw_list"][i]["date"]
        fw_sha1 = OTA["fw_list"][i]["sha1"]
        fw_filename = "{}_{}.py".format(fw_name, fw_date)
        ota_name = OTA["ota_list"][0]["name"]
        ota_date = OTA["ota_list"][0]["date"]
        ota_sha1 = OTA["ota_list"][0]["sha1"]
        ota_filename = "{}_{}.py".format(ota_name, ota_date)
        fw_url = f"{OTA['ota_url']}/{fw_filename}"
        ota_url = f"{OTA['ota_url']}/{ota_filename}"
        local_ota_sha1 = sha1_file(OTA["ota_file"])
        i = 0
        local_ota_flag = False
        while True:
            if i > 3:
                lcd_putstr("Aborted", 0, 2, I2C_NUM_COLS)
                lcd_putstr("  [Please Reboot]   ", 0, 3, I2C_NUM_COLS)
                while True:
                    time.sleep(1)
            
            lcd_putstr("Downloading FW...", 0, 2, I2C_NUM_COLS)
            download_file_stream(fw_url, OTA["tmp_file"])
            if not OTA["tmp_file"] in os.listdir():
                i = i + 1
                continue
            
            if local_ota_sha1 != ota_sha1:
                local_ota_flag = True
                download_file_stream(ota_url, OTA["tmp_ota"])
                if not OTA["tmp_ota"] in os.listdir():
                    i = i + 1
                    continue  
            
            lcd_putstr("Verifying Checksum..", 0, 2, I2C_NUM_COLS)
            actual_sha1 = sha1_file(OTA["tmp_file"])
            if local_ota_flag == True:
                actual_ota_sha1 = sha1_file(OTA["tmp_ota"])
                
            else:
                actual_ota_sha1 = 0
                ota_sha1 = 0
                
            if actual_sha1 != fw_sha1 or actual_ota_sha1 != ota_sha1:
                lcd_putstr("Checksum Failed!", 0, 2, I2C_NUM_COLS)
                os.remove(OTA["tmp_file"])
                os.remove(OTA["tmp_ota"])
                lcd_putstr(f"Retrying... {i + 1}/3", 0, 2, I2C_NUM_COLS)
                i = i + 1
                
            else:
                break
        
        if OTA["main_file"] in os.listdir():
            os.rename(OTA["main_file"], "main.bak.py")
        os.rename(OTA["tmp_file"], OTA["main_file"])

        # check pico_ota.py
        if local_ota_flag == True:
            if OTA["ota_file"] in os.listdir():
                os.rename(OTA["ota_file"], "pico_ota.bak.py")
            os.rename(OTA["tmp_ota"], OTA["ota_file"])

        lcd_putstr("Update Successful!", 0, 2, I2C_NUM_COLS)
        lcd_putstr("  [Please Reboot]   ", 0, 3, I2C_NUM_COLS)
        while True:
            time.sleep(1)
            
    except Exception as e:
        handle_error(e, "ota_update()")
        return None

if "ota" in os.listdir():
    os.remove("ota")
    
load_wifi_config()
