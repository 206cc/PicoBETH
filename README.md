[![cht](https://img.shields.io/badge/lang-cht-green.svg)](https://github.com/206cc/PicoBETH/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/206cc/PicoBETH/blob/main/README.en.md)
# PicoBETH
PicoBETH (Raspberry Pico Badminton Electronic Tension Head) 是一個開源項目，讓喜歡穿線，但只有機械式穿線機（重錘式、手搖式）的業餘穿線師可以自行製作電子拉線機頭，如果你有一些基本的程式能力，這個項目會很容易完成。

重錘式穿線機與改裝零件
![images1-1](docs/images1-1.jpg)

改裝完成（原型機）
![images1-2](docs/images1-2.jpg)

正式機
![images1-2](docs/images1-6.jpg)

正式機的改進
1. 增加螺杆防塵罩
2. 螺杆改使用1610規格，增加張力速度
3. 更合理的硬體佈局，各零件可單獨拆裝不需全拆
4. 使用堆疊方式減少體積，不會擋到置物槽
5. 改使用自行設計PCB電路板

穿線展示影片

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ygbpYtNiPa4/0.jpg)](https://www.youtube.com/watch?v=ygbpYtNiPa4)

## 原由
一年前因為公司社團關係，開始打羽毛球，球技不怎麼好卻迷上的穿線，買了一台重錘式穿線機，原本想再購買電子拉線機頭，但後來想想我可以用我會的知識，在 Raspberry Pico 上使用張力傳感器、幾個微動開關、按鈕製作了這個專案。

## 現有主要功能如下：

1. 使用磅或公斤單位設定張力
2. 預拉(Pre-Strech)
3. 張緊後的自動張力微調
4. 張力歸零
5. 張力系數設定
6. 張力校正
7. 穿線計時
8. 張緊次數記錄
9. 張緊LOG的詳細記錄

## 待機畫面
1. 使用左右鍵可設定磅、公斤及預拉的十位數、個位數、小數。
2. 使用上下鍵調整選擇的設定。
3. 穿線計時功能，在按下離開鍵開始計時，再按一下停止計時，按第三下計時器歸零。
![images1-3](docs/images1-3.png)

## 張緊畫面
1. 達到設定張力時自動進入張力微調模式，張力不足增加張力、過高減少張力，直到按下珠夾頭上的按鍵或離開按鍵結束張緊模式。
2. 按五向鍵的中鍵進入手動微調模式，此時自動微調模式會被取消，可按上下鍵手動微調張力；再次按下五向鍵的中鍵後可重新進入自動微調模式。
3. 達到指定張力後會開始出現計算秒數。
![images1-4](docs/images1-4.png)

> [!WARNING]
> 每次的張力微調幅度如太高或太低，可自行調整 FT 參數

## 設定畫面
1. UN: 選擇設定時使用磅或公斤單位
2. CC: 微調參數(詳見第一次開機章節)
3. HX: HX711 的張力傳感器校正(詳見第一次開機章節)
4. FT: 達到指定張力時微調的幅度
![images1-5](docs/images1-5.png)
  
> [!NOTE]
> 一般來說這些參數設定好後就不需要再設定了

## 張緊LOG的詳細記錄
在設定畫面下，使用左右鍵選到張緊次數，再點下五向建的中鍵進入張緊 LOG 記錄頁面  
在頁面下使用左右鍵可瀏覽 LOG 記錄  
TIMER: 如果有開啟計時功能，顯示此張緊時的時間  
LB: 設定張力/停止張力  
PS: 設定預拉值  
FT: 增加張力微調次數/減少張力微調次數/微調參數  
ST: CC參數/HX參數  

![images1-7](docs/images1-7.png)
  
> [!NOTE]
> 預設顯示 1-50 筆 LOG 記錄，如要需調整請修改 LOG_MAX 參數

> [!WARNING]
> LOG_MAX 參數請勿設定過大，開機時如載入過多 LOG 會導致記憶體不足會無開機

## 硬體

主要材料
1. Raspberry Pico H
2. 1610 200MM 滑台 / 1610 Sliding Table 200MM 
3. 57步進馬達(2相4線 1.8°) / 57 Stepper Motor (1.8° Step Angle 2 Phase 4 Line)
4. TB6600 步進馬達驅動器 / TB6600 Stepper Motor Driver
5. NJ5 20KG 張力傳感器 / NJ5 20KG load cell
6. HX711 模塊(紅色抗干擾版本) / Load Cell Amplifier(Red PCB, Anti-Interference Version)
7. 2004 i2c LCD 
8. WISE 2086 珠夾頭 / WISE 2086 Head
9. 5向按鍵模組 / Five-way key
10. 按鈕 / Button
11. 微控開關 / Micro Switch
12. 有源蜂鳴器 / Active buzzer
13. 三色 LED / Tri-Color LEDs

> [!WARNING]
> 除非您有自行修改程式的能力，否則請照指的的型號或規格購買材料

![images2-1](docs/images2-1.jpg)

## 接線圖
![images2-2](docs/images2-2.png)
> [!WARNING]
> 請適時增加安全措施，例如增加按鍵的上拉電阻、步進馬達的保險絲、LED 限流電阻之類保護 Raspberry Pi Pico 及馬達電機

## PCB 電路板
![images2-3](docs/images2-4.svg)

> [!NOTE]
> 您可以自行下載上圖洗電路板，避免手焊電路板的麻煩，如果不會洗板的可上露天拍賣搜尋 PicoBETH

> [!NOTE]
> 此電路板四周的鎖點比照 2004 LCD 鎖點位置，可堆疊減少體積

## TB6600 步進馬達電機參數
![images2-3](docs/images2-3.png)

> [!WARNING]
> 如更改此TB6600電機參數，程式碼可能會有許多要修正的地方

# 軟體安裝
使用 Thonny 將以下程式碼檔案儲存到 Raspberry Pico 中，其中 src 資料夾內是 hx711 及 2004 LCD 的相關函式庫

1. main.py
2. src\hx711.py
3. src\lcd_api.py
4. src\pico_i2c_lcd.py

> [!NOTE]
> 感謝 [https://github.com/endail/hx711-pico-mpy](https://github.com/endail/hx711-pico-mpy) 提供 hx711 for pico 的函式庫

> [!NOTE]
> 感謝 [https://github.com/T-622/RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) 提供 2004 LCD for pico 的函式庫

# 第一次開機

## 校正 HX 參數

HX711 張力感應器校正系數，第一次使用或有更換張力傳感器、HX711 電路板時務必重新校正一次

校正方法：
1. 將外接式張力計，一端綁在拉線機上，另一端綁上羽毛球線
2. 先將 LCD 設定頁面中HX參數設為 20.00
3. 跳回主選單設定拉力為 20 磅
4. 按上或下鍵開始拉線，當 LCD 顯示 20 磅時，抄下張力計顯示數值
5. 至設定頁面上填入剛抄下張力計的數值

> [!WARNING]
> 如不做此校正，實際張力會與 LCD 上的張力會有誤差

> [!IMPORTANT]
> 此參數以設定存檔為主(config.cfg)

參考影片: [https://youtu.be/JaplgmXzbjY](https://youtu.be/JaplgmXzbjY)

## 設定 CC 參數
當達到指定張力馬達停止時實際張力還會持續變化，另設此需除此係數校正，可手動設設也可自動在設定頁面校正

校正方法:
1. 將羽球線固定好，一端綁在拉線機上，另一端在珠夾上
2. 至 LCD 設定頁面中 CC 欄位中 AUTO 按鍵上按上或下鍵開始拉線
3. AUTO 會自動填入參考的 CC 值
4. 使用此值拉線測式，最佳的結果是預拉為 0 時達到指定張力不會進行微調動作
   (你也許會在馬達停止時看見 LCD 張力持續變化超過指定張力，這為正常物理現象，最佳的參數在於張力平衡後會線剛好在指定張力不會進行微調的動作)
5. 如果自動的CC值不理想，可至設定頁面手動微調CC值後，重覆4的步驟，找到最佳的值

> [!WARNING]
> 如果有開預拉，會進行退磅的徵調，所以測試時請將預拉設為 0

> [!IMPORTANT]
> 更換 HX711 電路板、滑台螺距、馬達的電機會影響此系數，如果覺得在預拉為0時頻繁微調可校正此值

> [!IMPORTANT]
> 此參數以設定存檔為主(config.cfg)

參考影片: [https://youtu.be/KuisR6eKiwk](https://youtu.be/KuisR6eKiwk)

# 最後
如果有製作上的問題，歡迎留言討論，也可以寫信給我詢問。
