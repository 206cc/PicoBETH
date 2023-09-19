# PicoBETH
PicoBETH (Raspberry Pico Badminton Electronic Tension Head) 是一個開源的項目，讓喜歡穿線，但只有機械式穿線機（重錘式、手搖式）的業餘穿線師可以自行製作電子拉線機頭，如果你有一些基本的程式能力，這個項目會很容易完成。

![images1-1](docs/images1-1.jpg)

![images1-2](docs/images1-2.jpg)

15磅、25磅、30磅展示影片
<youtube>

## 原由
一年前因為公司社團的關係，開始打羽毛球，球技不怎麼好卻迷上的穿線，買了一台重錘式穿線機，原本想購買電子拉線機頭，後來想想我可以用我會的知識，在 Raspberry Pico 上使用壓力傳感器、幾個微動開關和按鈕製作了這個項目。

## 現有主要功能如下：

1. 使用磅或公斤的單位進行張力設定
2. 預拉(Pre-Strech)功能
3. 張緊後的自動微調補磅減磅功能
4. 張力歸零
5. 張力系數設定
6. 張力校正

## 張緊畫面
![images1-3](docs/images1-3.png)

## 設定畫面
![images1-4](docs/images1-4.png)
 
## 硬體

主要材料
1. Raspberry Pico H
2. 1605 200MM 滑台 / 1605 Sliding Table 200MM 
3. 57步進馬達 / 57 Stepper Motor 
4. TB6600 步進馬達驅動器 / TB6600 Stepper Motor Driver
5. NJ5 20KG 壓力傳感器 / NJ5 20KG load cell
6. HX711 模塊 / HX711 IC
7. 2004 i2c LCD 
8. WISE 2086 珠夾頭 / WISE 2086 Head
9. 5向按鍵模組 / Five-way key
10. 按鈕 / Button
11. 微控開關 / Micro Switch
12. 有源蜂鳴器 / Active buzzer
13. 三色 LED / Tri-Color LEDs

![images2-1](docs/images2-1.jpg)

## 接線圖
![images2-2](docs/images2-2.png)
> [!WARNING]
> 請適時增加安全措施，例如增加按鍵的上拉電阻、步進馬達的保險絲之類

## TB6600 步進馬達電機參數
![images2-3](docs/images2-3.png)

> [!WARNING]
> 如修改此電機參數，程式碼可能會有許多要修正的地方

# 軟體安裝
將程式碼使用 Thonny 儲存到 Raspberry PICO中，其中 src 資料夾是 hx711 及 2004 LCD 用到的相關函式庫
> [!NOTE]
> 感謝 [https://github.com/endail/hx711-pico-mpy](https://github.com/endail/hx711-pico-mpy) 提供 hx711 for pico 的函式庫

> [!NOTE]
> 感謝 [https://github.com/T-622/RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) 提供 2004 LCD for pico 的函式庫

# 第一次開機

## 校正HX參數

HX711壓力感應器校正系數，第一次使用或有更換壓力傳感器、HX711電路板時務必重新校正一次
校正方法：
1.	將外接式張力計，一端綁在拉線機上，另一端綁上羽毛球線
2. 先將LCD設定頁面中HX參數設為20.00
3. 跳回主選單設定拉力為20磅
4. 按上或下鍵開始拉線，當LCD顯示20磅時，抄下張力計顯示數值
5. 至設定頁面上填入剛抄下張力計的數值

> [!WARNING]
> 如不做此校正，實際張力會與LCD上的張力會有誤差

> [!IMPORTANT]
> 此參數以設定存檔為主 config.cfg

參考影片: https://youtube.com/xxxx


## 設定CC參數
當達到指定張力馬達停止時實際張力還會持續變化，另設此需除此係數校正，可手動設設也可自動在設定頁面校正
校正方法:
1. 將羽球線固定好，一端綁在拉線機上，另一端在珠夾上
2. 至LCD設定頁面中CC欄位中AUTO按鍵上按上或下鍵開始拉線
3. AUTO會自動填入參考的CC值
4. 使用此值拉線測式，最佳的結果是預拉為0時達到指定張力不會進行微調動作 (你也許會在馬達停止時看見LCD張力持續變化超過指定張力，這為正常物理現象，最佳的參數在於張力平衡後會線剛好在指定張力不會進行微調的動作)
5. 如果自動的CC值不理想，可至設定頁面手動微調CC值後，重覆4的步驟，找到最佳的值

> [!WARNING]
> 如果有開預拉，會進行退磅的徵調，所以測試時請將預拉設為0

> [!IMPORTANT]
> 更換HX711電路板、滑台螺距、馬達的電機會影響此系數，如果覺得在預拉為0時頻繁微調可校正此值

> [!IMPORTANT]
> 此參數以設定存檔為主 config.cfg

參考影片: https://youtube.com/xxxx

## 待機時張力校正
正常來說待機時顯示器的張力會顯為0±3G，如不穩定或偏差太大，請檢查是否受到干擾或接錯線；如固定在某個超過0太多的數值請重新開機校正，或至設定頁面TS欄位點選RESET校正

# 最後
目前功能已滿足我拉線的需求，應該已不會再增加功能，只持續修正BUG，有興趣的人可自行加入想要的功能。
