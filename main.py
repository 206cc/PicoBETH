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

# VERSION INFORMATION
VERSION = "2.90A"
VERDATE = "2025-05-30"

# GitHub  https://github.com/206cc/PicoBETH
# YouTube https://www.youtube.com/@kuokuo702
# On the first boot, please visit https://github.com/206cc/PicoBETH?tab=readme-ov-file#final-settings to see how to calibrate the HX tension parameters.
# For code updates, please visit https://github.com/206cc/PicoBETH#firmware-update to view the update steps.
# Basic parameters
# 第一次開機請至 https://github.com/206cc/PicoBETH?tab=readme-ov-file#final-settings 觀看如何校正 HX 張力參數
# 軟體升級請至 https://github.com/206cc/PicoBETH#firmware-update 觀看升級步驟
# 基本參數
KNOT = 15                       # Default Knot %
                                # 預設打結%
LB_MIN = 15                     # Minimum tension in LB
                                # 設定最高張力
LB_MAX = 35                     # Maximum tension in LB
                                # 設定最低張力
KNOT_RANG = [5, 30]             # Minimum/Maximum percentage for knot
                                # 打結增最低/高%
CA_REM = 0.1                    # LB value for HX711 Tension calibration reminder
                                # 張力校正提醒(磅)
HX711_DIFRT = 2.0               # Check the HX711 difrt in grams.
                                # 檢查HX711飄移值(公克)
LOAD_CELL_KG = 20               # The load cell capacity in KG.(20KG or 50KG)
                                # 使用的荷重元公斤數(20KG or 50KG)
JPLIEW = 0                      # 2086 Improved Bead Clip Head Activation Button. [0=Standard/1=Enhanced](https://github.com/206cc/PicoBETH/tree/imp/beadclip-btn%40jpliew)
                                # 2086 進階的珠夾啟動開關 [0=標準/1=建階](https://github.com/206cc/PicoBETH/tree/imp/beadclip-btn%40jpliew)
EXTRA_CONFIG = {
    "USE_PULLDOWN": True,       # True = PULL_DOWN, False = PULL_UP         
    "HEAD_RESET": 1,            # Bead clip head Reset Mode: 0=Limit switch impact method, 1=Step calculation method. 珠夾頭復位型式 0=限位開關撞擊方式 1=計算步數方式 
    "PS_MAX": 30,               # Maximum percentage in Pre-Strech 設定預拉的最高%
    "LOG_MAX": 50,              # Maximum LOG retention records (Please do not set too large to avoid memory exhaustion) 最大LOG保留記錄(請勿太大，以免記憶體耗盡)
    "CORR_COEF_AUTO": 1,        # Self-learning tension parameter 0=Off 1=On 自我學習張力參數 0=off 1=on
    "CP_FAST": 40,              # Gram value for triggering the fast constant-pull mechanism 觸發快速恆拉微調公克值
    "CP_SLOW": 30,              # Gram value for triggering constant tension adjustment 觸發恆拉微調公克值
    "MOTOR_SPEED_V1": 40,       # Stepper motor at high speed 步進馬達高速
    "MOTOR_SPEED_V2": 500,      # Stepper motor at medium speed 步進馬達中速
    "MOTOR_SPEED_V3": 1000,     # Stepper motor at low speed 步進馬達低速
    "MOTOR_DELAY_US": 0,        # Stepper motor delay us 步進馬達延遲
    "TENNIS": 40                # Initial tension for tennis 網球起始張力
}

import os, gc, sys
if "ota" in os.listdir() and "pico_ota.py" in os.listdir():
    try:
        os.remove("ota")
        import pico_ota
        sys.exit()

    except Exception as e:
        sys.exit()
        
import time, _thread, machine, random
from machine import I2C, Pin
from src.hx711 import hx711          # from https://github.com/endail/hx711-pico-mpy
from src.pico_i2c_lcd import I2cLcd  # from https://github.com/T-622/RPI-PICO-I2C-LCD

# Other parameters 其它參數
FIRST_TEST = 1
SAVE_CFG_ARRAY = ['DEFAULT_LB','PRE_STRECH','MOTOR_STEPS','HX711_CAL','TENSION_COUNT','BOOT_COUNT', 'LB_KG_SELECT','CP_SW','KNOT','FIRST_TEST','BZ_SW','HX711_V0','MOTOR_SPEED_LV','LOAD_CELL_KG','LB_MAX','JPLIEW'] # Saved variables 存檔變數
MENU_ARR = [[5,0],[4,1],[4,2],[14,0],[14,1],[15,1],[17,1],[18,1],[19,1],[8,3],[19,3]] # Array for LB setting menu 設定選單陣列
OPTIONS_DICT = {"UNIT_ARR":['LB', 'KG', ' '],
                "ONOFF_ARR":['Off', 'On '],
                "MA_ARR":['M', 'C'],
                "PSKT_ARR":['PS', 'KT'],
                "HEAD":['Standard', 'Enhanced']}
TS_LB_ARR = [[4,0],[5,0],[7,0]] # Array for LB setting 磅調整陣列
TS_KG_ARR = [[4,1],[5,1],[7,1]] # Array for KG setting 公斤調整陣列
TS_KT     = [[14,0]]            # Switching between knot and Pre-Strech 打結鍵切換
TS_PS_ARR = [[17,0],[18,0]]     # Array for Pre-Strech 預拉調整陣列
MOTOR_SPEED_LV = 8              # Default stepper motor speed level 預設的步進馬達速度等級
MOTOR_MAX_STEPS = 100000
MOTOR_RS_STEPS = 2000           # Number of steps to retreat during slider reset 滑台復位時退回的步數
CORR_COEF = 1.00                # Tension coefficient 張力系數
HX711_V0 = 0
RT_MODE = 0
HEAD_RESET_COUNT = 0
MOTOR_SPEED_RATIO = 0
ABORT_GRAM = 1000
HX711_CAL = LOAD_CELL_KG
LB_KG_SELECT = 0
DEFAULT_LB = 20.0
PRE_STRECH = 10
CP_SW = 1
BZ_SW = 1
MENU_TEMP = 0
MENU_LIST_ARR = {
    "9-1":["Load Cell:"          ,"Set Load Cell Rating",[16],'LOAD_CELL_KG'],
    "9-2":["Max Tension:"        ,"35LB to 70LB",[16],'LB_MAX'],
    "9-3":["Start Mode: "        ,"Tension Start Select",[12],'JPLIEW'],
    "9-6":["Boot Count:"         ,"Power On Counter",[None],'BOOT_COUNT'],
    "9-4":["Rate:"               ,"HX711 Rate (Hz)",[None],'HX711'],
    "9-5":["Drift:"              ,"HX711 Drift (g/s)",[None],'HX711']
#    "9-6":["Stability:"          ,"HX711 Stability",[None],'HX711']
,
}

EXTRA_CONFIG["PULL_TYPE"] = Pin.PULL_DOWN if EXTRA_CONFIG["USE_PULLDOWN"] else Pin.PULL_UP
EXTRA_CONFIG["PRESSED_STATE"] = 1 if EXTRA_CONFIG["USE_PULLDOWN"] else 0

# Initialize all GPIO pins to low 初始化所有 GPIO
for pin in range(28):
    Pin(pin, Pin.OUT).low()

# Stepper motor 步進馬達
DIR_POS = machine.Pin(3, machine.Pin.OUT)  # DIR+
DIR_NEG = machine.Pin(2, machine.Pin.OUT)  # DIR-
PUL_POS = machine.Pin(5, machine.Pin.OUT)  # PUL+
PUL_NEG = machine.Pin(4, machine.Pin.OUT)  # PUL-

# Limit switches for slider front and rear limits 滑台限位前後限位感應開關
MOTOR_SW_FRONT = Pin(6, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])  # Front limit 滑軌前限位感應開關
MOTOR_SW_REAR = Pin(7, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])   # Rear limit 滑軌後限位感應開關

# Function keys 功能按鍵
BUTTON_HEAD = Pin(8, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])     # Bead clamp head activation button 珠夾頭啟動按鍵
BUTTON_UP = Pin(13, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])      # Up button 上按鍵
BUTTON_DOWN = Pin(12, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])    # Down button 下按鍵
BUTTON_LEFT = Pin(11, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])    # Left button 左按鍵
BUTTON_RIGHT = Pin(10, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])   # Right button 右按鍵
BUTTON_SETTING = Pin(14, Pin.IN, EXTRA_CONFIG["PULL_TYPE"]) # Setting button 設定按鍵
BUTTON_EXIT = Pin(15, Pin.IN, EXTRA_CONFIG["PULL_TYPE"])    # Exit button 取消按鍵
BUTTON_LIST = {
    "BUTTON_HEAD":0,
    "BUTTON_SETTING":0,
    "BUTTON_EXIT":0,
    "BUTTON_UP":0,
    "BUTTON_DOWN":0,
    "BUTTON_LEFT":0,
    "BUTTON_RIGHT":0,
    "MOTOR_SW_FRONT":0,
    "MOTOR_SW_REAR":0}                          # Button list 按鈕列表          
BUTTON_CLICK_MS = 500                           # Button click milliseconds 按鈕點擊毫秒

# LED
LED_GREEN = Pin(19, machine.Pin.OUT)  # Green 綠
LED_YELLOW = Pin(20, machine.Pin.OUT) # Yellow 黃
LED_RED = Pin(21, machine.Pin.OUT)    # Red 紅

# Active buzzer 蜂鳴器
BEEP = Pin(22, machine.Pin.OUT)

# Global variables 全域變數
LB_CONV_G = 0
TENSION_MON = 0
MOTOR_ON = 0
MOTOR_STP = 0
MOTOR_STEPS = 0
CURSOR_XY_TEMP = 0
CURSOR_XY_TS_TEMP = 1
HX711 = {"RATE":0, "DIFF":0, "V0":[], "CP_HZ":0.125, "HX711_CAL": LOAD_CELL_KG}
TENSION_COUNT = 0
BOOT_COUNT = 0
TIMER = 0
ERR_MSG = ["", ""]
ABORT_LM = 0
TS_ARR = []
LOGS = []
KNOT_FLAG = 0
RT_CC = [1.0, 1.0]
TIMER_FLAG = 0

# 2004 i2c LCD
I2C_ADDR     = 0x27
I2C_NUM_COLS = 20
I2C = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
LCD = I2cLcd(I2C, I2C_ADDR, 4, I2C_NUM_COLS)

# HX711
hx = hx711(Pin(27), Pin(26))
hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_80)

# Logs cleanup 整理 LOGS
def logs_cleanup():
    if 'logs.txt' in os.listdir() and os.stat('logs.txt')[6] > 100 * 1024:
        os.rename('logs.txt', 'logs.1.txt')

    if 'sys_log.txt' in os.listdir() and os.stat('sys_log.txt')[6] > 100 * 1024:
        os.rename('sys_log.txt', 'sys_log.1.txt')

# Read file parameters 參數讀取
def config_read():
    global HX711
    if 'config.cfg' in os.listdir():
        file = open('config.cfg', 'r')
        data = file.read()
        config_list = data.split(',')
        for val in config_list:
            cfg = val.split("=")
            if cfg[0] and cfg[0] in SAVE_CFG_ARRAY:
                if "." in cfg[1]:
                    globals()[cfg[0]] = float(cfg[1])
                else:
                    globals()[cfg[0]] = int(cfg[1])
                        
        file.close()
        HX711['HX711_CAL'] = HX711_CAL

# Writing file Parameter 參數寫入
def config_save(flag):
    global HX711_CAL, HX711
    if flag == 1:
        HX711['HX711_CAL'] = HX711_CAL
            
    elif flag == 0:
        tmp_HX711_CAL = HX711_CAL
        HX711_CAL = HX711['HX711_CAL']
        
    file = open('config.cfg', 'w')
    save_cfg = ""
    for val in SAVE_CFG_ARRAY:
        if isinstance(globals()[val], int) or isinstance(globals()[val], float):
            save_cfg = save_cfg + val +"=" + str(globals()[val]) + ","

    file.write(save_cfg)
    file.close()
    if flag == 0:
        HX711_CAL = tmp_HX711_CAL

# Writing file LOG 寫入LOG
def logs_save(log_str, flag):
    global ERR_MSG
    if flag == 0:
        file = open('logs.txt', 'a')
        for element in reversed(log_str):
            save_log = ""
            for val in element:
                save_log = save_log + str(val) + ","

            file.write(save_log[:-1] +"\n") 
        file.close()
    else:
        ERR_MSG[1] = f"{log_str}"
        file = open('sys_log.txt', 'a')
        file.write(f"{flag}:{TENSION_COUNT}T/{log_str}\n")
        file.close()

# Active buzzer 有源蜂鳴器
def beepbeep(run_time):
    if BZ_SW == 1:
        BEEP.on()
        time.sleep(run_time)
        BEEP.off()
    else:
        time.sleep(run_time)

# Tension display 張力顯示
def tension_info(tension, flag):
    if tension is None:
        tension = TENSION_MON

    if flag == 1:
        if LB_KG_SELECT == 0:
            lcd_putstr("{: >4.1f}".format(round(tension[0] * 0.00220462, 1)), 9, 0, 4)
        elif LB_KG_SELECT == 1:
            lcd_putstr("{: >4.1f}".format(round(tension[0] / 1000, 1)), 9, 1, 4)
        
        tension_diff = tension[0] - tension[1]
        if tension_diff < 0:
            ts_str = '-'
        else:
            ts_str = '+'
        
        lcd_putstr(ts_str, 19, 3, 1)
    elif flag == 3:
        lcd_putstr("      ", 14, 3, 6)
        if LB_KG_SELECT == 0:
            lcd_putstr("{: >4.1f}".format(tension * 0.0022), 9, 0, 4)
        elif LB_KG_SELECT == 1:
            lcd_putstr("{: >4.1f}".format(tension / 1000), 9, 1, 4)
    else:
        lcd_putstr("{: >4.1f}".format(tension * 0.0022), 9, 0, 4)
        lcd_putstr("{: >4.1f}".format(tension / 1000), 9, 1, 4)
        if flag == 0:
            lcd_putstr("{: >5d}G".format(tension), 14, 3, 6)
        elif flag == 2:
            lcd_putstr("{: >5d}R".format(RT_MODE), 14, 3, 6)

# Stepper motor operation 步進馬達作動
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

# Increase in tension 張力增加
def forward(delay, steps, check, init):
    global MOTOR_ON, MOTOR_STP, RT_MODE
    tennis_g = 453 * EXTRA_CONFIG['TENNIS']
    delay_us_value = EXTRA_CONFIG["MOTOR_DELAY_US"]
    LED_GREEN.off()
    MOTOR_ON = 1
    set_direction(False)
    for i in range(0, steps):
        start_time = time.ticks_us()
        if check == 1:
            # Reached the specified tension 到達指定張力
            if MOTOR_STP == 1:
                MOTOR_ON = 0
                MOTOR_STP = 0
                return i
            
            # Exit button 離開按鍵
            if button_list('BUTTON_EXIT'):
                head_reset(None)
                MOTOR_ON = 0
                MOTOR_STP = 0
                logs_save("Abort BUTTON_EXIT", "forward()")
                return "Abort"
            
            # Tension sensor anomaly or no string (tension less than 5 lb after ABORT_LM) 張力傳感器異常、無夾線(行程已過ABORT_LM時張力小於5磅)
            if i > ABORT_LM and TENSION_MON < 2267 and RT_MODE == 0:
                head_reset(None)
                MOTOR_ON = 0
                MOTOR_STP = 0
                logs_save("No String?", "forward()")
                return "No String?"
            
            # Tension exceeds negative 5 pounds during stringing (Is the YZC-133 installed upside down?) 張緊時張力超過負5磅(YZC-133裝反?)
            if TENSION_MON < -2267:
                head_reset(None)
                MOTOR_ON = 0
                MOTOR_STP = 0
                logs_save("YZC-133 Reversed?", "forward()")
                return "YZC-133 Reversed?"
        
        # Exceeding the rear limit switch 超過後限位SW
        if MOTOR_SW_REAR.value() == EXTRA_CONFIG["PRESSED_STATE"] or i > MOTOR_MAX_STEPS:
            head_reset(None)
            if init:
                return i
                
            MOTOR_ON = 0
            MOTOR_STP = 0
            RT_MODE = 0
            logs_save(f"Over Limits {i}", "forward()")
            return f"Over Limits {i}"
        
        # Exceeding the maximum specified tension 超過最大指定張力
        if ABORT_GRAM < TENSION_MON:
            head_reset(None)
            MOTOR_ON = 0
            MOTOR_STP = 0
            RT_MODE = 0
            logs_save(f"ABORT GRAM/{ABORT_GRAM}/{TENSION_MON}", "forward()")
            return "ABORT GRAM"
        
        if i < 30 or tennis_g < TENSION_MON:
            time.sleep_us(EXTRA_CONFIG["MOTOR_SPEED_V3"])
        else:
            elapsed_time = time.ticks_diff(time.ticks_us(), start_time)
            usleep_time = max(delay - elapsed_time, 0)
            time.sleep_us(usleep_time)
        
        step_once(delay)

# Tension decrease 張力減少
def backward(delay, steps, check):
    global MOTOR_STEPS
    LED_GREEN.off()
    set_direction(True)
    for i in range(0, steps):
        start_time = time.ticks_us()
        if check == 1:
            if MOTOR_SW_FRONT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                time.sleep(0.2)
                forward(int(EXTRA_CONFIG["MOTOR_SPEED_V1"] * (11 - MOTOR_SPEED_LV) / 2), MOTOR_RS_STEPS, 0, 0)
                return 0 
        
        if i < 30:
            time.sleep_us(EXTRA_CONFIG["MOTOR_SPEED_V3"])
        else:
            elapsed_time = time.ticks_diff(time.ticks_us(), start_time)
            usleep_time = max(delay - elapsed_time, 0)
            time.sleep_us(usleep_time)
        
        step_once(delay)

# Bead clip head Reset 珠夾頭復位
def head_reset(step):
    global HEAD_RESET_COUNT
    LED_YELLOW.on()
    time.sleep(0.2)
    if HEAD_RESET_COUNT == 99:
        backward(EXTRA_CONFIG["MOTOR_SPEED_V1"], MOTOR_MAX_STEPS, 1)
        logs_save("head_reset", "head_reset()")
        HEAD_RESET_COUNT = 0
    elif step and EXTRA_CONFIG["HEAD_RESET"] == 1:
        backward(EXTRA_CONFIG["MOTOR_SPEED_V1"], step, 1)
        HEAD_RESET_COUNT = HEAD_RESET_COUNT + 1
        if abs(TENSION_MON) > 100:
            backward(EXTRA_CONFIG["MOTOR_SPEED_V1"], MOTOR_MAX_STEPS, 1)
            logs_save(f"head_reset_step_err:{TENSION_MON}G", "head_reset()")
            HEAD_RESET_COUNT = 0
    else:
        backward(EXTRA_CONFIG["MOTOR_SPEED_V1"], MOTOR_MAX_STEPS, 1)
        HEAD_RESET_COUNT = HEAD_RESET_COUNT + 1
    
    beepbeep(0.3)
    LED_YELLOW.off()
    LED_GREEN.on()

# LCD PUTSTR
def lcd_putstr(text, x, y, length):
    text = text[:length]
    text = f'{text :{" "}<{length}}'
    LCD.move_to(x, y)
    LCD.putstr(text)

# Button detection 按鈕偵測
def button_list(key):
    global BUTTON_LIST
    if BUTTON_LIST[key]:
        BUTTON_LIST[key] = 0
        return True
    else:
        return False

# errno check
def handle_error(e, func):
    global ERR_MSG
    ERR_MSG[0] = f"{e}/MEM:{gc.mem_free()} bytes"   
    logs_save(ERR_MSG[0], func)
    with open("sys_log.txt", "a") as f:
        sys.print_exception(e, f)

# Second core 第二核心
def tension_monitoring():
    try:
        global TENSION_MON, MOTOR_STP, HX711, BUTTON_LIST, ERR_MSG
        # HX711 zeroing 歸零 HX711
        v0_arr = []
        t0 = time.ticks_ms()
        while True:
            if val := hx.get_value_noblock():
                HX711["V0"].append(val)
                if (time.ticks_ms() - t0) > 1000:
                    v0_arr = sorted(HX711["V0"])
                    HX711["HX711_V0"] = v0_arr[int((len(v0_arr)/2))]
                    HX711["DIFF"] = v0_arr[-1] - v0_arr[0]
                    HX711["RATE"] = len(v0_arr)
                    HX711["CP_HZ"] = round(1 / HX711["RATE"], 3)
                    break
        
        while True:
            # Tension monitoring 張力監控
            if val := hx.get_value_noblock():
                TENSION_MON = int((val-(HX711["HX711_V0"]))/100*(HX711_CAL/20))
                HX711["HX711_VAL"] = val
                if MOTOR_ON == 1:
                    if LB_CONV_G < (TENSION_MON * CORR_COEF):
                        MOTOR_STP = 1
            
            # Button detection 按鍵偵測
            for key in BUTTON_LIST:
                if globals()[key].value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    BUTTON_LIST[key] = time.ticks_ms()
                elif BUTTON_LIST[key]:
                    if (time.ticks_ms() - BUTTON_LIST[key]) > BUTTON_CLICK_MS:
                        BUTTON_LIST[key] = 0
    
    except Exception as e:
        handle_error(e, "tension_monitoring()")

def lb_kg_select():
    global TS_ARR
    if LB_KG_SELECT == 0:
        TS_ARR = TS_LB_ARR + TS_KT + TS_PS_ARR
    else:
        TS_ARR = TS_KG_ARR + TS_KT + TS_PS_ARR

def sys_logs_show():
    lcd_putstr("=PicoBETH= SYSLOG", 0, 3, I2C_NUM_COLS)
    lines = []
    filename = 'sys_log.txt'
    if filename in os.listdir():
        with open(filename, 'r') as file:
            for line in file:
                lines.append(line)
                if len(lines) > 50:
                    lines.pop(0)
    
        lens = len(lines)
        i = 0
        while True:
            lcd_putstr("{:02}".format(i), 18, 3, 2)
            str_list = [lines[(lens - 1 - i)][j:j+19] for j in range(0, 57, 19)]
            lcd_putstr(str_list[0], 0, 0, I2C_NUM_COLS)
            lcd_putstr(str_list[1], 0, 1, I2C_NUM_COLS)
            lcd_putstr(str_list[2], 0, 2, I2C_NUM_COLS)
            beepbeep(0.3)
            while True:
                if BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    i = max(i - 1, 0)
                    break
                
                if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    i = min(i + 1, lens)
                    break
    else:
        lcd_putstr("No log file found.", 0, 0, I2C_NUM_COLS)
        lcd_putstr("Press EXIT Restart.", 0, 1, I2C_NUM_COLS)
        while True:
            if BUTTON_EXIT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                machine.reset()

# Boot initialization 開機初始化
def init():
    try:
        global LB_CONV_G, TS_ARR, ERR_MSG, ABORT_LM, MOTOR_RS_STEPS, MOTOR_MAX_STEPS, BOOT_COUNT, ABORT_GRAM, BZ_SW, RT_MODE, MOTOR_SPEED_RATIO, MOTOR_SPEED_LV, LB_MAX, DEFAULT_LB, HX711_CAL, HX711_V0, LOAD_CELL_KG
        beta = ""
        if VERSION[-1].isalpha():
            beta = "(BETA)"
        logs_save("------", "init()PowerOn")        
        logs_save(f"VER:{VERSION}/DATE:{VERDATE}", "init()")
        lcd_putstr(" ==== PicoBETH ==== ", 0, 0, I2C_NUM_COLS)
        lcd_putstr(f"Ver : {VERSION}{beta}", 0, 1, I2C_NUM_COLS)
        lcd_putstr(f"Date: {VERDATE}", 0, 2, I2C_NUM_COLS)
        lcd_putstr("Ghub: 206cc/PicoBETH", 0, 3, I2C_NUM_COLS)
        time.sleep(1)
        lcd_putstr("", 0, 3, I2C_NUM_COLS)
        boot_mode = 0
        for i in range(20):
            time.sleep(0.1)

            # HW Test Mode
            if BUTTON_SETTING.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                boot_mode = 1

            # Factory Settings Mode
            if BUTTON_EXIT.value() == EXTRA_CONFIG["PRESSED_STATE"]:            
                boot_mode = 2

            # RT Mode
            if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                boot_mode = 3

            # OTA Update Mode
            if BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                boot_mode = 4

            # Sys Logs Mode
            if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                boot_mode = 5

            # Engineering Mode
            if BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                boot_mode = 6

            if boot_mode == 0:
                lcd_putstr(".", i, 3, 1)
            else:
                lcd_putstr(f"{boot_mode}", i, 3, 1)
        
        time.sleep(2)
        LCD.clear()
        
        # Update mode
        if boot_mode == 4:
            with open("ota", "w") as f:
                pass
                
            machine.reset()
            
        # HW Test Mode
        if boot_mode == 1:
            lcd_putstr("HW Testing MODE", 0, 0, I2C_NUM_COLS)
            time.sleep(2)
            
        # Factory Settings Mode
        if boot_mode == 2:
            lcd_putstr("Factory Settings", 0, 0, I2C_NUM_COLS)
            lcd_putstr("MODE", 0, 1, I2C_NUM_COLS)
            time.sleep(2)
            
        # RT Mode
        if boot_mode == 3:
            lcd_putstr("Reliability Testing", 0, 0, I2C_NUM_COLS)
            lcd_putstr("MODE", 0, 1, I2C_NUM_COLS)
            time.sleep(2)
            
        # Sys Logs Mode
        if boot_mode == 5:
            lcd_putstr("Display System Logs", 0, 0, I2C_NUM_COLS)
            lcd_putstr("MODE", 0, 1, I2C_NUM_COLS)
            time.sleep(2)
            sys_logs_show()
        
        test_MOTOR_SPEED_LV = MOTOR_SPEED_LV
        config_read()
        DEFAULT_LB = min(DEFAULT_LB, LB_MAX)
        ori_BZ_SW = BZ_SW
        ori_MOTOR_SPEED_LV = max(1, min(9, MOTOR_SPEED_LV))
        MOTOR_SPEED_LV = test_MOTOR_SPEED_LV
        BZ_SW = 1
        lb_kg_select()
        main_interface()
        lcd_putstr(f"{ori_MOTOR_SPEED_LV}", 10, 3, 1)
        LB_CONV_G = min(int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100)), int(LB_MAX * 453.59237))
        lcd_putstr("Tension monitoring...", 0, 2, I2C_NUM_COLS)
        _thread.start_new_thread(tension_monitoring, ())
 
        # 檢查 Load Cell 公斤數
        if LOAD_CELL_KG not in (20, 50):
            ERR_MSG[0] = f"ERR: Load Cell {LOAD_CELL_KG}"
            logs_save(ERR_MSG[0], "init()")
        
        # Waiting for HX711 zeroing 等待 HX711 歸零
        i = 0
        while True:
            if HX711["RATE"] != 0:
                logs_save(f"HX_Thread_Init_Time:{i/10}", "init()")
                break
            
            if i > 20:
                ERR_MSG[0] = "ERR: HX711@Zero #1"
                logs_save(ERR_MSG[0], "init()")
                break
            
            i = i + 1
            time.sleep(0.1)

        # Sampling error less than 0.01 grams (HX711 damaged?) 取樣誤差過小於 0.01公克(HX711損壞?)
        if HX711["DIFF"] < 10:
            ERR_MSG[0] = "ERR: HX711@Zero #2"
            logs_save(ERR_MSG[0], "init()")

        # Check if HX711 RATE exceeds 75Hz 檢查 HX711 RATE 是否超過 75Hz
        if HX711["RATE"] < 75:
            ERR_MSG[0] = f"ERR: HX711@{HX711['RATE']}Hz"
            logs_save(ERR_MSG[0], "init()")

        # Sampling error exceeds HX711_DIFRT gram or is less than 0.2G. (unstable) 取樣誤差過大超過 HX711_DIFRT 或小於 0.2公克(不穩定)
        if HX711["DIFF"] > (HX711_DIFRT * 1000) or HX711["DIFF"] < 200:
            ERR_MSG[0] = f"ERR: HX_DIFRT@{round(HX711['DIFF']/1000, 1)}G"
            logs_save(ERR_MSG[0], "init()")

        # Standby error exceeds 5 grams (unstable) 待機誤差過大超過 5公克(不穩定)
        if abs(TENSION_MON) > 5:
            ERR_MSG[0] = f"ERR: HX711@{abs(TENSION_MON)}G #2"
            logs_save(ERR_MSG[0], "init()")
        
        # HX711 log
        hx_diff_g = int(abs(HX711_V0 - HX711["HX711_V0"]) / 100 * (HX711_CAL / 20))
        logs_save(f"RV0:{HX711_V0}/V0:{HX711['HX711_V0']}/DIFF:{HX711['DIFF']}/RATE:{HX711['RATE']}/DIFF_G:{hx_diff_g}/HX711_CAL:{HX711_CAL}", "init()HX711")

        # Check if any button is in the unpressed state 檢查是否有按鍵處於未按下狀態
        chk_sw = check_sw()
        if chk_sw:
            ERR_MSG[0] = f"ERR: {chk_sw}"
            logs_save(ERR_MSG[0], "init()")

        if ERR_MSG[0] == "": 
            # Engineering Mode
            if boot_mode == 6:
                lcd_putstr("Engineering Mode", 0, 0, I2C_NUM_COLS)
                engineering_mode(0)
                main_interface()
            
            if boot_mode == 2:
                lcd_putstr("Factory Reset?", 0, 2, I2C_NUM_COLS)
                lcd_putstr("[UP=Y DOWN=N]", 0, 3, I2C_NUM_COLS)
                logs_save("Factory Reset Check", "init()")
                while True:
                    if button_list('BUTTON_UP'):
                        if 'config.cfg' in os.listdir():
                            os.rename('config.cfg', 'config.cfg'+'.bak')
                            logs_save("Config Backup", "init()")
                        
                        if 'logs.txt' in os.listdir():
                            os.remove('logs.txt')
                            logs_save("Logs Remove", "init()")
                        
                        machine.reset()
                    elif button_list('BUTTON_DOWN'):
                        main_interface()
                        logs_save("Factory Reset Cancel", "init()")
                        break
            elif button_list('BUTTON_SETTING') or boot_mode == 1:
                logs_save("HW TEST", "init()")
                hw_test(1, ori_BZ_SW)
            elif button_list('BUTTON_UP') or boot_mode == 3:
                logs_save("RT TEST", "init()")
                RT_MODE = 1
            
            if FIRST_TEST == 1:
                logs_save("HW TEST FIRST", "init()")
                hw_test(0, ori_BZ_SW)
            
            time.sleep(3)
            logs_save("head_reset#0", "init()")
            lcd_putstr("Checking motor...", 0, 2, I2C_NUM_COLS)
            head_reset(None)
            logs_save("MOTOR_MAX_STEPS#1", "init()")
            t0 = time.ticks_ms()
            MOTOR_MAX_STEPS = forward(int(EXTRA_CONFIG["MOTOR_SPEED_V1"] * (11 - MOTOR_SPEED_LV) / 2), MOTOR_MAX_STEPS, 0, 1)
            if not isinstance(MOTOR_MAX_STEPS, int):
                ERR_MSG[0] = MOTOR_MAX_STEPS
                logs_save(ERR_MSG[0], "init()")
            else:
                motor_time = time.ticks_ms() - t0
                logs_save("MOTOR_MAX_STEPS#2", "init()")
                MOTOR_SPEED_RATIO = round(MOTOR_MAX_STEPS/motor_time, 2)
                logs_save(f"STEPS:{MOTOR_MAX_STEPS}/TIME:{motor_time}/MR:{MOTOR_SPEED_RATIO}/MS:{EXTRA_CONFIG['MOTOR_SPEED_V1']}/LV:{MOTOR_SPEED_LV}", "init()MOTOR")
                if MOTOR_MAX_STEPS < 5000:
                    ERR_MSG[0] = "ERR: MAX STEPS"
                    logs_save(ERR_MSG[0], "init()")
                else:
                    MOTOR_RS_STEPS = int(MOTOR_MAX_STEPS / 20)
                    ABORT_LM = int(int(MOTOR_MAX_STEPS) * 0.4)
                    BZ_SW = ori_BZ_SW
                    head_reset(None)
                    MOTOR_SPEED_LV = ori_MOTOR_SPEED_LV
                    if DEFAULT_LB > LB_MAX:
                        DEFAULT_LB = LB_MAX
                    ABORT_GRAM = (LB_MAX + 5) * 454
                    
                    LED_RED.off()
                    main_interface()
                    check_hx_calibration(1)
                    beepbeep(0.3)
                    BOOT_COUNT = BOOT_COUNT + 1
                    if ERR_MSG[0] == "":
                        config_save(0)

    except Exception as e:
        handle_error(e, "init()")

# Start increasing tension 開始增加張力
def start_tensioning():
    try:
        global MOTOR_ON, MOTOR_STP, TENSION_COUNT, LOGS, CORR_COEF, KNOT_FLAG, LB_CONV_G, RT_MODE, ERR_MSG
        LCD.hide_cursor()
        lcd_putstr("Tensioning", 0, 2, I2C_NUM_COLS)
        lcd_putstr("     ", 15, 1, 5)
        if KNOT_FLAG == 0:
            LB_CONV_G = min(int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100)), int(LB_MAX * 453.59237))
        else:
            LB_CONV_G = min(int((DEFAULT_LB * 453.59237) * ((KNOT + 100) / 100)), int(LB_MAX * 453.59237))
        
        if TIMER:
            timer_diff = time.time() - TIMER
        else:
            timer_diff = 0
            
        rel = forward(int(EXTRA_CONFIG["MOTOR_SPEED_V1"] * (11 - MOTOR_SPEED_LV) / 2), MOTOR_MAX_STEPS, 1, 0)
        if isinstance(rel, int):
            head_pos = rel
        else:
            RT_MODE = 0
            lcd_putstr(f"{rel}", 0, 2, I2C_NUM_COLS)
            logs_save(f"ts_err#0/{rel}", "start_tensioning()")
            return 0       

        if LB_KG_SELECT == 0:
            lcd_putstr("--.-", 9, 1, 4)
        else:
            lcd_putstr("--.-", 9, 0, 4)
        
        MOTOR_ON = 0
        abort_flag = 0
        count_add = 0
        count_sub = 0
        ts_phase = 0
        cc_count_add = 0
        cc_add_flag = 0
        log_lb_max = 0
        manual_flag = 1
        mt_ts = 0
        temp_LB_CONV_G = LB_CONV_G
        LED_YELLOW.off ()
        t0 = time.time()
        # Reached specified tension 到達指定張力
        while True:
            tension = TENSION_MON
            cp_phase = 0
            ft = 1
            # IAAA
            if ts_phase == 0:
                if abs(temp_LB_CONV_G - tension) < EXTRA_CONFIG["CP_FAST"]:
                    beepbeep(0.3)
                    log_lb_max = temp_LB_CONV_G
                    tension_info(log_lb_max, 3)
                    lcd_putstr("Target Tension", 0, 2, I2C_NUM_COLS)
                    lcd_putstr("S:   ", 15, 1, 5)
                    if KNOT_FLAG == 0:
                        temp_LB_CONV_G = int(DEFAULT_LB * 453.59237)
                        
                    t0 = time.time()
                    if PRE_STRECH == 0:
                        ts_phase = 2
                        LED_YELLOW.on()
                        if CP_SW == 1:
                            manual_flag = 1
                        else:
                            manual_flag = 0
                    else:
                        ts_phase = 1
                        
            elif ts_phase == 1:
                if (abs(temp_LB_CONV_G - tension) < (EXTRA_CONFIG["CP_SLOW"] * 2)) and (time.time() - t0) >= 1:
                    beepbeep(0.1)
                    t0 = time.time()
                    ts_phase = 2
                    LED_YELLOW.on()
                    if CP_SW == 1:
                        manual_flag = 1
                    else:
                        manual_flag = 0
            
            # Constant-pull increase 恆拉增加張力
            if (temp_LB_CONV_G + 5) > tension and (manual_flag == 1 or ts_phase == 0):
                diff_g = temp_LB_CONV_G - tension
                if diff_g > 906:
                    cp_phase = 2
                    if cc_add_flag == 0:
                        cc_count_add = cc_count_add + 1000
                elif diff_g < (EXTRA_CONFIG["CP_FAST"] * 2) and ts_phase == 2:
                    cp_phase = 0
                    cc_add_flag = 1
                    if diff_g > 10:
                        if PRE_STRECH == 0 and diff_g > 50:
                            cp_phase = 1
                        else:
                            ft = 2
                else:
                    ft = 2
                    cp_phase = 1
                    if cc_add_flag == 0:
                        cc_count_add = cc_count_add + 1
                    
                    if ts_phase == 0:
                        count_add = count_add + 1
                
                abort_flag = forward(EXTRA_CONFIG["MOTOR_SPEED_V2"], ft, 0 ,0)
                head_pos = head_pos + ft
                
            # Constant-pull decrease 恆拉減少張力
            if (temp_LB_CONV_G + (EXTRA_CONFIG["CP_SLOW"] * 2)) < tension and (manual_flag == 1 or ts_phase == 0):
                diff_g =  tension - temp_LB_CONV_G
                if diff_g < EXTRA_CONFIG["CP_FAST"] * (5 - (PRE_STRECH / 10)) and ts_phase == 2:
                    cp_phase = 0
                else:
                    cp_phase = 1
                
                if ts_phase == 0:
                    count_sub = count_sub + 1
                    
                abort_flag = backward(EXTRA_CONFIG["MOTOR_SPEED_V2"], ft, 0)
                head_pos = head_pos - ft
                
            # Manually increase tension 手動增加張力
            if button_list('BUTTON_UP') and RT_MODE == 0 and (time.ticks_ms() - mt_ts) > 250:
                mt_ts = time.ticks_ms()
                if LB_KG_SELECT == 1:
                    temp_lb = (int(temp_LB_CONV_G / 499) + 1) / 2
                    temp_LB_CONV_G = min(int(temp_lb * 1000), int(LB_MAX * 453.59237))
                else:
                    temp_lb = (int(temp_LB_CONV_G / 226) + 1) / 2
                    temp_LB_CONV_G = min(int(temp_lb * 453.59237), int(LB_MAX * 453.59237))
                
                lcd_putstr("{: >4.1f}".format(temp_LB_CONV_G / 453.592), 4, 0, 4)
                lcd_putstr("{: >4.1f}".format(temp_LB_CONV_G / 1000), 4, 1, 4)
                mt_ts = time.ticks_ms()
                time.sleep(0.2)
                beepbeep(0.1)
                    
            # Manually decrease tension 手動減少張力
            if button_list('BUTTON_DOWN') and RT_MODE == 0 and (time.ticks_ms() - mt_ts) > 250:
                mt_ts = time.ticks_ms()
                if LB_KG_SELECT == 1: 
                    temp_lb = (int(temp_LB_CONV_G / 499) - 1) / 2
                    temp_LB_CONV_G = min(int(temp_lb * 1000), int(LB_MAX * 453.59237))
                else:
                    temp_lb = (int(temp_LB_CONV_G / 226) - 1) / 2
                    temp_LB_CONV_G = min(int(temp_lb * 453), int(LB_MAX * 453.59237))
                
                lcd_putstr("{: >4.1f}".format(temp_LB_CONV_G / 453.592), 4, 0, 4)
                lcd_putstr("{: >4.1f}".format(temp_LB_CONV_G / 1000), 4, 1, 4)
                time.sleep(0.2)
                beepbeep(0.1)
                    
            # Manual & automatic adjustment toggle 手動&自動微調切換
            if button_list('BUTTON_SETTING') and RT_MODE == 0 and (time.ticks_ms() - mt_ts) > 500:
                mt_ts = time.ticks_ms()
                if manual_flag == 0:
                    manual_flag = 1
                else:
                    manual_flag = 0
                        
                lcd_putstr(OPTIONS_DICT['MA_ARR'][manual_flag], 12, 3, 1)
                beepbeep(0.1)
            
            # String Broken (suddenly less than 5 lb) 斷線(突然小於5磅)
            if tension < 2267:
                lcd_putstr(OPTIONS_DICT['MA_ARR'][CP_SW], 12, 3, 1)
                lcd_putstr("Resetting...", 0, 2, I2C_NUM_COLS)
                head_reset(None)
                lcd_putstr("String Broken?", 0, 2, I2C_NUM_COLS)
                lcd_putstr("     ", 15, 1, 5)
                MOTOR_STP = 0
                RT_MODE = 0
                logs_save("ts_err#3", "start_tensioning()")
                return 0
            
            # Exit & head button 取消與珠夾頭按鈕
            if JPLIEW or RT_MODE != 0:
                button_head_pressed = False
            else:
                button_head_pressed = button_list('BUTTON_HEAD')
            button_exit_pressed = button_list('BUTTON_EXIT')
            rt_mode_time = time.time() - t0
            rt_mode_pressed = (ts_phase == 2 and rt_mode_time >= 3 and RT_MODE != 0)
            if button_head_pressed or button_exit_pressed or rt_mode_pressed:
                #CC參數自動調整
                cc_add_sub = 0
                if EXTRA_CONFIG["CORR_COEF_AUTO"] == 1:
                    if cc_count_add >= 1000 and CORR_COEF >= 1.1:
                        CORR_COEF = CORR_COEF - 0.05
                    elif cc_count_add > 20:
                        CORR_COEF = CORR_COEF - 0.01
                    elif cc_count_add == 0 and CORR_COEF <= 1.0:
                        CORR_COEF = CORR_COEF + 0.03
                    elif cc_count_add < 10:
                        CORR_COEF = CORR_COEF + 0.01
                    
                    CORR_COEF = max(0.95, min(CORR_COEF, 1.2))
                
                log_s = time.time() - t0
                lcd_putstr(OPTIONS_DICT['MA_ARR'][CP_SW], 12, 3, 1)
                lcd_putstr("Resetting...", 0, 2, I2C_NUM_COLS)
                lcd_putstr("{: >4.1f}".format(DEFAULT_LB), 4, 0, 4)
                lcd_putstr("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
                head_reset(head_pos)
                lcd_putstr("Ready", 0, 2, I2C_NUM_COLS)
                lcd_putstr("     ", 15, 1, 5)
                MOTOR_STP = 0
                if ts_phase == 2:
                    TENSION_COUNT = TENSION_COUNT + 1
                    # Writing to LOG 寫入LOG
                    LOGS.insert(0, [TENSION_COUNT, timer_diff, LB_KG_SELECT, DEFAULT_LB, log_lb_max, PRE_STRECH, log_s, count_add, count_sub, CORR_COEF, HX711_CAL, KNOT_FLAG, KNOT])
                    logs_save([LOGS[0]], 0)
                    if len(LOGS) > EXTRA_CONFIG["LOG_MAX"]:
                        LOGS = LOGS[:EXTRA_CONFIG["LOG_MAX"]]
                        
                    if KNOT_FLAG == 1:
                        KNOT_FLAG = 0
                        lcd_putstr(OPTIONS_DICT['PSKT_ARR'][KNOT_FLAG], 14, 0, 2)
                        lcd_putstr("{: >2d}".format(PRE_STRECH), 17, 0, 2)
                    
                    if TENSION_COUNT % EXTRA_CONFIG["LOG_MAX"] == 0:
                        logs_cleanup()
                    
                    config_save(0)
                else:
                    logs_save(f"ts_err#2/{int(button_head_pressed)}/{int(button_exit_pressed)}/{int(rt_mode_pressed)}/{ts_phase}/{rt_mode_time}/{RT_MODE}", "start_tensioning()")
                return 0
            
            if abort_flag == 1:
                logs_save("ts_err#1", "start_tensioning()")
                return 0  
            
            # Slow Constant-Pull 慢速恆拉
            if cp_phase == 0: 
                tension_info([tension, temp_LB_CONV_G], 1)
                if ts_phase == 2:
                    s_time = time.time()-t0
                    if s_time > 99:
                        s_time = "--"
                    else:
                        s_time = "{:>2d}".format(s_time)
                    lcd_putstr(s_time, 18, 1, 2)
                else:
                    lcd_putstr("  ", 18, 1, 2)
            # Fast Constant-Pull 快速恆拉
            elif cp_phase == 1:
                time.sleep(HX711["CP_HZ"])

    except Exception as e:
        handle_error(e, "start_tensioning()")

# Main screen 主畫面
def setting_ts():
    try:
        global DEFAULT_LB, PRE_STRECH, LB_CONV_G, CURSOR_XY_TS_TEMP, KNOT_FLAG, KNOT
        if KNOT_FLAG == 1:
            ps_kt_show = DEFAULT_LB * ((KNOT + 100) / 100)
        else:
            ps_kt_show = DEFAULT_LB * ((PRE_STRECH + 100) / 100)
                    
        lcd_putstr("{: >4.1f}".format(ps_kt_show), 9, 0, 4)
        lcd_putstr("{: >4.1f}".format(ps_kt_show * 0.45359237), 9, 1, 4)
        last_set_time = time.ticks_ms()
        set_count = len(TS_ARR)
        i = CURSOR_XY_TS_TEMP
        cursor_xy = TS_ARR[i][0], TS_ARR[i][1]
        LCD.move_to(TS_ARR[i][0], TS_ARR[i][1])
        LCD.blink_cursor_on()
        ps_kt_tmp = 0
        if KNOT_FLAG == 0:
            ps_kt_tmp = PRE_STRECH
        else:
            ps_kt_tmp = KNOT
        
        beepbeep(0.04)
        while True:
            # Action of pressing the up or down button 按下上下鍵動作
            if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                LCD.show_cursor()
                LCD.blink_cursor_on()
                kg = round(DEFAULT_LB * 0.45359237, 1)
                # LB 10-digit setting 設定 LB十位數
                if cursor_xy == (4, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        DEFAULT_LB = DEFAULT_LB + 10
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        DEFAULT_LB = DEFAULT_LB - 10
                
                # LB single-digit setting 設定 LB個位數
                elif cursor_xy == (5, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        DEFAULT_LB = DEFAULT_LB + 1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        DEFAULT_LB = DEFAULT_LB - 1
                
                # LB decimal setting 設定 LB小數
                elif cursor_xy == (7, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        DEFAULT_LB = DEFAULT_LB + 0.1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        DEFAULT_LB = DEFAULT_LB - 0.1
                        
                # KG 10-digit setting 設定 KG十位數
                elif cursor_xy == (4, 1):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        kg = kg + 10
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        kg = kg - 10
                        
                    DEFAULT_LB = round(kg * 2.20462262, 1)

                # KG single-digit setting 設定 KG個位數
                elif cursor_xy == (5, 1):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        kg = kg + 1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        kg = kg - 1
                        
                    DEFAULT_LB = round(kg * 2.20462262, 1)
                
                # KG decimal setting 設定 KG小數
                elif cursor_xy == (7, 1):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        kg = kg + 0.1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        kg = kg - 0.1
                        
                    DEFAULT_LB = round(kg * 2.20462262, 1)
                
                # Pre-Stretch or knot 10-digit setting 設定預拉或打結十位數
                elif cursor_xy == (17, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        ps_kt_tmp = ps_kt_tmp + 10
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        ps_kt_tmp = ps_kt_tmp - 10
                    
                # Pre-Stretch or knot single-digit setting 設定預拉或打結個位數
                elif cursor_xy == (18, 0):
                    ps_tmp = 5                        
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        if ps_kt_tmp < 5:
                            ps_tmp = 1
                            
                        ps_kt_tmp = ps_kt_tmp + ps_tmp
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        if ps_kt_tmp <= 5:
                            ps_tmp = 1
                            
                        ps_kt_tmp = ps_kt_tmp - ps_tmp
                
                # Pre-Stretch or knot tying switch 預拉或打結切換
                elif cursor_xy == (14, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        if KNOT_FLAG == 1:
                            KNOT_FLAG = 0
                            ps_kt_tmp = PRE_STRECH
                        else:
                            KNOT_FLAG = 1
                            ps_kt_tmp = KNOT
                            
                        lcd_putstr(OPTIONS_DICT['PSKT_ARR'][KNOT_FLAG], 14, 0, 2)
                        lcd_putstr("{: >2d}".format(ps_kt_tmp), 17, 0, 2)
                
                DEFAULT_LB = max(LB_MIN, min(LB_MAX, DEFAULT_LB))
                
                if KNOT_FLAG == 1:
                    KNOT = ps_kt_tmp
                    KNOT = max(KNOT_RANG[0], min(KNOT_RANG[1], KNOT))
                    ps_kt_tmp = KNOT
                    lcd_putstr("{: >2d}".format(KNOT), 17, 0, 2)
                    ps_kt_show = DEFAULT_LB * ((KNOT + 100) / 100)
                else:
                    PRE_STRECH = ps_kt_tmp
                    PRE_STRECH = max(0, min(EXTRA_CONFIG["PS_MAX"], PRE_STRECH))
                    ps_kt_tmp = PRE_STRECH
                    lcd_putstr("{: >2d}".format(PRE_STRECH), 17, 0, 2)
                    ps_kt_show = DEFAULT_LB * ((PRE_STRECH + 100) / 100)
                
                LCD.blink_cursor_off()
                LCD.hide_cursor()
                lcd_putstr("{: >4.1f}".format(min(ps_kt_show, LB_MAX)), 9, 0, 4)
                lcd_putstr("{: >4.1f}".format(min(ps_kt_show * 0.45359237, LB_MAX * 0.45359237)), 9, 1, 4)
                lcd_putstr("{:.1f}".format(DEFAULT_LB), 4, 0, 4)
                lcd_putstr("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
                LCD.move_to(TS_ARR[i][0],TS_ARR[i][1])
                LCD.show_cursor()
                LCD.blink_cursor_on()
                last_set_time = time.ticks_ms()
                beepbeep(0.1)
                time.sleep(0.1)

            # Action of pressing the left or right button 按下左右鍵動作
            if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                LCD.hide_cursor()
                LCD.blink_cursor_on()
                if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    if (i+1) < set_count:
                        i = i + 1
                    else:
                        i = 0
                elif BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    if (i-1) >= 0:
                        i = i - 1
                    else:
                        i = set_count - 1
                
                CURSOR_XY_TS_TEMP = i
                LCD.move_to(TS_ARR[i][0], TS_ARR[i][1])
                cursor_xy = TS_ARR[i][0], TS_ARR[i][1]
                last_set_time = time.ticks_ms()
                beepbeep(0.1)
                time.sleep(0.1)

            # Action of pressing the exit button 按下離開鍵動作
            if button_list('BUTTON_EXIT') or ((time.ticks_ms() - last_set_time) > (1.8 * 1000)):
                config_save(0)
                LCD.blink_cursor_off()
                LCD.hide_cursor()
                time.sleep(0.1)
                beepbeep(0.04)
                return 0
            
    except Exception as e:
        handle_error(e, "setting_ts()")

# Settings screen 設定頁面
def setting():
    try:
        global CURSOR_XY_TEMP, CORR_COEF, HX711_CAL, LB_KG_SELECT, CURSOR_XY_TS_TEMP, CP_SW, BZ_SW, FIRST_TEST, HX711_V0, MOTOR_SPEED_LV
        if HX711['HX711_CAL'] != HX711_CAL:
            save_flag = 1
            lcd_putstr("S", 19, 1, 1)
        else:
            save_flag = 0
            lcd_putstr(" ", 19, 1, 1)
        
        set_count = len(MENU_ARR)
        engineering_mode_flag = 0
        i = CURSOR_XY_TEMP
        cursor_xy = MENU_ARR[i][0], MENU_ARR[i][1]
        LCD.move_to(MENU_ARR[i][0], MENU_ARR[i][1])
        LCD.blink_cursor_on()
        time.sleep(0.1)
        beepbeep(0.1)
        while True:
            # Action of pressing the up or down button 按下上下鍵動作
            if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"] or button_list('BUTTON_SETTING'):
                LCD.hide_cursor()
                LCD.blink_cursor_off()
                flag = 0
                # System information 系統資訊
                if cursor_xy == (8, 3):
                    if BUTTON_SETTING.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        LCD.blink_cursor_off()
                        beepbeep(0.1)
                        lcd_putstr(f"SW:V{VERSION}_{VERDATE}", 0, 0, I2C_NUM_COLS)
                        lcd_putstr(f"HX:{HX711['DIFF']/1000:.1f}g/{sorted(HX711['V0'])[0]}/{HX711['RATE']}Hz", 0, 1, I2C_NUM_COLS)
                        lcd_putstr(f"MR:{MOTOR_SPEED_RATIO: >1.2f} MS:{int(EXTRA_CONFIG["MOTOR_SPEED_V1"]):02d} {BOOT_COUNT: >5d}B", 0, 2, I2C_NUM_COLS)
                        lcd_putstr(f"CC:{CORR_COEF: >1.2f}", 0, 3, 7)
                        LCD.move_to(8, 3)
                        LCD.blink_cursor_on()
                        beepbeep(0.1)
                        while True:
                            if BUTTON_EXIT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                                beepbeep(0.1)
                                setting_interface()
                                LCD.blink_cursor_on()
                                break
                            
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        engineering_mode_flag = engineering_mode_flag + 1
                        if engineering_mode_flag >= 5:
                            beepbeep(0.1)
                            engineering_mode(0)
                            beepbeep(0.1)
                            setting_interface()
                
                # LB or KG setting selection 磅、公斤設定選擇
                elif cursor_xy == (14, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        CURSOR_XY_TS_TEMP = 1
                        LB_KG_SELECT = (LB_KG_SELECT + 1) % 2
                        lcd_putstr(OPTIONS_DICT['UNIT_ARR'][LB_KG_SELECT], 14, 0, 5)
                        lb_kg_select()
                        
                # Constant-pull switch 恆拉開關
                elif cursor_xy == (4, 1):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        if CP_SW == 1:
                            CP_SW = 0
                        else:
                            CP_SW = 1
                        
                        lcd_putstr(OPTIONS_DICT['ONOFF_ARR'][CP_SW], 4, 1, 3)
                        
                # Buzzer switch 蜂鳴器開關
                elif cursor_xy == (4, 2):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        if BZ_SW == 1:
                            BZ_SW = 0
                        else:
                            BZ_SW = 1
                        
                        lcd_putstr(OPTIONS_DICT['ONOFF_ARR'][BZ_SW], 4, 2, 3)
                        
                # Bead clip head movement speed 珠夾頭速度
                elif cursor_xy == (5, 0):
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        MOTOR_SPEED_LV = MOTOR_SPEED_LV + 1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        MOTOR_SPEED_LV = MOTOR_SPEED_LV - 1

                # HX711 calibration coefficient ten-digit 校正系數十位數HX711
                elif cursor_xy == (14, 1):
                    flag = 1
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL + 10
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL - 10
                        
                # HX711 calibration coefficient single-digit 校正系數個位數HX711
                elif cursor_xy == (15, 1):
                    flag = 1
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL + 1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL - 1
                
                # HX711 calibration coefficient first decimal 校正系數第一位小數HX711
                elif cursor_xy == (17, 1):
                    flag = 1
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL + 0.1
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL - 0.1
                        
                # HX711 calibration coefficient second decimal 校正系數第二位小數HX711
                elif cursor_xy == (18, 1):
                    flag = 1
                    if BUTTON_UP.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL + 0.01
                    elif BUTTON_DOWN.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        HX711_CAL = HX711_CAL - 0.01
                        
                # HX711 tension calibration save 張力校正儲存HX711
                elif cursor_xy == (19, 1):
                    if BUTTON_SETTING.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        beepbeep(0.1)
                        HX711_V0 = HX711["HX711_V0"]
                        config_save(1)
                        lcd_putstr(" ", 19, 1, 1)
                        i = i - 1
                        save_flag = 0
                        CURSOR_XY_TEMP = i
                        cursor_xy = MENU_ARR[i][0], MENU_ARR[i][1]

                # Display LOG 顯示LOG
                elif cursor_xy == (19, 3):
                    if BUTTON_SETTING.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                        LCD.blink_cursor_off()
                        beepbeep(0.1)
                        if len(LOGS) != 0:
                            logs_idx = 0
                            LCD.hide_cursor()
                            logs_interface("init")
                            logs_interface(logs_idx)
                            LCD.blink_cursor_on()
                            log_flag = 0
                            beepbeep(0.1)
                            while True:
                                if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                                    logs_idx = (logs_idx + 1) % len(LOGS)
                                    beepbeep(0.1)
                                elif BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                                    logs_idx = logs_idx - 1
                                    if logs_idx < 0:
                                        logs_idx = len(LOGS) - 1
                                    beepbeep(0.1)
                                elif BUTTON_EXIT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                                    beepbeep(0.1)
                                    break
                                
                                if log_flag != logs_idx:
                                    logs_interface(logs_idx)
                                    beepbeep(0.1)
                                    log_flag = logs_idx
                                
                            setting_interface()
                            
                        LCD.blink_cursor_on()
                
                if flag == 1:
                    HX711_CAL = max(LOAD_CELL_KG - 10, min(LOAD_CELL_KG + 10, HX711_CAL))
                    
                    if FIRST_TEST == 2:
                        FIRST_TEST = 0
                
                    if HX711['HX711_CAL'] != HX711_CAL:
                        save_flag = 1
                        lcd_putstr("S", 19, 1, 1)
                    else:
                        save_flag = 0
                        lcd_putstr(" ", 19, 1, 1)
                
                MOTOR_SPEED_LV = max(1, min(9, MOTOR_SPEED_LV))
                lcd_putstr(f"L{MOTOR_SPEED_LV}", 4, 0, 6)
                lcd_putstr("{: >2.2f}".format(HX711_CAL), 14, 1, 5)
                LCD.move_to(MENU_ARR[i][0],MENU_ARR[i][1])
                LCD.show_cursor()
                LCD.blink_cursor_on()
                beepbeep(0.1)
                time.sleep(0.1)

            # Action of pressing the left or right button 按下左右鍵動作
            if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"] or BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                if BUTTON_RIGHT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    if (i+1) < set_count:
                        i = i + 1
                        if save_flag == 0 and (MENU_ARR[i][0], MENU_ARR[i][1]) == (19, 1):
                            i = i + 1
                    else:
                        i = 0
                elif BUTTON_LEFT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    if (i-1) >= 0:
                        i = i - 1
                        if save_flag == 0 and (MENU_ARR[i][0], MENU_ARR[i][1]) == (19, 1):
                            i = i - 1
                    else:
                        i = set_count - 1
                
                CURSOR_XY_TEMP = i
                LCD.move_to(MENU_ARR[i][0], MENU_ARR[i][1])
                cursor_xy = MENU_ARR[i][0], MENU_ARR[i][1]
                beepbeep(0.1)
                time.sleep(0.1)

            # Action of pressing the exit button 按下離開鍵動作
            if button_list('BUTTON_EXIT'):
                config_save(0)
                LCD.blink_cursor_off()
                LCD.hide_cursor()
                time.sleep(0.1)
                beepbeep(0.1)
                return 0
     
    except Exception as e:
        handle_error(e, "setting()")
            
# Settings interface 設定介面顯示
def setting_interface():
    LCD.hide_cursor()
    temp_sp = f"L{MOTOR_SPEED_LV}"
    lcd_putstr(f"SP: {temp_sp}    UN: {OPTIONS_DICT['UNIT_ARR'][LB_KG_SELECT]}", 0, 0, I2C_NUM_COLS)
    lcd_putstr(f"CP: {OPTIONS_DICT['ONOFF_ARR'][CP_SW]}   HX: {HX711_CAL: >2.2f} ", 0, 1, I2C_NUM_COLS)
    lcd_putstr(f"BZ: {OPTIONS_DICT['ONOFF_ARR'][BZ_SW]}", 0, 2, I2C_NUM_COLS)
    lcd_putstr(f"=MENU=  INFO {TENSION_COUNT: >6d}T", 0, 3, I2C_NUM_COLS)
    
# LOG interface 介面顯示LOG
def logs_interface(idx):
    LCD.hide_cursor()
    if idx=="init":
        lcd_putstr("  LOG  TIMER:   m  s", 0, 0, I2C_NUM_COLS)
        lcd_putstr("LB:    /        :  %", 0, 1, I2C_NUM_COLS)
        lcd_putstr("CP:  /  /      S:   ", 0, 2, I2C_NUM_COLS)
        lcd_putstr("CC:                T", 0, 3, I2C_NUM_COLS)
    else:
        lcd_putstr("{:0>2d}".format((idx + 1)), 0, 0, 2)
        if int(LOGS[idx][1]):

            lcd_putstr("{: >3d}".format(min(999, int(int(LOGS[idx][1]) / 60))) +"m"+ "{: >2d}".format(int(int(LOGS[idx][1]) % 60)) +"s", 13, 0, 7)
        else:
            lcd_putstr(" ------", 13, 0, 7)
            
        if int(LOGS[idx][2]) == 2:
            lcd_putstr("KG:" + "{: >4.1f}".format(float(LOGS[idx][3]) * 0.45359237), 0, 1, 7)
            lcd_putstr("{: >4.1f}".format(int(LOGS[idx][4]) * 0.001), 8, 1, 4)
        else:
            lcd_putstr("LB:" + "{: >4.1f}".format(float(LOGS[idx][3])), 0, 1, 7)
            lcd_putstr("{: >4.1f}".format(int(LOGS[idx][4]) * 0.0022046), 8, 1, 4)
        
        if int(LOGS[idx][12]) == 1:
            lcd_putstr("KT:" + "{: >2d}".format(int(LOGS[idx][13])), 14, 1, 5)
        else:
            lcd_putstr("PS:" + "{: >2d}".format(int(LOGS[idx][5])), 14, 1, 5)
            
        lcd_putstr("{: >3d}".format(int(LOGS[idx][6])), 17, 2, 3)
        lcd_putstr("{: >2d}".format(int(LOGS[idx][7])), 3, 2, 2)
        lcd_putstr("{: >2d}".format(int(LOGS[idx][8])), 6, 2, 2)
        lcd_putstr("{:02d}".format(int(LOGS[idx][11])), 9, 2, 2)
        lcd_putstr("{:.2f}".format(float(LOGS[idx][9])), 3, 3, 4)
        lcd_putstr("{: >5d}".format(int(LOGS[idx][0])), 14, 3, 5)

# Main screen 主畫面顯示
def main_interface():
    LCD.hide_cursor()
    lcd_putstr(f"LB:     /--.- {OPTIONS_DICT['PSKT_ARR'][KNOT_FLAG]}:  %", 0, 0, I2C_NUM_COLS)
    lcd_putstr("KG:     /--.-       ", 0, 1, I2C_NUM_COLS)
    lcd_putstr("                    ", 0, 2, I2C_NUM_COLS)
    lcd_putstr(f"=PICO=   L{MOTOR_SPEED_LV} {OPTIONS_DICT['MA_ARR'][CP_SW]}", 0, 3, I2C_NUM_COLS)
    lcd_putstr(f"{DEFAULT_LB:.1f}", 4, 0, 4)
    lcd_putstr(f"{DEFAULT_LB * 0.45359237: >4.1f}", 4, 1, 4)
    lcd_putstr(f"{PRE_STRECH: >2d}", 17, 0, 2)
    
# Timer 計時器顯示
def show_timer():
    if TIMER:
        LCD.hide_cursor()
        lcd_putstr("   m  ", 14, 1, 6)
        timer_diff = TIMER_FLAG - TIMER
        if timer_diff < 0:
            return 0
        
        lcd_putstr("{: >3d}".format(int(timer_diff / 60)), 14, 1, 3)
        lcd_putstr("{: >2d}".format(timer_diff % 60), 18, 1, 2)

# Hardware Functional Testing 硬體功能測試
def hw_test(flag, ori_BZ_SW):
    global FIRST_TEST, BZ_SW
    LED_RED.off()
    i = 1
    while True:
        if i == 1:
            lcd_putstr(f"T{i}: BUTTON_SETTING P", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    ress", 0, 3, 14)
            if button_list('BUTTON_SETTING'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 2:
            lcd_putstr(f"T{i}: BUTTON_UP Press", 0, 2, I2C_NUM_COLS)
            if button_list('BUTTON_UP'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 3:
            lcd_putstr(f"T{i}: BUTTON_DOWN Pres", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    s", 0, 3, 14)
            if button_list('BUTTON_DOWN'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 4:
            lcd_putstr(f"T{i}: BUTTON_LEFT Pre", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    ss", 0, 3, 14)
            if button_list('BUTTON_LEFT'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 5:
            lcd_putstr(f"T{i}: BUTTON_RIGHT Pre", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    ss", 0, 3, 14)
            if button_list('BUTTON_RIGHT'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 6:
            lcd_putstr(f"T{i}: BUTTON_EXIT Pres", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    s", 0, 3, 14)
            if button_list('BUTTON_EXIT'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 7:
            lcd_putstr(f"T{i}: BUTTON_HEAD Pres", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    s", 0, 3, 14)
            if button_list('BUTTON_HEAD'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 8:
            lcd_putstr(f"T{i}: MOTO_LM_REAR Pre", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    ss", 0, 3, 14)
            if MOTOR_SW_REAR.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 9:
            lcd_putstr(f"T{i}: MOTO_LM_FRONT Pr", 0, 2, I2C_NUM_COLS)
            lcd_putstr("    ess", 0, 3, 14)
            if MOTOR_SW_FRONT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("", 0, 3, 14)
                i = i + 1
        elif i == 10:
            lcd_putstr(f"T{i}: LED GREEN ON?", 0, 2, I2C_NUM_COLS)
            lcd_putstr("[Pres SET KEY]", 0, 3, 14)
            LED_GREEN.on()
            if button_list('BUTTON_SETTING'):
                LED_GREEN.off()
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 11:
            lcd_putstr(f"T{i}: LED YELLOW ON?", 0, 2, I2C_NUM_COLS)
            LED_YELLOW.on()
            if button_list('BUTTON_SETTING'):
                LED_YELLOW.off()
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 12:
            lcd_putstr(f"T{i}: LED RED ON?", 0, 2, I2C_NUM_COLS)
            LED_RED.on()
            if button_list('BUTTON_SETTING'):
                LED_RED.off()
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 13:
            lcd_putstr(f"T{i}: BEEP ON?", 0, 2, I2C_NUM_COLS)
            beepbeep(0.2)
            if button_list('BUTTON_SETTING'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 14:
            lcd_putstr(f"T{i}: Right KEY FWD?", 0, 2, I2C_NUM_COLS)
            if button_list('BUTTON_RIGHT'):
                forward(EXTRA_CONFIG["MOTOR_SPEED_V2"], 500, 0, 0)
            if button_list('BUTTON_SETTING'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 15:
            lcd_putstr(f"T{i}: Left KEY BWD?", 0, 2, I2C_NUM_COLS)
            if button_list('BUTTON_LEFT'):
                backward(EXTRA_CONFIG["MOTOR_SPEED_V2"], 500, 1)
            if button_list('BUTTON_SETTING'):
                lcd_putstr(f"T{i}: PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 16:
            lcd_putstr(f"T{i}: Head Over 1000G", 0, 2, I2C_NUM_COLS)
            lcd_putstr(" ", 0, 3, 14)
            if abs(TENSION_MON) > 1000:
                lcd_putstr(f"T{i}: ALL TEST PASS", 0, 2, I2C_NUM_COLS)
                lcd_putstr("     Please", 0, 3, 14)
                FIRST_TEST = 2
                if flag == 0:
                    BZ_SW = ori_BZ_SW
                    config_save(0)
                
                lcd_putstr("[Please Reboot]", 0, 3, I2C_NUM_COLS)
                while True:
                    if button_list('BUTTON_EXIT'):
                        machine.reset()
        
        tension_info(None, 0)

# Reliability Testing Mode 穩定性測試模式
def rt_mode():
    try:
        global BUTTON_LIST, RT_MODE, PRE_STRECH, DEFAULT_LB, TIMER, CP_SW, CORR_COEF, RT_CC
        tmp_TENSION_COUNT = TENSION_COUNT
        tmp_RT_MODE = RT_MODE
        if RT_MODE == 1:
            if 'rt_logs.txt' in os.listdir():
                os.remove('rt_logs.txt')
                
            if 'rt_logs.1.txt' in os.listdir():
                os.remove('rt_logs.1.txt')
            CP_SW = 1
            PRE_STRECH = 10
            RT_CC[0], RT_CC[1] = CORR_COEF, CORR_COEF
            TIMER = time.time()
            lcd_putstr("Pres SET Run RTM", 0, 2, I2C_NUM_COLS)
            lcd_putstr("{: >2d}".format(PRE_STRECH), 17, 0, 2)
            while True:
                if button_list('BUTTON_SETTING'):
                    break
                
        if RT_MODE % 10 == 0:
            RT_CC[0] = random.uniform(0.95, 1.2)
            CORR_COEF = RT_CC[0]
        
        DEFAULT_LB = (LB_MAX - 15) + (RT_MODE % 11)
        lcd_putstr("{:.1f}".format(DEFAULT_LB), 4, 0, 4)
        lcd_putstr("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
        lcd_putstr("    --G", 13, 3, 7)
        t0 = time.time()
        start_tensioning()
        rtm_time = (time.time() - t0)
        lcd_putstr("{: >4d}".format(min(int((time.time() - TIMER) / 60), 9999)) + "m", 15, 1, 5)
        tension_info(None, 2)    
        rt_str = f"{TENSION_COUNT}T/{CORR_COEF:.2f}/{RT_CC[0]:.2f}/{rtm_time}"
        lcd_putstr(rt_str, 0, 2, I2C_NUM_COLS)
        if button_list('BUTTON_UP'):
            time.sleep(5)
        
        lcd_putstr("Pres SET Stop RTM", 0, 2, I2C_NUM_COLS)
        if button_list('BUTTON_SETTING'):
            RT_MODE = 0
            beepbeep(0.1)
            lcd_putstr("RTM: Manual Stop", 0, 2, I2C_NUM_COLS)
        elif rtm_time >= 20:
            RT_MODE = 0
            beepbeep(0.1)
            lcd_putstr(f"RTM: Timeout {rtm_time}S", 0, 2, I2C_NUM_COLS)
        elif (tmp_TENSION_COUNT + 1) != TENSION_COUNT:
            RT_MODE = 0
            beepbeep(0.1)
            lcd_putstr(ERR_MSG[1], 0, 2, I2C_NUM_COLS)
        
        if RT_MODE != 0:
            file = open('rt_logs.txt', 'a')
            file.write(f"{RT_MODE}/{rt_str}/{rtm_time}\n")
            file.close()
            if RT_MODE % 1000 == 0:
                if 'rt_logs.txt' in os.listdir():
                    os.rename('rt_logs.txt', 'rt_logs.1.txt')
            
            RT_MODE = RT_MODE + 1
        else:
            lcd_putstr("{: >4d}".format(min(int((time.time() - TIMER) / 60), 9999)) + "m", 15, 1, 5)
            lcd_putstr("{: >5d}R".format(tmp_RT_MODE), 14, 3, 6)
            while True:
                if button_list('BUTTON_EXIT'):
                    break
            
            TIMER = 0
            CORR_COEF = RT_CC[1]
            lcd_putstr("     ", 15, 1, 5)
            lcd_putstr("Ready", 0, 2, I2C_NUM_COLS)
            beepbeep(0.1)
            
    except Exception as e:
        handle_error(e, "rt_mode()")

def check_sw():
    lcd_putstr("Checking all switch.", 0, 2, I2C_NUM_COLS)
    check_count = 0
    while check_count < 3:
        for key in BUTTON_LIST:
            if button_list(key):
                return key
    
        check_count = check_count + 1
        time.sleep(0.3)
    
    return False

def check_hx_calibration(flag):
    hx_diff_g = int((HX711["HX711_V0"] - HX711_V0) / 100 * (HX711_CAL / 20))
    if abs(hx_diff_g) > 45:
        if HX711_V0 == 0:
            hx_str = "HX Need Calibration!"
        else:
            hx_str = "HX Need Calibration?"
        lcd_putstr(f"{hx_str}", 0, 2, I2C_NUM_COLS)
        
        if flag == 1:
            logs_save(f"{hx_str} {hx_diff_g}g", "init()")
    else:
        lcd_putstr("Ready", 0, 2, I2C_NUM_COLS)

def process_setting_item(item):
    global LB_MAX, LOAD_CELL_KG, WIFI_IP, ABORT_GRAM, HX711_CAL, JPLIEW, HX711_V0

    try:
        LCD.move_to(MENU_LIST_ARR[item][2][0], 1)
        LCD.blink_cursor_on()
        cursor_x = 0
        change_flag = False
        move_flag = False
        shift_flag = 0
        temp_LOAD_CELL_KG = LOAD_CELL_KG
        beepbeep(0.2)
        while True:
            if item == "9-1":
                if BUTTON_UP.value() or BUTTON_DOWN.value():
                    LOAD_CELL_KG = 70 - LOAD_CELL_KG
                    
                    # 如設定 LOAD_CELL 需重新校正
                    if temp_LOAD_CELL_KG != LOAD_CELL_KG:
                        if LOAD_CELL_KG == 20:
                            HX711_CAL = 20
                        elif LOAD_CELL_KG == 50:
                            HX711_CAL = 50
                            
                        HX711_V0 = 0
                        config_save(1)
                        
                    temp_LOAD_CELL_KG = LOAD_CELL_KG
                    val_item = f"{LOAD_CELL_KG}KG"
                    change_flag = True
            
            elif item == "9-2":
                if BUTTON_LEFT.value():
                    cursor_x = (cursor_x - 1) % 2
                    shift_flag = int(cursor_x >= 2)
                    move_flag = True
                
                elif BUTTON_RIGHT.value():
                    cursor_x = (cursor_x + 1) % 2
                    shift_flag = int(cursor_x >= 2)
                    move_flag = True

                elif cursor_x == 0:
                    if BUTTON_UP.value():
                        LB_MAX = LB_MAX + 10
                        change_flag = True
                    elif BUTTON_DOWN.value():
                        LB_MAX = LB_MAX - 10
                        change_flag = True
                        
                elif cursor_x == 1:
                    if BUTTON_UP.value():
                        LB_MAX = LB_MAX + 1
                        change_flag = True
                    elif BUTTON_DOWN.value():
                        LB_MAX = LB_MAX - 1
                        change_flag = True
                
                if change_flag:
                    if LOAD_CELL_KG == 20:
                        LB_MAX = max(35, min(50, LB_MAX))
                    elif LOAD_CELL_KG == 50:
                        LB_MAX = max(35, min(70, LB_MAX))
                    ABORT_GRAM = (LB_MAX + 5) * 454
                    val_item = f"{LB_MAX}LB"

            elif item == "9-3":
                if BUTTON_UP.value() or BUTTON_DOWN.value():
                    JPLIEW = 1 - JPLIEW
                    val_item = OPTIONS_DICT['HEAD'][JPLIEW]
                    change_flag = True
            
            if button_list('BUTTON_EXIT'):
                LCD.blink_cursor_off()
                config_save(0)
                return
                
            if change_flag == True:
                lcd_putstr(f"{val_item}", (I2C_NUM_COLS - len(val_item)), 1, len(val_item))
                LCD.move_to(MENU_LIST_ARR[item][2][0] + cursor_x + shift_flag, 1)
                config_save(0)
                beepbeep(0.1)
                change_flag = False

            if move_flag:
                LCD.move_to(MENU_LIST_ARR[item][2][0] + cursor_x + shift_flag, 1)
                beepbeep(0.1)
                move_flag = False
                
            time.sleep(0.1)
        
    except Exception as e:
        handle_error(e, "process_setting_item()") 

# Engineering Mode 設定頁面
def engineering_mode(flag):
    try:
        global MENU_TEMP, MENU_LIST_ARR, ENGINEER_MENU
    
        lcd_putstr(" ==== MENU     ==== ", 0, 0, I2C_NUM_COLS)
        lcd_putstr(f"[\x7FB N\x7E SET]  {TENSION_COUNT:>6}T", 0, 3, I2C_NUM_COLS)
        
        menu_len = len(MENU_LIST_ARR)

        sort_item = []
        for key in MENU_LIST_ARR:
            sort_item.append(key)
            
        sort_item.sort()

        if flag == 0:
            i = MENU_TEMP
        else:
            i= flag
        
        while True:
            key = sort_item[i]
            val = MENU_LIST_ARR[sort_item[i]]
            lcd_putstr(f"{val[0]}", 0, 1, I2C_NUM_COLS)
            lcd_putstr(f"{val[1]}", 0, 2, I2C_NUM_COLS)
            lcd_putstr(f"{key}", 11, 0, 3)
            
            # 顯示 itme 數值
            val_item = ""
            if key == '9-1':
                val_item = f"{globals()[MENU_LIST_ARR[key][3]]}KG"
            elif key == '9-2':
                val_item = f"{str(globals()[MENU_LIST_ARR[key][3]])}LB"
            elif key == '9-3':
                val_item = f"{OPTIONS_DICT['HEAD'][globals()[MENU_LIST_ARR[key][3]]]}"
            elif key == '9-6':
                val_item = f"{globals()[MENU_LIST_ARR[key][3]]}"
            elif key == '9-4':
                val_item = f"{HX711['RATE']}Hz"
            elif key == '9-5':
                val_item = f"{str(HX711['DIFF'] / 1000)[:3]}G"
        #    elif key == '9-6':
        #        val_item = f"{str(round(1 - ((HX711['ANOM_COUNT'] / HX711['SAMPLE_COUNT']) / 2), 4) * 100)[:5]}%"
            elif key == '3-3':
                val_item = f"v{VERSION}"
                lcd_putstr(f"          {VERDATE}", 0, 2, I2C_NUM_COLS)
            
            lcd_putstr(f"{val_item}", (I2C_NUM_COLS - len(val_item)), 1, len(val_item))
            LCD.hide_cursor()
            
            while True:
                if button_list('BUTTON_RIGHT'):
                    i = min(i + 1, menu_len - 1)
                    MENU_TEMP = i
                    break
                    
                elif button_list('BUTTON_LEFT'):
                    i = max(i - 1, 0)
                    MENU_TEMP = i
                    break
                    
                elif button_list('BUTTON_SETTING'):
                    if MENU_LIST_ARR[key][2][0] != None:
                        process_setting_item(key) 
                        
                    break
                    
                elif button_list('BUTTON_EXIT'):
                    beepbeep(0.1)
                    return 
                    
                time.sleep(0.1)
            
            beepbeep(0.1)
    
    except Exception as e:
        handle_error(e, "engineering_mode()")

init()
try:
    ts_info_time = time.ticks_ms()
    v0_arr = []
    while True:
        if RT_MODE == 0:
            # Start tensioning 開始張緊
            if button_list('BUTTON_HEAD'):
                start_tensioning()
                show_timer()
            
            # Setting mode 設定模式
            if button_list('BUTTON_SETTING'):
                beepbeep(0.1)
                setting_interface()
                setting()
                main_interface()
                lcd_putstr("Ready", 0, 2, I2C_NUM_COLS)
                beepbeep(0.1)
                show_timer()
            
            # Timer switch & Head reset 計時器開關 & 珠夾復位
            if button_list('BUTTON_EXIT'):
                press_time = time.ticks_ms()
                while BUTTON_EXIT.value() == EXTRA_CONFIG["PRESSED_STATE"]:
                    if time.ticks_diff(time.ticks_ms(), press_time) > 1000:
                        head_reset(None)
                        break
                
                if time.ticks_diff(time.ticks_ms(), press_time) <= 1000:
                    if TIMER:
                        if TIMER_FLAG:
                            TIMER = 0
                            TIMER_FLAG = 0
                            lcd_putstr("      ", 14, 1, 6)
                        else:
                            TIMER_FLAG = time.time()
                    else:
                        TIMER = time.time()
                        lcd_putstr("   m  ", 14, 1, 6)
                    
                beepbeep(0.5)
            
            # Tension increment/decrement setting 加減張力設定
            if button_list('BUTTON_UP') or button_list('BUTTON_DOWN') or button_list('BUTTON_LEFT') or button_list('BUTTON_RIGHT'):
                setting_ts()
            
            # Tension display update 張力顯示更新
            if (time.ticks_ms() - ts_info_time) > 100:
                LCD.hide_cursor()
                tension_info(None, 0)
                if TIMER:
                    if TIMER_FLAG == 0:
                        timer_diff = time.time() - TIMER
                        lcd_putstr("{: >3d}".format(int(timer_diff / 60)), 14, 1, 3)
                        lcd_putstr("{: >2d}".format(timer_diff % 60), 18, 1, 2)
                
                LCD.move_to(TS_ARR[CURSOR_XY_TS_TEMP][0], TS_ARR[CURSOR_XY_TS_TEMP][1])
                LCD.show_cursor()
                ts_info_time = time.ticks_ms()
            
        # Reliability Testing Mode 穩定性測試模式
        else:
            rt_mode()
        
        # 自動 V0 修正
        v0_arr.append(HX711["HX711_VAL"])
        if len(v0_arr) > 600:
            v0_arr = sorted(v0_arr)
            HX711["HX711_V0"] = v0_arr[int(len(v0_arr) / 2)]
            v0_arr = []
            check_hx_calibration(0)
        
        if ERR_MSG[0]:
            LED_RED.on()
            beepbeep(3)
            lcd_putstr(ERR_MSG[0], 0, 2, I2C_NUM_COLS)
            break
        
        time.sleep(0.01)
    
except Exception as e:
    handle_error(e, "main_loop()")
