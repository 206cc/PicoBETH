# MIT License
# 
# Copyright (c) 2023 Kuo Yang-Yang <MAIL: 500119.cpc@gmail.com IG:206cc.tw>
#                                  <WEB: https://github.com/206cc/PicoBETH>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# GitHub  https://github.com/206cc/PicoBETH
# YouTube https://www.youtube.com/@kuokuo702
# Please go to https://github.com/206cc/PicoBETH?tab=readme-ov-file#final-settings for instructions on how to configure FT and HX parameters.
# Basic parameters (settings saved in CFG_NAME will take precedence if there are stored parameter values)
# 第一次開機請至 https://github.com/206cc/PicoBETH?tab=readme-ov-file#final-settings 觀看如何設定 FT、HX 參數
# 基本參數(如 CFG_NAME 內有儲存參數值會以的存檔的設定為主)
FIRST_TEST = 1       # Self-test check on first boot
                     # 第一次開機自我測試檢查
HX711_CAL = 20.00    # Calibration coefficients for HX711 load cell amplifier
                     # HX711張力放大器校正系數
CORR_COEF_AUTO = 1   # Self-learning tension parameter 0=off 1=on
                     # 自我學習張力參數 0=off 1=on
LB_KG_SELECT = 0     # Setting for pounds or kilograms, 0=both can be set, 1=only pounds, 2=only kilograms
                     # 磅或公斤的設定，0=皆可設定，1=只設定磅，2=只設定公斤
DEFAULT_LB = 20.0    # Default weight in LB
                     # 預設磅數
PRE_STRECH = 10      # Default Pre-Strech
                     # 預設預拉
KNOT = 15            # Default Knot
                     # 預設打結
LB_MAX = 35.0        # Maximum tension in LB
                     # 設定張緊的最高磅數
LB_MIN = 15.0        # Minimum tension in LB
                     # 設定張緊的最低磅數
PS_MAX = 30          # Maximum percentage in Pre-Strech
                     # 設定預拉的最高%數
KNOT_MIN = 5         # Minimum percentage for knot
                     # 打結增最低%數
KNOT_MAX = 30        # Maximum percentage for knot
                     # 打結增最高%數
HX711_MAX = 25.00    # Maximum value for HX711 calibration parameter
                     # HX711校正參數最大值
HX711_MIN = 15.00    # Minimum value for HX711 calibration parameter
                     # HX711校正參數最小值
FT_ADD_MAX = 20      # Maximum value for Constant-pull adjustment parameter
                     # 恆拉微調參數最大值
FT_ADD_MIN = 1       # Minimum value for Constant-pull adjustment parameter
                     # 恆拉微調參數最小值
PU_PRECISE = 50      # Gram value for triggering constant tension adjustment
                     # 觸發恆拉微調公克值
PU_STAY = 0.3        # Pre-Strech hold time (using buzzer), return to the original tension setting after the specified number of seconds
                     # 預拉暫留秒數(使用蜂鳴器)，秒數過後退回原設定張力
FT_ADD = 7           # Number of steps for stepper motor during constant-pull adjustment
                     # 恆拉微調時步進馬達的步數
CP_SW = 1            # Constant-pull switch 0=off, 1=on
                     # 恆拉開關 0=關閉，1=啟用
BB_SW = 1            # Buzzer switch 0=off, 1=on
                     # 蜂鳴器開關 0=關閉，1=啟用
ABORT_GRAM = 20000   # Maximum interrupt grams (about 44 lb)
                     # 最大中斷公克(約44磅)
LOG_MAX = 50         # Maximum LOG retention records (Please do not set too large to avoid memory exhaustion and inability to boot)
                     # 最大LOG保留記錄(請勿太大，以免記憶體耗盡無法開機)
                    
import time, _thread, machine
from machine import I2C, Pin
from src.hx711 import hx711          # from https://github.com/endail/hx711-pico-mpy
from src.pico_i2c_lcd import I2cLcd  # from https://github.com/T-622/RPI-PICO-I2C-LCD

# Other parameters 其它參數
VERSION = "2.02"
VER_DATE = "2024-05-22"
SAVE_CFG_ARRAY = ['DEFAULT_LB','PRE_STRECH','CORR_COEF','MOTO_STEPS','HX711_CAL','TENSION_COUNT','BOOT_COUNT', 'LB_KG_SELECT','CP_SW','FT_ADD','CORR_COEF_AUTO','KNOT','MOTO_MAX_STEPS','FIRST_TEST','BB_SW'] # Saved variables 存檔變數
MENU_ARR = [[4,0],[4,1],[4,2],[15,0],[16,0],[15,1],[16,1],[18,1],[19,1],[11,3],[19,3]] # Array for LB setting menu 設定選單陣列
UNIT_ARR = ['LB&KG', 'LB', 'KG']
ONOFF_ARR = ['Off', 'On ']
MA_ARR = ['M', 'A']
ML_ARR = ['N', 'L']
PSKT_ARR = ['PS', 'KT']
TS_LB_ARR = [[4,0],[5,0],[7,0]] # Array for LB setting 磅調整陣列
TS_KG_ARR = [[4,1],[5,1],[7,1]] # Array for KG setting 公斤調整陣列
TS_KT     = [[14,0]]            # Switching between knot and Pre-Strech 打結鍵切換
TS_PS_ARR = [[17,0],[18,0]]     # Array for Pre-Strech 預拉調整陣列
MOTO_FORW_W = [[1, 0, 1, 0],[0, 1, 0, 0],[0, 1, 1, 1],[1, 0, 1, 0]] # Stepper motor forward rotation parameter 步進馬達正轉參數
MOTO_BACK_W = [[0, 1, 0, 1],[1, 0, 0, 1],[1, 0, 1, 0],[0, 1, 1, 0]] # Stepper motor reverse rotation parameter 步進馬達反轉參數
MOTO_MAX_STEPS = 1000000
MOTO_RS_STEPS = 2000    # Number of steps to retreat during slider reset 滑台復位時退回的步數
MOTO_SPEED_V1 = 0.0001  # Stepper motor high speed 步進馬達高速
MOTO_SPEED_V2 = 0.001   # Stepper motor low speed 步進馬達低速
FT_SUB_COEF = 0.5       # Compensation coefficient for reducing tension during constant-pull 恆拉時減少張力的補償系數
BOTTON_SLEEP = 0.1      # Button waiting time in seconds 按鍵等待秒數
CORR_COEF = 1.00        # Tension coefficient 張力系數

# Stepper motor 步進馬達
IN1 = machine.Pin(4, machine.Pin.OUT) # PUL-
IN2 = machine.Pin(5, machine.Pin.OUT) # PUL+
IN3 = machine.Pin(2, machine.Pin.OUT) # DIR-
IN4 = machine.Pin(3, machine.Pin.OUT) # DIR+

# Limit switches for slider front and rear limits 滑台限位前後限位感應開關
MOTO_SW_FRONT = Pin(6, Pin.IN, Pin.PULL_DOWN)  # Front limit 滑軌前限位感應開關
MOTO_SW_REAR = Pin(7, Pin.IN, Pin.PULL_DOWN)   # Rear limit 滑軌後限位感應開關

# Function keys 功能按鍵
BOTTON_HEAD = Pin(8, Pin.IN, Pin.PULL_DOWN)     # Bead clamp head activation button 珠夾頭啟動按鍵
BOTTON_UP = Pin(13, Pin.IN, Pin.PULL_DOWN)      # Up button 上按鍵
BOTTON_DOWN = Pin(12, Pin.IN, Pin.PULL_DOWN)    # Down button 下按鍵
BOTTON_LEFT = Pin(11, Pin.IN, Pin.PULL_DOWN)    # Left button 左按鍵
BOTTON_RIGHT = Pin(10, Pin.IN, Pin.PULL_DOWN)   # Right button 右按鍵
BOTTON_SETTING = Pin(14, Pin.IN, Pin.PULL_DOWN) # Setting button 設定按鍵
BOTTON_EXIT = Pin(15, Pin.IN, Pin.PULL_DOWN)    # Exit button 取消按鍵
BOTTON_LIST = {"BOTTON_HEAD":0,
               "BOTTON_SETTING":0,
               "BOTTON_EXIT":0,
               "BOTTON_UP":0,
               "BOTTON_DOWN":0,
               "BOTTON_LEFT":0,
               "BOTTON_RIGHT":0}                # Button list 按鈕列表
BOTTON_CLICK_MS = 500                           # Button click milliseconds 按鈕點擊毫秒

# LED
LED_GREEN = Pin(19, machine.Pin.OUT)  # Green 綠
LED_YELLOW = Pin(20, machine.Pin.OUT) # Yellow 黃
LED_RED = Pin(21, machine.Pin.OUT)    # Red 紅

# Active buzzer 蜂鳴器
BEEP = Pin(22, machine.Pin.OUT)

# Global variables 全域變數
LB_CONV_G = 0
TENSION_MON = 0
MOTO_MOVE = 0
MOTO_BACK = 0
MOTO_WAIT = 0
MOTO_STEPS = 0
CURSOR_XY_TMP = 0
CURSOR_XY_TS_TMP = 1
HX711 = {"RATE":0, "DIFF":0, "V0":[]}
TENSION_COUNT = 0
BOOT_COUNT = 0
TIMER = 0
ERR_MSG = ""
ABORT_LM = 0
TS_ARR = []
LOGS = []
TENSION_MON_TMP = 0
KNOT_FLAG = 0

# 2004 i2c LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# HX711
hx = hx711(Pin(27), Pin(26))
hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_80)

# Read file parameters 參數讀取
def config_read():
    try:
        file = open("config.cfg", "r")
        data = file.read()
        config_list = data.split(",")
        for val in config_list:
            cfg = val.split("=")
            if cfg[0]:
                if "." in cfg[1]:
                    globals()[cfg[0]] = float(cfg[1])
                else:
                    globals()[cfg[0]] = int(cfg[1])
                    
        file.close()
    except OSError:  # failed
       pass

# Writing file Parameter 參數寫入
def config_save():
    try:
        file = open("config.cfg", "w")
        save_cfg = ""
        for val in SAVE_CFG_ARRAY:
            if isinstance(globals()[val], int) or isinstance(globals()[val], float):
                save_cfg = save_cfg + val +"=" + str(globals()[val]) + ","

        file.write(save_cfg)
        file.close()
    except OSError:  # failed
       pass

# Writing file LOG 寫入LOG
def logs_save(log_str, flag):
    try:
        file = open("logs.txt", flag)
        for element in reversed(log_str):
            save_log = ""
            for val in element:
                save_log = save_log + str(val) + ","

            file.write(save_log[:-1] + "\n") 
        file.close()
    except OSError:  # failed
       pass

# Read file LOG 讀取LOG
def logs_read():
    global LOGS
    try:
        fp = open("logs.txt", "r")
        line = fp.readline()
        while line:
            log_list = line.strip().split(",")
            LOGS.insert(0, log_list)
            line = fp.readline()
            if len(LOGS) > LOG_MAX:
                LOGS = LOGS[:LOG_MAX]
        
        fp.close()
        logs_save(LOGS, "w")
    except OSError:  # failed
       pass

# Active buzzer 有源蜂鳴器
def beepbeep(run_time):
    if BB_SW == 1:
        BEEP.on()
        time.sleep(run_time)
        BEEP.off()
    else:
        time.sleep(run_time)

# Tension display 張力顯示
def tension_info(tension):
    if tension is None:
        tension = TENSION_MON
    
    show_lcd("{: >4.1f}".format(tension * 0.0022), 9, 0, 4)
    show_lcd("{: >4.1f}".format(tension / 1000), 9, 1, 4)
    show_lcd("{: >5d}G".format(tension), 14, 3, 6)
    return tension

# Stepper motor operation 步進馬達作動
def setStep(in_w):
    IN1.value(in_w[0])
    IN2.value(in_w[1])
    IN3.value(in_w[2])
    IN4.value(in_w[3])

# Increase in tension 張力增加
def forward(delay, steps, check, init):
    global MOTO_MOVE, MOTO_WAIT
    LED_GREEN.off()
    MOTO_MOVE = 1
    for i in range(0, steps):
        if check == 1:
            if MOTO_WAIT == 1:
                MOTO_MOVE = 0
                MOTO_WAIT = 0
                return(0)
            
            
            # Exit button 離開按鍵
            if botton_list('BOTTON_EXIT'):
                moto_goto_standby()
                MOTO_MOVE = 0
                MOTO_WAIT = 0
                return("Abort")
            
            # Tension sensor anomaly or no string (tension less than 5 lb after ABORT_LM) 張力傳感器異常、無夾線(行程已過ABORT_LM時張力小於5磅)
            if i > ABORT_LM and TENSION_MON < 2267:
                moto_goto_standby()
                MOTO_MOVE = 0
                MOTO_WAIT = 0
                return("No String?")
        
        # Exceeding the rear limit switch 超過後限位SW
        if MOTO_SW_REAR.value():
            moto_goto_standby()
            if init:
                return i
                
            MOTO_MOVE = 0
            MOTO_WAIT = 0
            return("Over Limits")
        
        # Exceeding the maximum specified tension 超過最大指定張力
        if ABORT_GRAM < TENSION_MON:
            moto_goto_standby()
            MOTO_MOVE = 0
            MOTO_WAIT = 0
            return("ABORT GRAM")
        
        setStep(MOTO_FORW_W[0])
        setStep(MOTO_FORW_W[1])
        setStep(MOTO_FORW_W[2])
        setStep(MOTO_FORW_W[3])
        time.sleep(delay)

# Tension decrease 張力減少
def backward(delay, steps, check, init):
    global MOTO_BACK, MOTO_STEPS
    LED_GREEN.off()
    MOTO_BACK = 1
    for i in range(0, steps):
        if check == 1:
            if MOTO_SW_FRONT.value():
                if init == 1:
                    MOTO_STEPS = i
                    
                time.sleep(0.1)
                forward(MOTO_SPEED_V1, MOTO_RS_STEPS, 0, 0)
                MOTO_BACK = 0
                return 0 
            
        setStep(MOTO_BACK_W[0])
        setStep(MOTO_BACK_W[1])
        setStep(MOTO_BACK_W[2])
        setStep(MOTO_BACK_W[3])
        time.sleep(delay)

# Slider reset 滑台復位
def moto_goto_standby():
    LED_YELLOW.on()
    time.sleep(0.2)
    backward(MOTO_SPEED_V1, MOTO_MAX_STEPS, 1, 0)
    beepbeep(0.2)
    LED_YELLOW.off()
    LED_GREEN.on()

# LCD display
def show_lcd(text, x, y, length):
    text = text[:length]
    text = f'{text :{" "}<{length}}'
    lcd.move_to(x, y)
    lcd.putstr(text)

# Button detection 按鈕偵測
def botton_list(key):
    global BOTTON_LIST
    if BOTTON_LIST[key]:
        BOTTON_LIST[key] = 0
        return True
    else:
        return False
    
# Second core 第二核心
def tension_monitoring():
    global TENSION_MON, MOTO_WAIT, HX711, BOTTON_LIST, TENSION_MON_TMP
    # HX711 zeroing 歸零HX711
    v0_arr = []
    t0 = time.ticks_ms()
    while True:
        if val := hx.get_value_noblock():
            HX711["V0"].append(val)
            if (time.ticks_ms() - t0) > 1000:
                v0_arr = sorted(HX711["V0"])
                v0 = v0_arr[int((len(v0_arr)/2))]
                HX711["DIFF"] = v0_arr[-1] - v0_arr[0]
                HX711["RATE"] = len(v0_arr)
                break
    
    while True:
        # Tension monitoring 張力監控
        if val := hx.get_value_noblock():
            TENSION_MON = int((val-(v0))/100*(HX711_CAL/20))
            if MOTO_MOVE == 1:
                if LB_CONV_G < (TENSION_MON * CORR_COEF):
                    TENSION_MON_TMP = TENSION_MON
                    MOTO_WAIT = 1
        
        # Button detection 按鍵偵測
        for key in BOTTON_LIST:
            if globals()[key].value() == 1:
                BOTTON_LIST[key] = time.ticks_ms()
            elif BOTTON_LIST[key]:
                if (time.ticks_ms() - BOTTON_LIST[key]) > BOTTON_CLICK_MS:
                    BOTTON_LIST[key] = 0

def lb_kg_select():
    global TS_ARR
    if LB_KG_SELECT == 1:
        TS_ARR = TS_LB_ARR + TS_KT + TS_PS_ARR
    elif LB_KG_SELECT == 2:
        TS_ARR = TS_KG_ARR + TS_KT + TS_PS_ARR
    else:
        TS_ARR = TS_LB_ARR + TS_KG_ARR + TS_KT + TS_PS_ARR

# Boot initialization 開機初始化
def init():
    global LB_CONV_G, TS_ARR, ERR_MSG, ABORT_LM, MOTO_RS_STEPS, MOTO_MAX_STEPS, BOOT_COUNT, ABORT_GRAM, FT_ADD
    max_MOTO_MAX_STEPS = MOTO_MAX_STEPS
    config_read()
    logs_read()
    lb_kg_select()
    show_lcd(" **** PicoBETH **** ", 0, 0, I2C_NUM_COLS)
    show_lcd("Version: " + VERSION, 0, 1, I2C_NUM_COLS)
    show_lcd("Date: " + VER_DATE, 0, 2, I2C_NUM_COLS)
    show_lcd("Ghub: 206cc/PicoBETH", 0, 3, I2C_NUM_COLS)
    time.sleep(3)
    LED_RED.on()
    main_interface()
    ori_ABORT_GRAM = ABORT_GRAM
    ABORT_GRAM = 1000
    LB_CONV_G = min(int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100)), int(LB_MAX * 453.59237))
    show_lcd("Tension monitoring...", 0, 2, I2C_NUM_COLS)
    _thread.start_new_thread(tension_monitoring, ())
    
    # Waiting for HX711 zeroing 等待 HX711 歸零
    i = 0
    while True:
        if HX711["RATE"] != 0:
            break
        
        if i > 20:
            ERR_MSG = "ERR: HX711@Zero #1"
            break
        
        i = i + 1
        time.sleep(0.1)
        
    # Sampling error less than 0.01 grams (HX711 damaged?) 取樣誤差過小於 0.01公克(HX711損壞?)
    if HX711["DIFF"] < 10:
        ERR_MSG = "ERR: HX711@Zero #2"
        
    # Sampling value too small (HX711 damaged?) 取樣值過小(HX711損壞?)
    if HX711["V0"][0] < 0:
        ERR_MSG = "ERR: HX711@Zero #3"

    # Check if HX711 RATE exceeds 75Hz 檢查 HX711 RATE 是否超過 75Hz
    if HX711["RATE"] < 75:
        ERR_MSG = "ERR: HX711@"+ str(HX711["RATE"]) +"Hz"

    # Sampling error exceeds 1 gram (unstable) 取樣誤差過大超過 1公克(不穩定)
    if HX711["DIFF"] > 1000:
        ERR_MSG = "ERR: HX711@"+ str(int(HX711["DIFF"]/1000)) +"G #1"

    # Standby error exceeds 5 grams (unstable) 待機誤差過大超過 5公克(不穩定)
    if abs(TENSION_MON) > 5:
        ERR_MSG = "ERR: HX711@"+ str(abs(TENSION_MON)) +"G #2"
    
    if ERR_MSG == "":
        if FIRST_TEST == 1:
            first_test()
        
        moto_goto_standby()
        show_lcd("Checking motor...", 0, 2, I2C_NUM_COLS)
        ori_MOTO_MAX_STEPS = MOTO_MAX_STEPS
        MOTO_MAX_STEPS = max_MOTO_MAX_STEPS
        MOTO_MAX_STEPS = forward(MOTO_SPEED_V1, MOTO_MAX_STEPS, 0, 1)
        
        if MOTO_MAX_STEPS == "ABORT GRAM":
            ERR_MSG = "ERR: Abort Gram"
        else:
            MOTO_RS_STEPS = int(int(MOTO_MAX_STEPS) / 20)
            ABORT_LM = int(int(MOTO_MAX_STEPS) * 0.3)
            ABORT_GRAM = ori_ABORT_GRAM
            tmp_FT_ADD = round(FT_ADD * MOTO_MAX_STEPS / ori_MOTO_MAX_STEPS)
            if tmp_FT_ADD != 0:
                FT_ADD = tmp_FT_ADD
            
            moto_goto_standby()
            LED_RED.off()
            if FIRST_TEST == 2:
                show_lcd("Check HX Coeffs!", 0, 2, I2C_NUM_COLS)
            else:
                show_lcd("Ready", 0, 2, I2C_NUM_COLS)
                
            beepbeep(0.3)
            BOOT_COUNT = BOOT_COUNT + 1
            config_save()

# Start increasing tension 開始增加張力
def start_tensioning():
    global MOTO_MOVE, MOTO_WAIT, TENSION_COUNT, LOGS, CORR_COEF, FT_ADD, KNOT_FLAG, LB_CONV_G
    show_lcd("Tensioning", 0, 2, I2C_NUM_COLS)
    if KNOT_FLAG == 0:
        LB_CONV_G = min(int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100)), int(LB_MAX * 453.59237))
    else:
        LB_CONV_G = min(int((DEFAULT_LB * 453.59237) * ((KNOT + 100) / 100)), int(LB_MAX * 453.59237))
    
    if TIMER:
        timer_diff = time.time() - TIMER
    else:
        timer_diff = 0
        
    rel = forward(MOTO_SPEED_V1, MOTO_MAX_STEPS, 1, 0)
    if rel:
        show_lcd(str(rel), 0, 2, I2C_NUM_COLS)
        return 0

    MOTO_MOVE = 0
    abort_flag = 0
    count_add = 0
    count_sub = 0
    over_flag = 0
    cc_count_add = 0
    cc_add_flag = 0
    log_lb_max = 0
    manual_flag = 1
    log_lb_max = 0
    tmp_LB_CONV_G = LB_CONV_G
    LED_YELLOW.on()
    t0 = time.time()
    # Reached specified tension 到達指定張力
    while True:
        ft_flag = 0
        if over_flag == 0:
            if abs(tmp_LB_CONV_G - TENSION_MON) < PU_PRECISE:
                beepbeep(PU_STAY)
                log_lb_max = tmp_LB_CONV_G
                tension_info(log_lb_max)
                show_lcd("Target Tension", 0, 2, I2C_NUM_COLS)
                show_lcd("S:   ", 15, 1, 5)
                if KNOT_FLAG == 0:
                    tmp_LB_CONV_G = int(DEFAULT_LB * 453.59237)
                    
                t0 = time.time()
                if PRE_STRECH == 0:
                    over_flag = 2
                    if CP_SW == 1:
                        manual_flag = 1
                    else:
                        manual_flag = 0
                else:
                    over_flag = 1
                    
        elif over_flag == 1:
            if (abs(tmp_LB_CONV_G - TENSION_MON) < PU_PRECISE) and (time.time()-t0) > 0.5:
                beepbeep(0.1)
                t0 = time.time()
                over_flag = 2
                if CP_SW == 1:
                    manual_flag = 1
                else:
                    manual_flag = 0
        
        # Constant-pull increase 恆拉增加張力
        if tmp_LB_CONV_G > TENSION_MON and (manual_flag == 1 or over_flag == 0):
            diff_g = tmp_LB_CONV_G - TENSION_MON
            abort_flag = forward(MOTO_SPEED_V2, FT_ADD, 0 ,0)
            if diff_g < PU_PRECISE:
                ft_flag = 0
                cc_add_flag = 1  
            else:
                ft_flag = 1
                if cc_add_flag == 0:
                    cc_count_add = cc_count_add + 1
                
                if over_flag == 0:
                    count_add = count_add + 1    
        
        # Constant-pull decrease 恆拉減少張力
        if (tmp_LB_CONV_G + PU_PRECISE) < TENSION_MON and (manual_flag == 1 or over_flag == 0):
            diff_g =  TENSION_MON - tmp_LB_CONV_G
            abort_flag = backward(MOTO_SPEED_V2, FT_ADD * FT_SUB_COEF, 0, 0)
            if diff_g < PU_PRECISE:
                ft_flag = 0
            else:
                ft_flag = 1
            
            if over_flag == 0:
                count_sub = count_sub + 1
            
        # Manually increase tension 手動增加張力
        if botton_list('BOTTON_UP'):
            manual_flag = 0
            forward(MOTO_SPEED_V2, FT_ADD, 0, 0)
            show_lcd(MA_ARR[manual_flag], 11, 3, 1)
            count_add = count_add + 1
                
        # Manually decrease tension 手動減少張力
        if botton_list('BOTTON_DOWN'):
            manual_flag = 0
            backward(MOTO_SPEED_V2, FT_ADD * FT_SUB_COEF, 1, 0)
            show_lcd(MA_ARR[manual_flag], 11, 3, 1)
            count_sub = count_sub + 1
                
        # Manual & automatic adjustment toggle 手動&自動微調切換
        if botton_list('BOTTON_SETTING'):
            if manual_flag == 0:
                manual_flag = 1
            else:
                manual_flag = 0
                    
            show_lcd(MA_ARR[manual_flag], 11, 3, 1)
            beepbeep(0.1)
        
        # Disconnection (suddenly less than 5 lb) 斷線(突然小於5磅)
        if TENSION_MON < 2267:
            show_lcd(MA_ARR[CP_SW], 11, 3, 1)
            show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
            moto_goto_standby()
            show_lcd("String Broken?", 0, 2, I2C_NUM_COLS)
            show_lcd("     ", 15, 1, 5)
            MOTO_WAIT = 0
            return 0
        
        # Exit & head button 取消與珠夾頭按鈕
        if botton_list('BOTTON_HEAD') or botton_list('BOTTON_EXIT'):
            #CC參數自動調整
            cc_add_sub = 0
            if CORR_COEF_AUTO == 1:
                if cc_count_add > 5:
                    CORR_COEF = CORR_COEF - 0.01
                elif cc_count_add == 0:
                    CORR_COEF = CORR_COEF + 0.01
            
            log_s = time.time() - t0
            show_lcd(MA_ARR[CP_SW], 11, 3, 1)
            show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
            moto_goto_standby()
            show_lcd("Ready", 0, 2, I2C_NUM_COLS)
            show_lcd("     ", 15, 1, 5)
            MOTO_WAIT = 0
            TENSION_COUNT = TENSION_COUNT + 1
            # Writing to LOG 寫入LOG
            LOGS.insert(0, [TENSION_COUNT, timer_diff, LB_KG_SELECT, DEFAULT_LB, log_lb_max, PRE_STRECH, log_s, count_add, count_sub, CORR_COEF, HX711_CAL, FT_ADD, KNOT_FLAG, KNOT])
            logs_save([LOGS[0]], "a")
            if len(LOGS) > LOG_MAX:
                LOGS = LOGS[:LOG_MAX]
                
            if KNOT_FLAG == 1:
                KNOT_FLAG = 0
                show_lcd(PSKT_ARR[KNOT_FLAG], 14, 0, 2)
                show_lcd("{: >2d}".format(PRE_STRECH), 17, 0, 2)
            
            config_save()
            return 0
        
        if abort_flag == 1:
            return 0  
        
        if ft_flag == 0:
            tension_info(None)
            show_lcd("{: >3d}".format(min(time.time()-t0, 999)), 17, 1, 3)
        else:
            time.sleep(0.02)

# Main screen 主畫面
def setting_ts():
    global DEFAULT_LB, PRE_STRECH, LB_CONV_G, CURSOR_XY_TS_TMP, KNOT_FLAG, KNOT
    if KNOT_FLAG == 1:
        ps_kt_show = DEFAULT_LB * ((KNOT + 100) / 100)
    else:
        ps_kt_show = DEFAULT_LB * ((PRE_STRECH + 100) / 100)
                
    show_lcd("{: >4.1f}".format(ps_kt_show), 9, 0, 4)
    show_lcd("{: >4.1f}".format(ps_kt_show * 0.45359237), 9, 1, 4)
    last_set_time = time.ticks_ms()
    set_count = len(TS_ARR)
    i = CURSOR_XY_TS_TMP
    cursor_xy = TS_ARR[i][0], TS_ARR[i][1]
    lcd.move_to(TS_ARR[i][0], TS_ARR[i][1])
    lcd.blink_cursor_on()
    ps_kt_tmp = 0
    if KNOT_FLAG == 0:
        ps_kt_tmp = PRE_STRECH
    else:
        ps_kt_tmp = KNOT
        
    while True:
        # Action of pressing the up or down button 按下上下鍵動作
        if BOTTON_UP.value() or BOTTON_DOWN.value():
            kg = round(DEFAULT_LB * 0.45359237, 1)
            # LB 10-digit setting 設定 LB十位數
            if cursor_xy == (4, 0):
                if BOTTON_UP.value():
                    DEFAULT_LB = DEFAULT_LB + 10
                elif BOTTON_DOWN.value():
                    DEFAULT_LB = DEFAULT_LB - 10
            
            # LB single-digit setting 設定 LB個位數
            elif cursor_xy == (5, 0):
                if BOTTON_UP.value():
                    DEFAULT_LB = DEFAULT_LB + 1
                elif BOTTON_DOWN.value():
                    DEFAULT_LB = DEFAULT_LB - 1
            
            # LB decimal setting 設定 LB小數
            elif cursor_xy == (7, 0):
                if BOTTON_UP.value():
                    DEFAULT_LB = DEFAULT_LB + 0.1
                elif BOTTON_DOWN.value():
                    DEFAULT_LB = DEFAULT_LB - 0.1
                    
            # KG 10-digit setting 設定 KG十位數
            elif cursor_xy == (4, 1):
                if BOTTON_UP.value():
                    kg = kg + 10
                elif BOTTON_DOWN.value():
                    kg = kg - 10
                    
                DEFAULT_LB = round(kg * 2.20462262, 1)

            # KG single-digit setting 設定 KG個位數
            elif cursor_xy == (5, 1):
                if BOTTON_UP.value():
                    kg = kg + 1
                elif BOTTON_DOWN.value():
                    kg = kg - 1
                    
                DEFAULT_LB = round(kg * 2.20462262, 1)
            
            # KG decimal setting 設定 KG小數
            elif cursor_xy == (7, 1):
                if BOTTON_UP.value():
                    kg = kg + 0.1
                elif BOTTON_DOWN.value():
                    kg = kg - 0.1
                    
                DEFAULT_LB = round(kg * 2.20462262, 1)
            
            # Pre-Stretch or knot 10-digit setting 設定預拉或打結十位數
            elif cursor_xy == (17, 0):
                if BOTTON_UP.value():
                    ps_kt_tmp = ps_kt_tmp + 10
                elif BOTTON_DOWN.value():
                    ps_kt_tmp = ps_kt_tmp - 10
                
            # Pre-Stretch or knot single-digit setting 設定預拉或打結個位數
            elif cursor_xy == (18, 0):
                if BOTTON_UP.value():
                    ps_kt_tmp = ps_kt_tmp + 1
                elif BOTTON_DOWN.value():
                    ps_kt_tmp = ps_kt_tmp - 1
            
            # Pre-Stretch or knot tying switch 預拉或打結切換
            elif cursor_xy == (14, 0):
                if BOTTON_UP.value() or BOTTON_DOWN.value():
                    if KNOT_FLAG == 1:
                        KNOT_FLAG = 0
                        ps_kt_tmp = PRE_STRECH
                    else:
                        KNOT_FLAG = 1
                        ps_kt_tmp = KNOT
                        
                    show_lcd(PSKT_ARR[KNOT_FLAG], 14, 0, 2)
                    show_lcd("{: >2d}".format(ps_kt_tmp), 17, 0, 2)
            
            if DEFAULT_LB >= LB_MAX:
                DEFAULT_LB = LB_MAX  
            elif DEFAULT_LB <= LB_MIN:
                DEFAULT_LB = LB_MIN
            
            if KNOT_FLAG == 1:
                KNOT = ps_kt_tmp
                if KNOT >= KNOT_MAX:
                    KNOT = KNOT_MAX
                elif KNOT <= KNOT_MIN:
                    KNOT = KNOT_MIN
                    
                ps_kt_tmp = KNOT
                show_lcd("{: >2d}".format(KNOT), 17, 0, 2)
                ps_kt_show = DEFAULT_LB * ((KNOT + 100) / 100)
            else:
                PRE_STRECH = ps_kt_tmp
                if PRE_STRECH >= PS_MAX:
                    PRE_STRECH = PS_MAX
                elif PRE_STRECH <= 0:
                    PRE_STRECH = 0
                
                ps_kt_tmp = PRE_STRECH
                show_lcd("{: >2d}".format(PRE_STRECH), 17, 0, 2)
                ps_kt_show = DEFAULT_LB * ((PRE_STRECH + 100) / 100)
            
            show_lcd("{: >4.1f}".format(ps_kt_show), 9, 0, 4)
            show_lcd("{: >4.1f}".format(ps_kt_show * 0.45359237), 9, 1, 4)
            show_lcd("{:.1f}".format(DEFAULT_LB), 4, 0, 4)
            show_lcd("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
            lcd.move_to(TS_ARR[i][0],TS_ARR[i][1])
            last_set_time = time.ticks_ms()
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)

        # Action of pressing the left or right button 按下左右鍵動作
        if BOTTON_RIGHT.value() or BOTTON_LEFT.value():
            if BOTTON_RIGHT.value():
                if (i+1) < set_count:
                    i = i + 1
                else:
                    i = 0
            elif BOTTON_LEFT.value():
                if (i-1) >= 0:
                    i = i - 1
                else:
                    i = set_count - 1
            
            CURSOR_XY_TS_TMP = i
            lcd.move_to(TS_ARR[i][0], TS_ARR[i][1])
            cursor_xy = TS_ARR[i][0], TS_ARR[i][1]
            last_set_time = time.ticks_ms()
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)

        # Action of pressing the exit button 按下離開鍵動作
        if botton_list('BOTTON_EXIT') or ((time.ticks_ms() - last_set_time) > (1.8 * 1000)):
            config_save()
            lcd.blink_cursor_off()
            time.sleep(BOTTON_SLEEP)
            beepbeep(0.1)
            return 0

# Settings screen 設定頁面
def setting():
    global CURSOR_XY_TMP, CORR_COEF, HX711_CAL, LB_KG_SELECT, FT_ADD, CURSOR_XY_TS_TMP, CP_SW, BB_SW, FIRST_TEST
    set_count = len(MENU_ARR)
    i = CURSOR_XY_TMP
    cursor_xy = MENU_ARR[i][0], MENU_ARR[i][1]
    lcd.move_to(MENU_ARR[i][0], MENU_ARR[i][1])
    lcd.blink_cursor_on()
    time.sleep(BOTTON_SLEEP)
    beepbeep(0.1)
    while True:
        # Action of pressing the up or down button 按下上下鍵動作
        if BOTTON_UP.value() or BOTTON_DOWN.value() or botton_list('BOTTON_SETTING'):
            flag = 0
            # System information 系統資訊
            if cursor_xy == (11, 3):
                if BOTTON_SETTING.value():
                    beepbeep(0.1)
                    show_lcd("SW:V"+ VERSION +"_"+ VER_DATE, 0, 0, I2C_NUM_COLS)
                    show_lcd("HX:"+ str(HX711["DIFF"]) +"mg/"+ str(sorted(HX711["V0"])[0]) +"/"+ str(HX711["RATE"]) +"Hz", 0, 1, I2C_NUM_COLS)
                    show_lcd("CC:"+ ML_ARR[CORR_COEF_AUTO] + "{: >1.2f}".format(CORR_COEF) +"   BOOT:" + str(BOOT_COUNT), 0, 2, I2C_NUM_COLS)
                    lcd.move_to(11, 3)
                    beepbeep(0.1)
                    while True:
                        if BOTTON_EXIT.value():
                            beepbeep(0.1)
                            setting_interface()
                            break
            
            # LB or KG setting selection 磅、公斤設定選擇
            elif cursor_xy == (4, 0):
                if BOTTON_UP.value() or BOTTON_DOWN.value():
                    CURSOR_XY_TS_TMP = 1
                    LB_KG_SELECT = (LB_KG_SELECT + 1) % 3
                    show_lcd(UNIT_ARR[LB_KG_SELECT], 4, 0, 5)
                    lb_kg_select()

            # Tension adjustment FT parameter ten-digit 張力微調 FT參數十位數
            elif cursor_xy == (15, 0):
                flag = 2
                if BOTTON_UP.value():
                    FT_ADD = FT_ADD + 10
                elif BOTTON_DOWN.value():
                    FT_ADD = FT_ADD - 10

            # Tension adjustment FT parameter single-digit 張力微調 FT參數個位數
            elif cursor_xy == (16, 0):
                flag = 2
                if BOTTON_UP.value():
                    FT_ADD = FT_ADD + 1
                elif BOTTON_DOWN.value():
                    FT_ADD = FT_ADD - 1
                    
            # Constant-pull switch 恆拉開關
            elif cursor_xy == (4, 1):
                if BOTTON_UP.value() or BOTTON_DOWN.value():
                    if CP_SW == 1:
                        CP_SW = 0
                    else:
                        CP_SW = 1
                    
                    show_lcd(ONOFF_ARR[CP_SW], 4, 1, 3)
                    
            # Buzzer switch 蜂鳴器開關
            elif cursor_xy == (4, 2):
                if BOTTON_UP.value() or BOTTON_DOWN.value():
                    if BB_SW == 1:
                        BB_SW = 0
                    else:
                        BB_SW = 1
                    
                    show_lcd(ONOFF_ARR[BB_SW], 4, 2, 3)

            # HX711 calibration coefficient ten-digit 校正系數十位數HX711
            elif cursor_xy == (15, 1):
                flag = 1
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 10
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 10
                    
            # HX711 calibration coefficient single-digit 校正系數個位數HX711
            elif cursor_xy == (16, 1):
                flag = 1
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 1
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 1
            
            # HX711 calibration coefficient first decimal 校正系數第一位小數HX711
            elif cursor_xy == (18, 1):
                flag = 1
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 0.1
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 0.1
                    
            # HX711 calibration coefficient second decimal 校正系數第二位小數HX711
            elif cursor_xy == (19, 1):
                flag = 1
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 0.01
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 0.01

            # Display LOG 顯示LOG
            elif cursor_xy == (19, 3):
                if BOTTON_SETTING.value():
                    beepbeep(0.1)
                    if len(LOGS) != 0:
                        logs_idx = 0
                        lcd.hide_cursor()
                        logs_interface("init")
                        logs_interface(logs_idx)
                        log_flag = 0
                        beepbeep(0.1)
                        while True:
                            if BOTTON_RIGHT.value():
                                logs_idx = (logs_idx + 1) % len(LOGS)
                                beepbeep(0.1)
                            elif BOTTON_LEFT.value():
                                logs_idx = logs_idx - 1
                                if logs_idx < 0:
                                    logs_idx = len(LOGS) - 1
                                beepbeep(0.1)
                            elif BOTTON_EXIT.value():
                                beepbeep(0.1)
                                break
                            
                            if log_flag != logs_idx:
                                logs_interface(logs_idx)
                                beepbeep(0.1)
                                log_flag = logs_idx
                            
                        setting_interface()
                        lcd.show_cursor()
                        lcd.blink_cursor_on()
            
            if flag == 1:
                if HX711_CAL >= HX711_MAX:
                    HX711_CAL = HX711_MAX  
                elif HX711_CAL <= HX711_MIN:
                    HX711_CAL = HX711_MIN
                
                if FIRST_TEST == 2:
                    FIRST_TEST = 0
            
            if flag == 2:
                if FT_ADD >= FT_ADD_MAX:
                    FT_ADD = FT_ADD_MAX  
                elif FT_ADD <= FT_ADD_MIN:
                    FT_ADD = FT_ADD_MIN
            
            show_lcd("{: >2.2f}".format(HX711_CAL), 15, 1, 5)
            show_lcd("{:02d}".format(FT_ADD), 15, 0, 2)
            lcd.move_to(MENU_ARR[i][0],MENU_ARR[i][1])
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)

        # Action of pressing the left or right button 按下左右鍵動作
        if BOTTON_RIGHT.value() or BOTTON_LEFT.value():
            if BOTTON_RIGHT.value():
                if (i+1) < set_count:
                    i = i + 1
                else:
                    i = 0
            elif BOTTON_LEFT.value():
                if (i-1) >= 0:
                    i = i - 1
                else:
                    i = set_count - 1
            
            CURSOR_XY_TMP = i
            lcd.move_to(MENU_ARR[i][0], MENU_ARR[i][1])
            cursor_xy = MENU_ARR[i][0], MENU_ARR[i][1]
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)

        # Action of pressing the exit button 按下離開鍵動作
        if botton_list('BOTTON_EXIT'):
            config_save()
            lcd.blink_cursor_off()
            time.sleep(BOTTON_SLEEP)
            beepbeep(0.1)
            return 0
     
# Settings interface display 設定介面顯示
def setting_interface():
    show_lcd("UN:        FT: "+ "{:02d}".format(FT_ADD), 0, 0, I2C_NUM_COLS)
    show_lcd(UNIT_ARR[LB_KG_SELECT], 4, 0, 5) 
    show_lcd("AT: "+ ONOFF_ARR[CP_SW] +"    HX: "+ "{: >2.2f}".format(HX711_CAL), 0, 1, I2C_NUM_COLS)
    show_lcd("BB: "+ ONOFF_ARR[BB_SW], 0, 2, I2C_NUM_COLS)
    show_lcd("<PicoBETH> I "+ "{: >6d}".format(TENSION_COUNT) +"T", 0, 3, I2C_NUM_COLS)
    
# LOG interface display 介面顯示LOG
def logs_interface(idx):
    if idx=="init":
        show_lcd("  LOG  TIMER:   m  s", 0, 0, I2C_NUM_COLS)
        show_lcd("LB:    /        :  %", 0, 1, I2C_NUM_COLS)
        show_lcd("FT:  /  /      S:   ", 0, 2, I2C_NUM_COLS)
        show_lcd("C/H:    /          T", 0, 3, I2C_NUM_COLS)
    else:
        show_lcd("{:0>2d}".format((idx + 1)), 0, 0, 2)
        if int(LOGS[idx][1]):
            show_lcd("{: >3d}".format(int(int(LOGS[idx][1]) / 60)) +"m"+ "{: >2d}".format(int(int(LOGS[idx][1]) % 60)) +"s", 13, 0, 7)
        else:
            show_lcd(" ------", 13, 0, 7)
            
        if int(LOGS[idx][2]) == 2:
            show_lcd("KG:" + "{: >4.1f}".format(int(LOGS[idx][3]) * 0.45359237), 0, 1, 7)
            show_lcd("{: >4.1f}".format(int(LOGS[idx][4]) * 0.001), 8, 1, 4)
        else:
            show_lcd("LB:" + str(LOGS[idx][3]), 0, 1, 7)
            show_lcd("{: >4.1f}".format(int(LOGS[idx][4]) * 0.0022046), 8, 1, 4)
        
        if int(LOGS[idx][12]) == 1:
            show_lcd("KT:" + "{: >2d}".format(int(LOGS[idx][13])), 14, 1, 5)
        else:
            show_lcd("PS:" + "{: >2d}".format(int(LOGS[idx][5])), 14, 1, 5)
            
        show_lcd("{: >3d}".format(int(LOGS[idx][6])), 17, 2, 3)
        show_lcd("{: >2d}".format(int(LOGS[idx][7])), 3, 2, 2)
        show_lcd("{: >2d}".format(int(LOGS[idx][8])), 6, 2, 2)
        show_lcd("{:02d}".format(int(LOGS[idx][11])), 9, 2, 2)
        show_lcd("{:.2f}".format(float(LOGS[idx][9])), 4, 3, 4)
        show_lcd("{:.2f}".format(float(LOGS[idx][10])), 9, 3, 5)
        show_lcd("{: >5d}".format(int(LOGS[idx][0])), 14, 3, 5)

# Main screen display 主畫面顯示
def main_interface():
    show_lcd("LB:     /--.- "+ PSKT_ARR[KNOT_FLAG] +":  %", 0, 0, I2C_NUM_COLS)
    show_lcd("KG:     /--.-       ", 0, 1, I2C_NUM_COLS)
    show_lcd("                    ", 0, 2, I2C_NUM_COLS)
    show_lcd("<PicoBETH> "+ MA_ARR[CP_SW] + ML_ARR[CORR_COEF_AUTO], 0, 3, I2C_NUM_COLS)
    show_lcd("{:.1f}".format(DEFAULT_LB), 4, 0, 4)
    show_lcd("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
    show_lcd("{: >2d}".format(PRE_STRECH), 17, 0, 2)
    
# Timer display 計時器顯示
def show_timer():
    if TIMER:
        show_lcd("   m  ", 14, 1, 6)
        timer_diff = timer_flag - TIMER
        if timer_diff < 0:
            return 0
        
        show_lcd("{: >3d}".format(int(timer_diff / 60)), 14, 1, 3)
        show_lcd("{: >2d}".format(timer_diff % 60), 18, 1, 2)

# Initial functionality test on first boot 第一次開機功能測試
def first_test():
    global FIRST_TEST
    LED_RED.off()
    i = 1
    while True:
        if i == 1:
            show_lcd("T"+ str(i) +": BOTTON_SETTING P", 0, 2, I2C_NUM_COLS)
            show_lcd("    ress", 0, 3, 14)
            if botton_list('BOTTON_SETTING'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 2:
            show_lcd("T"+ str(i) +": BOTTON_UP Press", 0, 2, I2C_NUM_COLS)
            if botton_list('BOTTON_UP'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 3:
            show_lcd("T"+ str(i) +": BOTTON_DOWN Pres", 0, 2, I2C_NUM_COLS)
            show_lcd("    s", 0, 3, 14)
            if botton_list('BOTTON_DOWN'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 4:
            show_lcd("T"+ str(i) +": BOTTON_LEFT Pre", 0, 2, I2C_NUM_COLS)
            show_lcd("    ss", 0, 3, 14)
            if botton_list('BOTTON_LEFT'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 5:
            show_lcd("T"+ str(i) +": BOTTON_RIGHT Pre", 0, 2, I2C_NUM_COLS)
            show_lcd("    ss", 0, 3, 14)
            if botton_list('BOTTON_RIGHT'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 6:
            show_lcd("T"+ str(i) +": BOTTON_EXIT Pres", 0, 2, I2C_NUM_COLS)
            show_lcd("    s", 0, 3, 14)
            if botton_list('BOTTON_EXIT'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 7:
            show_lcd("T"+ str(i) +": BOTTON_HEAD Pres", 0, 2, I2C_NUM_COLS)
            show_lcd("    s", 0, 3, 14)
            if botton_list('BOTTON_HEAD'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 8:
            show_lcd("T"+ str(i) +": MOTO_LM_REAR Pre", 0, 2, I2C_NUM_COLS)
            show_lcd("    ss", 0, 3, 14)
            if MOTO_SW_REAR.value():
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 9:
            show_lcd("T"+ str(i) +": MOTO_LM_FRONT Pr", 0, 2, I2C_NUM_COLS)
            show_lcd("    ess", 0, 3, 14)
            if MOTO_SW_FRONT.value():
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                show_lcd("", 0, 3, 14)
                i = i + 1
        elif i == 10:
            show_lcd("T"+ str(i) +": LED GREEN ON?", 0, 2, I2C_NUM_COLS)
            show_lcd("[Pres SET KEY]", 0, 3, 14)
            LED_GREEN.on()
            if botton_list('BOTTON_SETTING'):
                LED_GREEN.off()
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 11:
            show_lcd("T"+ str(i) +": LED YELLOW ON?", 0, 2, I2C_NUM_COLS)
            LED_YELLOW.on()
            if botton_list('BOTTON_SETTING'):
                LED_YELLOW.off()
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 12:
            show_lcd("T"+ str(i) +": LED RED ON?", 0, 2, I2C_NUM_COLS)
            LED_RED.on()
            if botton_list('BOTTON_SETTING'):
                LED_RED.off()
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 13:
            show_lcd("T"+ str(i) +": BEEP ON?", 0, 2, I2C_NUM_COLS)
            beepbeep(0.2)
            if botton_list('BOTTON_SETTING'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 14:
            show_lcd("T"+ str(i) +": Right KEY FWD?", 0, 2, I2C_NUM_COLS)
            if botton_list('BOTTON_RIGHT'):
                forward(MOTO_SPEED_V2, 500, 0, 0)
            if botton_list('BOTTON_SETTING'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 15:
            show_lcd("T"+ str(i) +": Left KEY BWD?", 0, 2, I2C_NUM_COLS)
            if botton_list('BOTTON_LEFT'):
                backward(MOTO_SPEED_V2, 500, 1, 0)
            if botton_list('BOTTON_SETTING'):
                show_lcd("T"+ str(i) +": PASS", 0, 2, I2C_NUM_COLS)
                i = i + 1
        elif i == 16:
            show_lcd("T"+ str(i) +": Head Over 1000G", 0, 2, I2C_NUM_COLS)
            if abs(TENSION_MON) > 1000:
                show_lcd("T"+ str(i) +": ALL PASS Reboot", 0, 2, I2C_NUM_COLS)
                show_lcd("     Please", 0, 3, 14)
                FIRST_TEST = 2
                config_save()
                i = i + 1
        
        tension_info(None)
    
init()
ts_info_time = time.ticks_ms()
timer_flag = 0
while True:
    # Start tensioning 開始張緊
    if botton_list('BOTTON_HEAD'):
        start_tensioning()
        show_timer()
    
    # Setting mode 設定模式
    if botton_list('BOTTON_SETTING'):
        beepbeep(0.1)
        setting_interface()
        setting()
        main_interface()
        show_lcd("Ready", 0, 2, I2C_NUM_COLS)
        beepbeep(0.1)
        show_timer()
    
    # Timer switch 計時器開關
    if botton_list('BOTTON_EXIT'):
        if TIMER:
            if timer_flag:
                TIMER = 0
                timer_flag = 0
                show_lcd("      ", 14, 1, 6)
            else:
                timer_flag = time.time()
        else:
            TIMER = time.time()
            show_lcd("   m  ", 14, 1, 6)
            
        beepbeep(0.5)
    
    # Tension increment/decrement setting 加減張力設定
    if botton_list('BOTTON_UP') or botton_list('BOTTON_DOWN') or botton_list('BOTTON_LEFT') or botton_list('BOTTON_RIGHT'):
        setting_ts()
    
    # Tension display update 張力顯示更新
    if (time.ticks_ms() - ts_info_time) > 100:
        tension_info(None)
        if TIMER:
            if timer_flag == 0:
                timer_diff = time.time() - TIMER
                show_lcd("{: >3d}".format(int(timer_diff / 60)), 14, 1, 3)
                show_lcd("{: >2d}".format(timer_diff % 60), 18, 1, 2)
        
        lcd.move_to(TS_ARR[CURSOR_XY_TS_TMP][0], TS_ARR[CURSOR_XY_TS_TMP][1])
        lcd.show_cursor()
        ts_info_time = time.ticks_ms()
        
    if ERR_MSG:
        LED_RED.on()
        beepbeep(3)
        show_lcd(ERR_MSG, 0, 2, I2C_NUM_COLS)
        break
    