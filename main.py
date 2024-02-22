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

# 基本參數(如CFG_NAME內有儲存參數值會以的存檔的設定為主)
HX711_CAL = 20.00    # HX711張力感應器校正系數，第一次使用或有更換張力傳感器、HX711電路板時務必重新校正一次
                     # 校正方法:
                     #   1. 將外接式張力計，一端綁在拉線機上，另一端綁上羽毛球線
                     #   2. 先將LCD設定頁面中HX參數設為20.00
                     #   3. 跳回主選單設定拉力為20磅
                     #   4. 按上或下鍵開始張緊，當LCD顯示20磅時，抄下張力計顯示數值
                     #   5. 至設定頁面上填入剛抄下張力計的數值
                     # 註: 
                     #   1. 如不做此校正，實際張力會與LCD上的張力會有誤差
                     #   2 .此參數以設定存檔為主
                     # 參考影片: https://youtu.be/JaplgmXzbjY
                     
CORR_COEF = 1.00     # 當達到指定張力馬達停止時實際張力還會持續變化，另設此需除此係數校正，可手動設設也可自動在設定頁面校正
                     # 校正方法:
                     #   1. 將羽球線固定好，一端綁在拉線機上，另一端在珠夾上
                     #   2. 至LCD設定頁面中CC欄位中AUTO按鍵上按上或下鍵開始張緊
                     #   3. AUTO會自動填入參考的CC值
                     #   4. 使用此值張緊測式，最佳的結果是預拉為0時達到指定張力不會進行微調動作
                     #      (你也許會在馬達停止時看見LCD張力持續變化超過指定張力，這為正常物理現象，
                     #       最佳的參數在於張力平衡後會線剛好在指定張力不會進行微調的動作)
                     #   5. 如果自動的CC值不理想，可至設定頁面手動微調CC值後，重覆4的步驟，找到最佳的值
                     # 註: 
                     #   1. 如果有開預拉，會進行退磅的徵調，所以測試時請將預拉設為0
                     #   2. 更換HX711電路板、滑台螺距、馬達的電機會影響此系數，如果覺得在預拉為0時頻繁微調請校正此值
                     #   3. 此參數以設定存檔為主
                     # 參考影片: https://youtu.be/KuisR6eKiwk

LB_KG_SELECT = 0     # 磅或公斤的設定，0=皆可設定，1=只設定磅，2=只設定公斤
DEFAULT_LB = 18.0    # (LB)預設磅數
PRE_STRECH = 10      # (%)預拉Pre-Strech
LB_MAX = 35.0        # (LB)設定張緊的最高磅數
LB_MIN = 15.0        # (LB)設定張緊的最低磅數
PS_MAX = 30          # (LB)設定預拉的最高%數
HX711_MAX = 25.00    # HX711校正參數最大值
HX711_MIN = 15.00    # HX711校正參數最小值
CORR_MAX = 1.7       # 張力校正參數最大值
CORR_MIN = 0.3       # 張力校正參數最小值
FT_ADD_MAX = 30      # 增加磅數微調參數最大值
FT_ADD_MIN = 10      # 增加磅數微調參數最小值
PU_PRECISE = 200     # (G)如超過設定張力加此值，則進入釋放微調
PU_STAY = 1          # (Second)預拉暫留秒數，秒數過後退回原設定磅數
FT_ADD = 20          # 增加磅數微調時步進馬達的步數(1610螺桿參數)(建議調成微調一次增加0.3磅左右)
FT_AUTO = 1          # 自動微調加減張力 0=關閉，1=只設啟用
MOTO_RS_STEPS = 2000 # 滑台復位時感應到前限位開關時退回的步數，必需退回到未按壓前限位開關的程度
ABORT_GRAM = 20000   # (G)最大中斷公克(約44磅)
AUTO_SAVE_SEC = 1.5  # (Second)自動儲存設定張力秒數
LOG_MAX = 50         # 最大LOG保留記錄(請勿太大，以免記憶體耗盡無法開機)
                    
import time, _thread, machine
from machine import I2C, Pin
from src.hx711 import hx711          # from https://github.com/endail/hx711-pico-mpy
from src.pico_i2c_lcd import I2cLcd  # from https://github.com/T-622/RPI-PICO-I2C-LCD

# 其它參數(請勿更動)
VERSION = "1.52"
VER_DATE = "2024-02-22"
CFG_NAME = "config.cfg" # 設定存檔檔名
LOG_NAME = "logs.txt"   # LOG存檔檔名
SAVE_CFG_ARRAY = ['DEFAULT_LB','PRE_STRECH','CORR_COEF','MOTO_STEPS','HX711_CAL','TENSION_COUNTS', 'LB_KG_SELECT','FT_AUTO'] # 存檔變數
MENU_ARR = [[4,0],[4,1],[5,1],[7,1],[8,1],[4,2],[5,2],[7,2],[8,2],[15,0],[16,0],[15,1],[19,3]] # 設定選單陣列
UNIT_ARR = ['LB&KG', 'LB', 'KG']
ONOFF_ARR = ['Off', 'On']
AM_ARR = ['M', 'A']
TS_LB_ARR = [[4,0],[5,0],[7,0]] # 磅調整陣列
TS_KG_ARR = [[4,1],[5,1],[7,1]] # 公斤調整陣列
TS_PS_ARR = [[17,0],[18,0]]     # 預拉調整陣列
MOTO_FORW_W = [[1, 0, 1, 0],[0, 1, 0, 0],[0, 1, 1, 1],[1, 0, 1, 0]] # 步進馬達正轉參數
MOTO_BACK_W = [[0, 1, 0, 1],[1, 0, 0, 1],[1, 0, 1, 0],[0, 1, 1, 0]] # 步進馬達反轉參數
MOTO_MAX_STEPS = 1000000
MOTO_SPEED = 0.0001  # (Second)步進馬達速度(越小越快)
TS_INFO_MS = 100     # (MS)主畫面張力更新顯示毫秒
FT_SUB_COEF = 1.5    # 減少磅數微調時步進馬達的步數
FT_LB = 1            # (LB)進入連續微調的相差磅數
BOTTON_SLEEP = 0.1   # (Second)按鍵等待秒數

## 步進馬達
IN1 = machine.Pin(4, machine.Pin.OUT) # 接 PUL-
IN2 = machine.Pin(5, machine.Pin.OUT) # 接 PUL+
IN3 = machine.Pin(2, machine.Pin.OUT) # 接 DIR-
IN4 = machine.Pin(3, machine.Pin.OUT) # 接 DIR+

# 滑軌限位前後限位感應開關
MOTO_SW_FRONT = Pin(6, Pin.IN, Pin.PULL_DOWN)  # 滑軌前限位感應開關
MOTO_SW_REAR = Pin(7, Pin.IN, Pin.PULL_DOWN)   # 滑軌後限位感應開關

# 功能按鍵
BOTTON_HEAD = Pin(8, Pin.IN, Pin.PULL_DOWN)     # 啟動按鍵(珠夾頭)
BOTTON_UP = Pin(13, Pin.IN, Pin.PULL_DOWN)      # 上按鍵
BOTTON_DOWN = Pin(12, Pin.IN, Pin.PULL_DOWN)    # 下按鍵
BOTTON_LEFT = Pin(11, Pin.IN, Pin.PULL_DOWN)    # 左按鍵
BOTTON_RIGHT = Pin(10, Pin.IN, Pin.PULL_DOWN)   # 右按鍵
BOTTON_SETTING = Pin(14, Pin.IN, Pin.PULL_DOWN) # 設定按鍵
BOTTON_EXIT = Pin(15, Pin.IN, Pin.PULL_DOWN)    # 取消按鍵
BOTTON_LIST = {"BOTTON_HEAD":0,
               "BOTTON_SETTING":0,
               "BOTTON_EXIT":0,
               "BOTTON_UP":0,
               "BOTTON_DOWN":0,
               "BOTTON_LEFT":0,
               "BOTTON_RIGHT":0}                # 按鈕列表
BOTTON_CLICK_MS = 500                           # (MS)按鈕點擊毫秒

# LED參數
LED_GREEN = Pin(19, machine.Pin.OUT)  # 綠
LED_YELLOW = Pin(20, machine.Pin.OUT) # 黃
LED_RED = Pin(21, machine.Pin.OUT)    # 紅

# 蜂鳴器
BEEP = Pin(22, machine.Pin.OUT)

#全域變數，請勿更動
LB_CONV_G = 0
TENSION_MON = 0
MOTO_MOVE = 0
MOTO_BACK = 0
MOTO_WAIT = 0
MOTO_STEPS = 0
CURSOR_XY_TMP = 0
CURSOR_XY_TS_TMP = 1
HX711_I = 0
TENSION_COUNTS = 0
TIMER = 0
TIMER_DIFF = 0
ERR_MSG = ""
ABORT_LM = 0
TS_ARR = []
LOGS = []
TENSION_MON_TMP = 0

# 2004 i2c LCD 螢幕參數設定
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# HX711 張力傳感器參數
hx = hx711(Pin(27), Pin(26))
hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_80)

# 參數讀取
def config_read():
    try:
        file = open(CFG_NAME, "r")
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

# 參數寫入
def config_save():
    try:
        file = open(CFG_NAME, "w")
        save_cfg = ""
        for val in SAVE_CFG_ARRAY:
            save_cfg = save_cfg + val +"=" + str(globals()[val]) + ","

        file.write(save_cfg)
        file.close()
    except OSError:  # failed
       pass

# LOG儲存
def logs_save(log_str, flag):
    try:
        file = open(LOG_NAME, flag)
        for element in reversed(log_str):
            save_log = ""
            for val in element:
                save_log = save_log + str(val) + ","

            file.write(save_log[:-1] + "\n") 
        file.close()
    except OSError:  # failed
       pass
    

# LOG讀取
def logs_read():
    global LOGS
    try:
        fp = open(LOG_NAME, "r")
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

# 有源蜂鳴器
def beepbeep(run_time):
    BEEP.on()
    time.sleep(run_time)
    BEEP.off()

# 張力顯示
def tension_info():
    show_lcd("{: >5d}G".format(TENSION_MON), 14, 3, 6)
    show_lcd("{: >4.1f}".format(TENSION_MON * 0.0022), 9, 0, 4)
    show_lcd("{: >4.1f}".format(TENSION_MON / 1000), 9, 1, 4)
    
# 步進馬達旋轉
def setStep(in_w):
    IN1.value(in_w[0])
    IN2.value(in_w[1])
    IN3.value(in_w[2])
    IN4.value(in_w[3])

# 張力增加
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
            
            # 停止條件
            if botton_list('BOTTON_HEAD') or botton_list('BOTTON_EXIT'):
                show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
                moto_goto_standby(init, 0)
                MOTO_MOVE = 0
                MOTO_WAIT = 0
                return("Abort")
            
            # 張力傳感器異常、無夾線(行程已過ABORT_LM時張力小於5磅)
            if i > ABORT_LM and TENSION_MON < 2267:
                show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
                moto_goto_standby(init, 0)
                MOTO_MOVE = 0
                MOTO_WAIT = 0
                return("No String?")
        
        # 後限位SW
        if MOTO_SW_REAR.value():
            show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
            moto_goto_standby(init, 0)
            if init:
                return i
                
            MOTO_MOVE = 0
            MOTO_WAIT = 0
            return(1)
        
        # 超過最大指定張力後復位
        if ABORT_GRAM < TENSION_MON:
            show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
            moto_goto_standby(init, 0)
            show_lcd("Exceeding "+ str(ABORT_GRAM) +"G, Abort.", 0, 2, I2C_NUM_COLS)
            MOTO_MOVE = 0
            MOTO_WAIT = 0
            return(1)
        
        setStep(MOTO_FORW_W[0])
        setStep(MOTO_FORW_W[1])
        setStep(MOTO_FORW_W[2])
        setStep(MOTO_FORW_W[3])
        time.sleep(delay)

# 張力減少
def backward(delay, steps, check, init):
    global MOTO_BACK, MOTO_STEPS
    LED_GREEN.off()
    MOTO_BACK = 1
    for i in range(0, steps):
        if check == 1:
            if MOTO_SW_FRONT.value():
                if init == 1:
                    MOTO_STEPS = i
                    
                forward(MOTO_SPEED, MOTO_RS_STEPS, 0, 0)
                MOTO_BACK = 0
                return 0 
            
        setStep(MOTO_BACK_W[0])
        setStep(MOTO_BACK_W[1])
        setStep(MOTO_BACK_W[2])
        setStep(MOTO_BACK_W[3])
        time.sleep(delay)

# 滑台復位
def moto_goto_standby(init, reset):
    global HX711_I
    LED_YELLOW.on()
    backward(MOTO_SPEED, MOTO_MAX_STEPS, 1, init)
    if reset == 1:
        time.sleep(1)
        HX711_I = 0
    
    beepbeep(0.1)
    LED_YELLOW.off()
    LED_GREEN.on()

# LCD 顯示
def show_lcd(text, x, y, length):
    text = text[:length]
    text = f'{text :{" "}<{length}}'
    lcd.move_to(x, y)
    lcd.putstr(text)

# 按鈕偵測
def botton_list(key):
    global BOTTON_LIST
    if BOTTON_LIST[key]:
        BOTTON_LIST[key] = 0
        return True
    else:
        return False
    
# 張力監控
def tension_monitoring():
    global TENSION_MON, MOTO_WAIT, HX711_I, BOTTON_LIST, TENSION_MON_TMP
    v0_arr = []
    HX711_I = 0
    while True:
        if val := hx.get_value_noblock():
            if HX711_I <= 10:
                v0_arr.append(val)
                if HX711_I == 10:
                    v0_arr = sorted(v0_arr)
                    v0 = v0_arr[5]
                    v0_arr = []
                    
                HX711_I = HX711_I + 1
            else:
                TENSION_MON = int((val-(v0))/100*(HX711_CAL/20))
                if MOTO_MOVE == 1:
                    if LB_CONV_G < (TENSION_MON * CORR_COEF):
                        TENSION_MON_TMP = TENSION_MON
                        MOTO_WAIT = 1
        
        # 按鍵偵測
        for key in BOTTON_LIST:
            if globals()[key].value() == 1:
                BOTTON_LIST[key] = time.ticks_ms()
            elif BOTTON_LIST[key]:
                if (time.ticks_ms() - BOTTON_LIST[key]) > BOTTON_CLICK_MS:
                    BOTTON_LIST[key] = 0

        time.sleep(0.02)

def lb_kg_select():
    global TS_ARR
    if LB_KG_SELECT == 1:
        TS_ARR = TS_LB_ARR + TS_PS_ARR
    elif LB_KG_SELECT == 2:
        TS_ARR = TS_KG_ARR + TS_PS_ARR
    else:
        TS_ARR = TS_LB_ARR + TS_KG_ARR + TS_PS_ARR

# 開機初始化
def init():
    global LB_CONV_G, TS_ARR, ERR_MSG, ABORT_LM
    config_read()
    logs_read()
    lb_kg_select()
    show_lcd(" **** PicoBETH **** ", 0, 0, I2C_NUM_COLS)
    show_lcd("Version: " + VERSION, 0, 1, I2C_NUM_COLS)
    show_lcd("Date: " + str(VER_DATE), 0, 2, I2C_NUM_COLS)
    LED_RED.on()
    LED_YELLOW.on()
    LED_GREEN.on()
    time.sleep(0.5)
    LED_YELLOW.off()
    LED_GREEN.off()
    moto_goto_standby(0, 0)
    show_lcd("Checking motor...", 0, 2, I2C_NUM_COLS)
    max_lm = forward(MOTO_SPEED, MOTO_MAX_STEPS, 0, 1)
    ABORT_LM = (max_lm * 0.3)
    main_interface()
    LB_CONV_G = int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100))
    show_lcd("Tension monitoring...", 0, 2, I2C_NUM_COLS)
    _thread.start_new_thread(tension_monitoring, ())
    time.sleep(0.5)
    if abs(TENSION_MON) > 10:
        show_lcd("Reset Tension Sensor", 0, 2, I2C_NUM_COLS)
        moto_goto_standby(init, 1)
        time.sleep(1)
        if abs(TENSION_MON) > 10:
            ERR_MSG = "Tension Sensor Error"
            show_lcd("{: >5d}G".format(TENSION_MON), 14, 3, 6)
        
    LED_RED.off()
    show_lcd("Ready", 0, 2, I2C_NUM_COLS)
    beepbeep(1)

# 開始增加張力
def start_tensioning():
    global MOTO_MOVE, MOTO_WAIT, TENSION_COUNTS, LOGS
    show_lcd("Tensioning", 0, 2, I2C_NUM_COLS)
    LED_YELLOW.on()
    beepbeep(0.1)
    if FT_AUTO == 1:
        manual_flag = 0
    else:
        manual_flag = 1
    
    if TIMER:
        TIMER_DEFF = time.time() - TIMER
    else:
        TIMER_DEFF = 0
        
    rel = forward(MOTO_SPEED, MOTO_MAX_STEPS, 1, 0)
    log_lb_max = int(TENSION_MON_TMP * CORR_COEF)
    if rel:
        show_lcd(str(rel), 0, 2, I2C_NUM_COLS)
        return 0

    MOTO_MOVE = 0
    beepbeep(0.3)
    tension_info()
    show_lcd("Target Tension", 0, 2, I2C_NUM_COLS)
    show_lcd("S:   ", 15, 1, 5)
    time.sleep(PU_STAY)
    check_g = int(DEFAULT_LB * 453.59237)
    ft_flag = 0
    abort_flag = 0
    count_add = 0
    count_sub = 0
    t0 = time.time()
    # 到達指定張力，等待
    while True:  
        # 張力不足加磅
        if check_g > TENSION_MON and manual_flag == 0:
            diff_g = check_g - TENSION_MON
            if diff_g < (FT_LB * 453):
                ft_flag = 0
            else:
                ft_flag = 1
            
            abort_flag = forward(MOTO_SPEED, FT_ADD, 0 ,0)
            count_add = count_add + 1
        
        # 張力超過減磅
        if (check_g + PU_PRECISE) < TENSION_MON and manual_flag == 0:
            diff_g =  TENSION_MON - check_g
            if diff_g < (FT_LB * 453):
                ft_flag = 0
            else:
                ft_flag = 1
            
            backward(MOTO_SPEED, FT_ADD * FT_SUB_COEF, 1, 0)
            count_sub = count_sub + 1
                        
        # 手動加磅
        if botton_list('BOTTON_UP'):
            manual_flag = 1
            forward(MOTO_SPEED, FT_ADD, 0, 0)
            show_lcd(AM_ARR[FT_AUTO], 11, 3, 1)
            count_add = count_add + 1
            
        # 手動減磅
        if botton_list('BOTTON_DOWN'):
            manual_flag = 1
            backward(MOTO_SPEED, FT_ADD * FT_SUB_COEF, 1, 0)
            show_lcd(AM_ARR[FT_AUTO], 11, 3, 1)
            count_sub = count_sub + 1
            
        # 手動改自動微調
        if botton_list('BOTTON_SETTING'):
            if manual_flag == 1:
                manual_flag = 0
            else:
                manual_flag = 1
                
            show_lcd(AM_ARR[FT_AUTO], 11, 3, 1)
            beepbeep(0.1)
        
        # 夾線頭按鈕取消按鈕
        if botton_list('BOTTON_HEAD') or botton_list('BOTTON_EXIT'):
            log_s = time.time() - t0
            show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
            moto_goto_standby(init, 0)
            show_lcd("Ready", 0, 2, I2C_NUM_COLS)
            show_lcd("     ", 15, 1, 5)
            MOTO_WAIT = 0
            TENSION_COUNTS = TENSION_COUNTS + 1
            config_save()
            #LOG寫入
            LOGS.insert(0, [TENSION_COUNTS, TIMER_DEFF, LB_KG_SELECT, DEFAULT_LB, log_lb_max, PRE_STRECH, log_s, count_add, count_sub, CORR_COEF, HX711_CAL, FT_ADD])
            logs_save([LOGS[0]], "a")
            if len(LOGS) > LOG_MAX:
                LOGS = LOGS[:LOG_MAX]
            
            return 0
        
        # 斷線(已達指定張力突然小於5磅)
        if TENSION_MON < 2267:
            show_lcd("Resetting...", 0, 2, I2C_NUM_COLS)
            moto_goto_standby(init, 0)
            show_lcd("String Broken?", 0, 2, I2C_NUM_COLS)
            show_lcd("     ", 15, 1, 5)
            MOTO_WAIT = 0
            return 0
        
        if abort_flag == 1:
            return 0  
        
        if count_add == 0 and count_sub == 0:
            tension_info()
        elif ft_flag:
            time.sleep(0.1)
        else:
            tension_info()
        
        t1 = time.time() - t0
        show_lcd("{: >3d}".format(t1), 17, 1, 3)

# 主畫面張力及預拉設定
def setting_ts():
    global DEFAULT_LB, PRE_STRECH, LB_CONV_G, CURSOR_XY_TS_TMP
    last_set_time = time.ticks_ms()
    set_count = len(TS_ARR)
    i = CURSOR_XY_TS_TMP
    cursor_xy = TS_ARR[i][0], TS_ARR[i][1]
    lcd.move_to(TS_ARR[i][0], TS_ARR[i][1])
    lcd.blink_cursor_on()
    while True:
        # 按下上下鍵動作
        if BOTTON_UP.value() or BOTTON_DOWN.value():
            kg = round(DEFAULT_LB * 0.45359237, 1)
            # LB 10位數設定
            if cursor_xy == (4, 0):
                if BOTTON_UP.value():
                    DEFAULT_LB = DEFAULT_LB + 10
                elif BOTTON_DOWN.value():
                    DEFAULT_LB = DEFAULT_LB - 10
            
            # LB 個位數設定
            elif cursor_xy == (5, 0):
                if BOTTON_UP.value():
                    DEFAULT_LB = DEFAULT_LB + 1
                elif BOTTON_DOWN.value():
                    DEFAULT_LB = DEFAULT_LB - 1
            
            # LB 小數設定
            elif cursor_xy == (7, 0):
                if BOTTON_UP.value():
                    DEFAULT_LB = DEFAULT_LB + 0.1
                elif BOTTON_DOWN.value():
                    DEFAULT_LB = DEFAULT_LB - 0.1
                    
            # KG 十位數設定
            elif cursor_xy == (4, 1):
                if BOTTON_UP.value():
                    kg = kg + 10
                elif BOTTON_DOWN.value():
                    kg = kg - 10
                    
                DEFAULT_LB = round(kg * 2.20462262, 1)

            # KG 個位數設定
            elif cursor_xy == (5, 1):
                if BOTTON_UP.value():
                    kg = kg + 1
                elif BOTTON_DOWN.value():
                    kg = kg - 1
                    
                DEFAULT_LB = round(kg * 2.20462262, 1)
            
            # KG 小數設定
            elif cursor_xy == (7, 1):
                if BOTTON_UP.value():
                    kg = kg + 0.1
                elif BOTTON_DOWN.value():
                    kg = kg - 0.1
                    
                DEFAULT_LB = round(kg * 2.20462262, 1)
                
            # 預拉10位數設定
            elif cursor_xy == (17, 0):
                if BOTTON_UP.value():
                    PRE_STRECH = PRE_STRECH + 10
                elif BOTTON_DOWN.value():
                    PRE_STRECH = PRE_STRECH - 10
                
            # 預拉個位數設定
            elif cursor_xy == (18, 0):
                if BOTTON_UP.value():
                    PRE_STRECH = PRE_STRECH + 1
                elif BOTTON_DOWN.value():
                    PRE_STRECH = PRE_STRECH - 1
            
            if DEFAULT_LB >= LB_MAX:
                DEFAULT_LB = LB_MAX  
            elif DEFAULT_LB <= LB_MIN:
                DEFAULT_LB = LB_MIN
                
            if PRE_STRECH >= PS_MAX:
                PRE_STRECH = PS_MAX
            elif PRE_STRECH <= 0:
                PRE_STRECH = 0
            
            show_lcd("{:.1f}".format(DEFAULT_LB), 4, 0, 4)
            show_lcd("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
            show_lcd("{: >2d}".format(PRE_STRECH), 17, 0, 2)
            lcd.move_to(TS_ARR[i][0],TS_ARR[i][1])
            LB_CONV_G = int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100))
            last_set_time = time.ticks_ms()
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)

        # 按下左右鍵動作
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

        # 按下離開鍵動作
        if botton_list('BOTTON_EXIT') or ((time.ticks_ms() - last_set_time) > (AUTO_SAVE_SEC * 1000)):
            config_save()
            lcd.blink_cursor_off()
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)
            return 0

# 設定頁面
def setting():
    global CURSOR_XY_TMP, CORR_COEF, HX711_CAL, LB_KG_SELECT, FT_ADD, CURSOR_XY_TS_TMP, FT_AUTO
    set_count = len(MENU_ARR)
    i = CURSOR_XY_TMP
    cursor_xy = MENU_ARR[i][0], MENU_ARR[i][1]
    lcd.move_to(MENU_ARR[i][0], MENU_ARR[i][1])
    lcd.blink_cursor_on()
    time.sleep(BOTTON_SLEEP)
    while True:
        # 按下上下鍵動作
        if BOTTON_UP.value() or BOTTON_DOWN.value() or botton_list('BOTTON_HEAD') or botton_list('BOTTON_SETTING'):
            # 張力校正系數個位數
            if cursor_xy == (5, 1):
                if BOTTON_UP.value():
                    CORR_COEF = CORR_COEF + 1
                elif BOTTON_DOWN.value():
                    CORR_COEF = CORR_COEF - 1
            
            # 張力校正系數小數第一位
            elif cursor_xy == (7, 1):
                if BOTTON_UP.value():
                    CORR_COEF = CORR_COEF + 0.1
                elif BOTTON_DOWN.value():
                    CORR_COEF = CORR_COEF - 0.1
                    
            # 張力校正系數小數第二位
            elif cursor_xy == (8, 1):
                if BOTTON_UP.value():
                    CORR_COEF = CORR_COEF + 0.01
                elif BOTTON_DOWN.value():
                    CORR_COEF = CORR_COEF - 0.01
                    
            # 張力校正系數自動測試
            elif cursor_xy == (4, 1):
                if BOTTON_UP.value() or BOTTON_DOWN.value() or BOTTON_HEAD.value():
                    beepbeep(0.1)
                    time.sleep(0.5)
                    tmp_CORR_COEF = CORR_COEF
                    CORR_COEF = 1
                    ret = forward(MOTO_SPEED, MOTO_MAX_STEPS, 1, 0)
                    if ret == 0:
                        time.sleep(PU_STAY)
                        CORR_COEF = round(((TENSION_MON/((100+PRE_STRECH)/100))/(DEFAULT_LB*453.59)), 2)
                        moto_goto_standby(init, 0)
                    else:
                        show_lcd("HX: "+ "{: >2.2f}".format(HX711_CAL), 0, 2, I2C_NUM_COLS)
                        CORR_COEF = tmp_CORR_COEF
            
            # 磅、公斤設定選擇
            elif cursor_xy == (4, 0):
                if BOTTON_UP.value() or BOTTON_DOWN.value():
                    CURSOR_XY_TS_TMP = 1
                    LB_KG_SELECT = (LB_KG_SELECT + 1) % 3
                    show_lcd(UNIT_ARR[LB_KG_SELECT], 4, 0, 5)
                    lb_kg_select()

            # 張力微調步數十位數
            elif cursor_xy == (15, 0):
                if BOTTON_UP.value():
                    FT_ADD = FT_ADD + 10
                elif BOTTON_DOWN.value():
                    FT_ADD = FT_ADD - 10

            # 張力微調步數個位數
            elif cursor_xy == (16, 0):
                if BOTTON_UP.value():
                    FT_ADD = FT_ADD + 1
                elif BOTTON_DOWN.value():
                    FT_ADD = FT_ADD - 1
                    
            # 張力微調開關
            elif cursor_xy == (15, 1):
                if BOTTON_UP.value() or BOTTON_DOWN.value():
                    if FT_AUTO == 1:
                        FT_AUTO = 0
                    else:
                        FT_AUTO = 1
                        
                    show_lcd(ONOFF_ARR[FT_AUTO], 15, 1, 3)

            # HX711校正系數十位數
            if cursor_xy == (4, 2):
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 10
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 10
                    
            # HX711校正系數個位數
            if cursor_xy == (5, 2):
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 1
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 1
            
            # HX711校正系數個位數
            elif cursor_xy == (7, 2):
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 0.1
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 0.1
                    
            # HX711校正系數個位數
            elif cursor_xy == (8, 2):
                if BOTTON_UP.value():
                    HX711_CAL = HX711_CAL + 0.01
                elif BOTTON_DOWN.value():
                    HX711_CAL = HX711_CAL - 0.01

            # LOG顯示
            elif cursor_xy == (19, 3):
                if BOTTON_SETTING.value():
                    beepbeep(0.1)
                    if len(LOGS) != 0:
                        logs_idx = 0
                        lcd.hide_cursor()
                        logs_interface("init")
                        logs_interface(logs_idx)
                        log_flag = 0
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
                                log_flag = logs_idx
                            
                        setting_interface()
                        lcd.show_cursor()
                        lcd.blink_cursor_on()

            if CORR_COEF >= CORR_MAX:
                CORR_COEF = CORR_MAX  
            elif CORR_COEF <= CORR_MIN:
                CORR_COEF = CORR_MIN
                
            if HX711_CAL >= HX711_MAX:
                HX711_CAL = HX711_MAX  
            elif HX711_CAL <= HX711_MIN:
                HX711_CAL = HX711_MIN
                
            if FT_ADD >= FT_ADD_MAX:
                FT_ADD = FT_ADD_MAX  
            elif FT_ADD <= FT_ADD_MIN:
                FT_ADD = FT_ADD_MIN
            
            show_lcd("{: >1.2f}".format(CORR_COEF), 5, 1, 4)
            show_lcd("{: >2.2f}".format(HX711_CAL), 4, 2, 5)
            show_lcd("{: >2d}".format(FT_ADD), 15, 0, 2)
            lcd.move_to(MENU_ARR[i][0],MENU_ARR[i][1])
            LB_CONV_G = int((DEFAULT_LB * 453.59237) * ((PRE_STRECH + 100) / 100))
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)

        # 按下左右鍵動作
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

        # 按下離開鍵動作
        if botton_list('BOTTON_EXIT'):
            config_save()
            lcd.blink_cursor_off()
            beepbeep(0.1)
            time.sleep(BOTTON_SLEEP)
            return 0
     
# 設定介面顯示
def setting_interface():
    show_lcd("UN:        FT: "+ "{: >2d}".format(FT_ADD), 0, 0, I2C_NUM_COLS)
    show_lcd(UNIT_ARR[LB_KG_SELECT], 4, 0, 5) 
    show_lcd("CC: A"+ "{: >1.2f}".format(CORR_COEF) + "  AT: " + ONOFF_ARR[FT_AUTO], 0, 1, I2C_NUM_COLS)
    show_lcd("HX: "+ "{: >2.2f}".format(HX711_CAL), 0, 2, I2C_NUM_COLS)
    show_lcd("<PicoBETH>    "+ "{: >5d}".format(TENSION_COUNTS) +"T", 0, 3, I2C_NUM_COLS)
    
# LOG介面顯示
def logs_interface(idx):
    if idx=="init":
        show_lcd("  LOG  TIMER:   m  s", 0, 0, I2C_NUM_COLS)
        show_lcd("LB:    /      PS:  %", 0, 1, I2C_NUM_COLS)
        show_lcd("FT:  /  /      S:   ", 0, 2, I2C_NUM_COLS)
        show_lcd("ST:    /           T", 0, 3, I2C_NUM_COLS)
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
        
        show_lcd(str(LOGS[idx][5]), 17, 1, 2)
        show_lcd("{: >3d}".format(int(LOGS[idx][6])), 17, 2, 3)
        show_lcd("{: >2d}".format(int(LOGS[idx][7])), 3, 2, 2)
        show_lcd("{: >2d}".format(int(LOGS[idx][8])), 6, 2, 2)
        show_lcd(str(LOGS[idx][11]), 9, 2, 2)
        show_lcd(str(LOGS[idx][9]), 3, 3, 4)
        show_lcd(str(LOGS[idx][10]), 8, 3, 5)
        show_lcd("{: >5d}".format(int(LOGS[idx][0])), 14, 3, 5)

# 設定主畫面顯示
def main_interface():
    show_lcd("LB:     /--.- PS:  %", 0, 0, I2C_NUM_COLS)
    show_lcd("KG:     /--.-       ", 0, 1, I2C_NUM_COLS)
    show_lcd("                    ", 0, 2, I2C_NUM_COLS)
    show_lcd("<PicoBETH> "+ AM_ARR[FT_AUTO] +"        ", 0, 3, I2C_NUM_COLS)
    show_lcd("{:.1f}".format(DEFAULT_LB), 4, 0, 4)
    show_lcd("{: >4.1f}".format(DEFAULT_LB * 0.45359237), 4, 1, 4)
    show_lcd("{: >2d}".format(PRE_STRECH), 17, 0, 2)

def show_timer():
    if TIMER:
        show_lcd("   m  ", 14, 1, 6)
        TIMER_DEFF = timer_flag - TIMER
        if TIMER_DEFF < 0:
            return 0
        
        show_lcd("{: >3d}".format(int(TIMER_DEFF / 60)), 14, 1, 3)
        show_lcd("{: >2d}".format(TIMER_DEFF % 60), 18, 1, 2)

init()
ts_info_time = time.ticks_ms()
timer_flag = 0
while True:
    # 開始張緊
    if botton_list('BOTTON_HEAD'):
        start_tensioning()
        show_timer()
    
    # 設定模式
    if botton_list('BOTTON_SETTING'):
        beepbeep(0.1)
        setting_interface()
        setting()
        main_interface()
        show_lcd("Ready", 0, 2, I2C_NUM_COLS)
        show_timer()
    
    # 計時器開關
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
    
    # 加減磅設定
    if botton_list('BOTTON_UP') or botton_list('BOTTON_DOWN') or botton_list('BOTTON_LEFT') or botton_list('BOTTON_RIGHT'):
        setting_ts()
    
    # 張力顯示更新
    if (time.ticks_ms() - ts_info_time) > TS_INFO_MS:
        tension_info()
        if TIMER:
            if timer_flag == 0:
                TIMER_DEFF = time.time() - TIMER
                show_lcd("{: >3d}".format(int(TIMER_DEFF / 60)), 14, 1, 3)
                show_lcd("{: >2d}".format(TIMER_DEFF % 60), 18, 1, 2)
        
        lcd.move_to(TS_ARR[CURSOR_XY_TS_TMP][0], TS_ARR[CURSOR_XY_TS_TMP][1])
        lcd.show_cursor()
        ts_info_time = time.ticks_ms()
        
    if ERR_MSG:
        show_lcd(ERR_MSG, 0, 2, I2C_NUM_COLS)
        break

