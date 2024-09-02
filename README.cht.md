![images1-1](docs/Pico_Logo.png)

[![cht](https://img.shields.io/badge/lang-cht-green.svg)](https://github.com/206cc/PicoBETH/blob/main/README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/206cc/PicoBETH/blob/main/README.md)
# PicoBETH
PicoBETH (Raspberry Pico Badminton Electronic Tension Head) 是一個開源項目，讓喜歡穿線，但只有機械式穿線機（重錘式、手搖式）的業餘穿線師可以自行製作電子拉線機頭，如果你有一些基本的程式能力，這個項目會很容易完成。

> 設計理念：便宜、簡單、精準

## 現有主要功能與特點

[![DEMO VIDEO](https://img.youtube.com/vi/pWgD_OSyc1g/0.jpg)](https://www.youtube.com/watch?v=pWgD_OSyc1g)

### 功能
- **磅/公斤顯示及設定**
- **預拉(Pre-Strech)**
- **自動恆拉(Constant-Pull)**
- **打結加磅(Knot)**
- **張緊時手動調整張力**
- **張力校正**
- **穿線計時器**
- **張力計時器**
- **張力計數器和開機計數器**
- **張緊LOG的詳細記錄**
- **9段速度切換**

### 特點
- **0.05LB 高精度**
  - 在 94Hz Sparkfun HX711 及軟體版本 V2.2 之後
  - [參考影片](https://youtu.be/Hk7eMABAxT0)
- **低功耗**
  - 僅需 DC19V4A 電源*
- **UPS不斷電**
  - 使用 18650x6 電池可保證至少完整的穿完一隻球拍
- **緊湊不佔空間**
  - 尺寸大小約為 38(L) x 15(W) x 9(H) CM(不含珠夾頭)

> [!CAUTION]
> 在 2.70 版本之後的**快速模式**下，當速度設置在 **L7** 以上且**張力超過 30LB** 時，原本的 12V3A 電源不足以支持，可能導致馬達打滑。因此，此版本已更換為 19V4A 的電源。如果你也打算更換為 19V 電源，請務必確認你的 5V 電源轉換器能承受 19V 的輸入電壓。此外，如果你使用外接 UPS 電源，也應更換為可接受 19V 輸入輸出的版本。

## 開發項目計劃

| 計劃項目           | 進度     | 備註                           |
| ------------------ | -------- | ------------------------------ |
| 可靠度測試         | 進行中   | 目前張緊次數 125,000+ (2024/08/30) [測試影片](https://youtu.be/4xY9-XTofpA)|
| 適用網球拍         | 尚未開始 | 零件採購中                     |
| 相容 Pico 2       | 尚未開始 |                      |

### 已知問題
- 如果在L9速度下偶爾出現馬達打滑的情況，請降低速度。

## 原由
一年前，由於參加公司社團，我開始接觸羽毛球。雖然球技平平，但我對穿線產生了濃厚的興趣。當時購買了一台重錘式穿線機，原本打算再購買一個電子拉線機頭，但後來我決定利用自己掌握的知識，結合 Raspberry Pico、張力傳感器、微動開關和按鈕來製作這個專案。

**重錘式穿線機與改裝零件**
![img_parts](docs/img_parts.jpg)

**改裝完成（開發中）**
![img_dev_machine](docs/img_dev_machine.jpg)

**正式機** [製作合集](https://youtu.be/uJVE3YFJtJA)
![img_final_machine](docs/img_final_machine.jpg)

**穿線展示影片**

[![VIDEO](https://img.youtube.com/vi/ygbpYtNiPa4/0.jpg)](https://www.youtube.com/watch?v=ygbpYtNiPa4)

> [!NOTE]
> 如果你沒有穿線機，可以參考此專案做一個穿線機台 [Pico-Badminton-Stringer](https://github.com/HsuKaoPang/Pico-Badminton-Stringer)

> [!NOTE]
> 如果你現在正在考慮選擇手動穿線機，我建議選購具備六點固定和底座夾具的重錘式穿線機。重錘式機型具備一定的恆拉效果，穿出的球拍張力與電子穿線機相比差異不大。在完成這個專案之前，你可以先使用重錘式機器來熟悉穿線操作。將來如果電子穿線頭出現故障，你也能迅速恢復使用重錘式機器。

## 警告
如果你的羽毛球穿線機結構不夠堅固，我非常不建議繼續這個專案。一個不堅固的固定平台在張緊時會發生形變，導致球拍框架變圓、張緊度降低。最終，機器會補償張力，形成惡性循環，直到羽毛球拍斷裂。

> [!CAUTION]
> 非常重要，如果您的穿線機台是簡易型的，請務必補強結構。

> [!CAUTION]
> 非常重要，如果您的穿線機台是簡易型的，請務必補強結構。

> [!CAUTION]
> 非常重要，所以說三次，如果您的穿線機台是簡易型的，請務必補強結構。

## 操作介面

以下展示 V2.70 版本的操作介面

### 主畫面

- 按下離開鍵以啟用計時功能，再次按下以停止計時，第三次按下時計時器將歸零。

![img_main](docs/img_main.jpg)

1. 設定磅數
2. 設定公斤
3. 狀態顯示
4. PS=預拉功能 KT=打結功能
5. 穿線計時器時間
6. 恆拉狀態 C=啟用 M=停用
7. 珠夾頭移動速度 1=最慢 9=最快
8. 目前張力值(公克)

### 張力設定畫面

- 按下五向鍵進入張力設定模式，第一次按下時僅顯示包含預拉的最大張力，第二次按下則開始調整張力和預拉設定。
- 預拉功能(PS)及打結功能(KT)使用上下鍵切換，打結功能用完後會自動切回預拉功能。

![img_lbset](docs/img_lbset.jpg)

1. 磅數設定，含預拉的最大張力
2. 公斤設定，含預拉的最大張力

### 張緊中畫面

- 當達到設定的張力時，會進入恆拉模式；如果張力不足，系統會自動增加張力，張力過高則會自動減少張力。這個過程會持續，直到你按下珠夾頭上的按鍵或離開鍵來結束張緊模式。
- 按下五向鍵的中鍵會停用恆拉系統，再次按下中鍵即可重新啟用恆拉系統。。
- 按下五向鍵的上下鍵一次會加減 0.5LB

![img_tensioning](docs/img_tensioning.jpg)

1. 設定張力
2. 目前張力
3. 達到指定張力後會開始出現計算秒數
4. 恆拉狀態 C=啟用 M=停用
5. 珠夾頭移動速度 1=最慢 9=最快
6. 與設定張力相差公克數，超過99G顯示 +++ ，低於 99G 顯示 ---

### 設定畫面

![img_setting](docs/img_setting.jpg)

1. SP: 珠夾頭移動速度 1=最慢 9=最快
2. CP: 恆拉開關
3. BZ: 蜂鳴器開關
4. UN: 在主畫面中使用磅或公斤進行設定。
5. HX: HX711 的張力傳感器校正(詳見最後設定章節)
6. I: 系統資訊
7. T: 總張緊計數/Log記錄

### 張緊LOG的詳細記錄

![img_tslog](docs/img_tslog.jpg)

1. LOG編號
2. 此次張緊資訊 設定值/最大值
3. 恆拉系統的 增加張力微調次數/減少張力微調次數/微調參數  
4. 張力系數
5. 如果有開啟計時功能，顯示此張緊時的時間
6. 此次張緊預拉%
7. 張緊秒數
8. 第幾次張緊數

> [!NOTE]
> 預設顯示 1-50 筆 LOG 記錄，如要需調整請修改 LOG_MAX 參數，請勿設定過大，會導致記憶體不足

### 系統資訊

![img_sysinfo](docs/img_sysinfo.jpg)

1. 軟體版本及日期
2. HX711張力放大器參數 開機飄移值/張力基準值/取樣頻率
3. 珠夾頭移動速度，開機時的 全行程步數/移動毫秒 越高越快
4. 步進馬達轉速，越低越快
5. 張力參數
6. 開機次數
7. 總張緊計數

## 硬體

主要材料
1. Raspberry Pico H
2. CBX/SGX 1610 200MM 滑台
3. NEMA23 57步進馬達(2相4線 1.8° 1.2Nm)
4. TB6600 步進馬達驅動器
5. NJ5 20KG 張力傳感器 (YZC-133)
6. HX711 模塊(SparkFun)
7. 2004 i2c LCD 
8. WISE 2086 珠夾頭
9. 5向按鍵模組
10. 按鈕
11. 微控開關
12. 有源蜂鳴器(高平電觸發)
13. 三色 LED
14. 12V 18650 UPS 電池盒

**主要 [BOM清單](https://docs.google.com/spreadsheets/d/1ML2syn-BDUk_CEcyjm62lMwHZluXPYK5swn7pdFXTbw) 價格參考**

![img_part_list](docs/img_part_list.jpg)

> [!WARNING]
> 請務必觀看下一章節 硬體採購建議

> [!WARNING]
> 除非您有自行修改程式的能力，否則請照指的的型號或規格購買材料

## 硬體採購建議

### 滑台

滑台有非常多樣式，此專案中使用的是螺杆式的 CBX/SGX 1610 200MM 滑台，建議購買 CBX 及馬達端帶有軸承固定座的版本，有些無固定座的滑台在高速模式及高張力下會有問題。

軸承固定座
![img_bracket](docs/img_bracket.jpg)

### TB6600 步進電機驅動器

TB6600 是一款小型且經濟實惠的步進電機驅動器，適用於 42 型和 57 型步進電機。在網路商店中，這款驅動器的價格相對便宜。建議選購標註有‘升級版’或‘加強版’的 TB6600，因為某些較便宜的版本在使用過程中可能會產生明顯的電流聲。由於我尚未長時間使用這些廉價版本的 TB6600，因此無法確定其可能存在的潛在問題。

### HX711 張力感應加大器

HX711 是一款簡單易用的稱重傳感器放大器，通常用於高精度電子稱，在這個專案用來量測弦線的張力，我測試過許多廠商生產的 HX711 電路板，發現一個嚴重的問題，許多廠商生產的 HX711 電路板用起來常會有飄移的現象，當然此飄移的現象可以修復，之後會在我的 [Youtube 頻道](https://www.youtube.com/@kuokuo702) 專門拍一集如何修復此現像的影片，建議直接買 SparkFun 生產的 HX711 Load Cell Amplifier 品質較為優良，在製作前先使用 [EP.3 影片](https://youtu.be/pZT4ccE3bZk) 中教學的飄移測試程式測式此板的穩定度，如果你有遇到問題可以在影片中留言。

我測試過的 HX711 電路版 
![img_hx711](docs/img_hx711.jpg)

### NJ5 (YZC-133) 張力傳感器

張力傳感器不一定必須使用 NJ5（YZC-133）。我之所以選擇這個型號，是因為它能夠輕鬆安裝在 Wise 2086 珠夾頭上。如果你使用的是其他夾具，還有許多不同的張力傳感器可供選擇，只需確保選擇承重為 20KG 的型號即可。建議參考以下的 SparkFun HX711 指南，其中提供了詳細的說明。

[https://learn.sparkfun.com/tutorials/load-cell-amplifier-hx711-breakout-hookup-guide/all](https://learn.sparkfun.com/tutorials/load-cell-amplifier-hx711-breakout-hookup-guide/all)

## 硬體設計建議

### 滑台上的前後限位SWITCH

滑動台上的前後限位微動開關如果尺寸過小，可能導致緩衝區不足，從而在觸發開關後到平台完全停止前，平台仍會稍微移動。過小的緩衝區可能導致平台撞擊到微動開關的本體。因此，建議使用尺寸較大的微動開關或弧形臂微動開關，這些開關具有較大的緩衝區，更為合適。如果空間允許，也可以使用長臂微動開關，僅接觸長臂部分，避免本體受力。

![img_limit_switch](docs/img_limit_switch.jpg)

### 珠夾頭與平台間的距離

理論上，珠夾頭與平台之間的距離越近越好，這樣可以延長滑台的壽命。如果不使用Wise 2086珠夾頭，可以選擇造型較短的傳感器，以降低二者之間的距離。

![img_head_table](docs/img_head_table.jpg)

### 使用PCB電路板

您可以先在麵包板組裝測試，成功後再將電路轉移到電路板上或手工焊接板上，不建議長期使用麵包板會有一些問題。

## 接線圖

![img_wiring_diagram](docs/img_wiring_diagram.jpg)

> [!WARNING]
> LED 如果不是給 Raspberry Pi 使用的模組，需串接 330 歐姆電阻以保護 GPIO。

# 製作教學

製作過程影集(持續更新中)

[![VIDEO](https://img.youtube.com/vi/oMgVq6rkX_Q/0.jpg)](https://www.youtube.com/playlist?list=PLN3s8Sz8h_G_Dp-Vqi42OujVhEX1pyrGo)

## 軟體安裝
使用 Thonny 將以下程式碼檔案儲存到 Raspberry Pico 中，其中 src 資料夾內是 hx711 及 2004 LCD 的相關函式庫

1. main.py
2. src\hx711.py
3. src\lcd_api.py
4. src\pico_i2c_lcd.py

> [!WARNING]
> 三個函式庫檔案 hx711.py lcd_api.py pico_i2c_lcd.py 必須放在 src 資料夾下。

> [!NOTE]
> 相關製作影片 [![VIDEO](https://img.youtube.com/vi/oMgVq6rkX_Q/0.jpg)](https://www.youtube.com/watch?v=oMgVq6rkX_Q)

## TB6600 步進馬達電機參數

建議使用快速模式，除非滑台品質不佳導致馬達在快速模式下打滑，此時再切換至慢速模式。

![img_tb6600](docs/img_tb6600.jpg)

> [!NOTE]
> 相關製作影片 [![VIDEO](https://img.youtube.com/vi/7eG5W6a95h0/0.jpg)](https://www.youtube.com/watch?v=7eG5W6a95h0)

## HX711 張力感測器放大器

此專案對於HX711的要求較高，我測試過許多廠商的 HX711機板，建議使用 SparkFun 品質較為穩定。
![img_sparkfun_hx711](docs/img_sparkfun_hx711.jpg)

### 開啟 80Hz

SparkFun 的 HX711 RATE 預設是 10Hz，需使用美工刀將以下綠色箭頭處的連接線割斷來開啟 80Hz
![img_sparkfun_80hz](docs/img_sparkfun_80hz.jpg)

### 穩定度測試

每片 HX711 的品質不一，在裝上機器前可先使用麵包板測試穩定度，正常穩定的機板跑一整天的飄移量不會超過1G
![img_hx711_test](docs/img_hx711_test.jpg)

> [!NOTE]
> 測試程式為 TEST_hx711.py

> [!WARNING]
> 在V1.96版本之後開機時會檢查RATE，未達到80Hz或飄移量超過1G會無法開機使用

> [!WARNING]
> 每個HX711的放大器品質不一，如果有問題建議換供應商購買

> [!NOTE]
> 相關製作影片 [![VIDEO](https://img.youtube.com/vi/pZT4ccE3bZk/0.jpg)](https://www.youtube.com/watch?v=pZT4ccE3bZk)

## 結構佈局

零件的佈局可以根據需要自由調整，下圖顯示的是供參考的定位孔圖。具體的使用方法請參閱製作影片。

![img_dph](docs/img_dph.jpg)

> [!NOTE]
> 相關製作影片 [![VIDEO](https://img.youtube.com/vi/gZF2_dbtVzA/0.jpg)](https://www.youtube.com/watch?v=gZF2_dbtVzA)

## PCB 電路板
![img_pcb](docs/img_pcb.jpg)

Gerber PCB [製板文件下載](https://github.com/206cc/PicoBETH/tree/main/docs/Gerber_PicoBETH_PCB_2024-08-28.zip)

在 1.5 版本中，將未使用的 GPIO 引出，方便後續自定義功能的開發與使用。

> [!WARNING]
> 1.3a 版本已移除按鍵與微控開關的 10K 電阻，因 Raspberry Pi Pico 已內建按鍵的下拉電阻，同時使用可能會有問題。

![img_btn](docs/img_btn.jpg)

Gerber PCB BTN [製板文件下載](https://github.com/206cc/PicoBETH/tree/main/docs/Gerber_PicoBETH_BTN_2024-08-28.zip)


> [!NOTE]
> 請將 Gerber 檔案下載後 EMAIL 給線上(露天、蝦皮)PCB製造廠商，備註單層雙面1.6mm、雙面焊盤，廠商報價後下單即可。

> [!NOTE]
> 相關製作影片 [![VIDEO](https://img.youtube.com/vi/0bb_qs8acqc/0.jpg)](https://www.youtube.com/watch?v=0bb_qs8acqc)

## 硬體測試模式

組裝完成一次開機時請依照指示做所有的按鍵、前後限位、HX711感測器的測試。

> [!NOTE]
> 相關製作影片 [![VIDEO](https://img.youtube.com/vi/MN-W57_CqYg/0.jpg)](https://www.youtube.com/watch?v=MN-W57_CqYg)

## 最後設定

### 校正 HX 參數

HX711 張力感應器校正系數，第一次使用或有更換張力傳感器、HX711 電路板時務必重新校正一次。

在 V2.2 版本之後，因為微調細膩度的提升，可開啟自動恆拉功能校正會更為準確。

校正步驟：
1. 至設定頁面確認自動恆拉功能開啟。
2. 至設定頁面將 HX 參數設為 20.00。
3. 跳回主選單設定拉力為 20.0 磅，預拉 10%。
4. 將外接式張力計，一端綁在拉線機上，另一端綁上羽毛球線。
5. 開始拉線，待平衡時記下最低加磅時的外接式張力計顯示數值。
6. 至設定頁面上填入剛記下的張力計的數值，並點 S 按鍵儲存。

參考影片

[![DEMO](https://img.youtube.com/vi/WMFJQU_TSFk/0.jpg)](https://www.youtube.com/watch?v=WMFJQU_TSFk)

> [!IMPORTANT]
> 非常重要：如果不進行此校正，實際張力與 LCD 顯示的張力會存在誤差。

## 張緊飄移測試

完成張力校正後檢驗張緊時的飄移程度，正常的飄移應該如下方影片展示的一樣約在 ±0.05LB 之內，通過測試後可進行最後的可靠度測試。

參考影片

[![DEMO VIDEO](https://img.youtube.com/vi/wPfW1ht--Y0/0.jpg)](https://www.youtube.com/watch?v=wPfW1ht--Y0)

HX711 飄移的影響 

[![DEMO VIDEO](https://img.youtube.com/vi/MuzmD5DwLmM/0.jpg)](https://www.youtube.com/watch?v=MuzmD5DwLmM)

## 可靠度測試(Reliability Testing)

在 V2.4版本之後新增可靠度測試模式，可自動模擬穿線張緊，用來測試剛組裝好或有更換硬體的機器有無異常。

### 使用方式

在開機時出現版本資訊時，長按方向鍵上鍵直到出現長音放開。固定好線後按下設定中鍵開始

### 測試方法
自動從 20LB 至 30LB 循環張緊，預拉固定10%，平衡後3秒退回。除非有異常狀況自動停止，需在指定提示下按設定中鍵停止，否則測試不會結束。

### 合格標準
建議至少測試 1000次張緊(約4小時)，期間不能有任何的異常中斷，組裝正常的機器是不會出現異常中斷的情況。

> [!WARNING]
> 請勿在 Thonny 上直接執行可靠度測試，請將程式寫入 Raspberry Pi Pico 後單機執行。

參考影片

[![DEMO VIDEO](https://img.youtube.com/vi/ypDOEKCdW9U/0.jpg)](https://www.youtube.com/watch?v=ypDOEKCdW9U)

## 保養維謢

### 螺杆保養

每次使用時觀察是否有不正常的振動或噪音，每個月使用目視的方式確認螺杆狀況。確認螺杆是否沾有灰塵等異物，以及潤滑狀況是否足夠。周圍出現黃褐色潤滑油時，只要行走面呈現光滑現象就表示潤滑狀況良好。滾珠螺桿保養所使用潤滑油粘度建議為 30~40 cSt。

### 零件更換

如有維修更換元件後，可在開機時進入硬體測試模式，重新測試所有元件是否正常。

使用方式：在開機時出現版本資訊時，長按設定中鍵直到出現長音放開。

> [!IMPORTANT]
> 如有更換硬體零件，請務必執行 **硬體測試模式** 測試所有硬體功能是否正常。

### 出廠設定

可不經由電腦重新建立 config.cfg 恢復出廠預設值(原設定檔更名為 config.cfg.bak)，恢復預設後請務必重新校正 HX 張力參數。

使用方式：在開機時出現版本資訊時，長按離開鍵直到出現長音放開。

參考影片

[![DEMO](https://img.youtube.com/vi/iAgFXuEtak4/0.jpg)](https://www.youtube.com/watch?v=iAgFXuEtak4)

### 韌體更新

韌體更新請依照以下步驟執行：

- **備份 Raspberry Pi Pico 上的所有檔案至電腦上**
- **上傳新版本的 main.py 至 Raspberry Pi Pico**
- [**執行硬體測試**](https://github.com/206cc/PicoBETH/blob/main/README.cht.md#%E7%A1%AC%E9%AB%94%E6%B8%AC%E8%A9%A6%E6%A8%A1%E5%BC%8F)
- [**可靠度測試**](https://github.com/206cc/PicoBETH/blob/main/README.cht.md#%E5%8F%AF%E9%9D%A0%E5%BA%A6%E6%B8%AC%E8%A9%A6reliability-testing)
- **用舊的球拍至少試穿一次**

> [!IMPORTANT]
> 以上步驟都很重要。

## 日誌系統

在 V2.5 版本之後，新增簡易的日誌系統，用於幫助排除故障、記錄重要事件，並方便日後查閱和分析。

### 系統日誌 `sys_log.txt`

需透過電腦觀看，您可以透過內建的 `logs_save()` 函數自訂 log 的存儲位置。當記錄檔達到 100KB 時，系統會自動更名並複寫。

**格式:**
```
觸發function:總張緊計數/自訂資訊
```

**示例:**
```
init(HX711):55863T/21188/21465/401/90
forward():55863T/No String?
start_tensioning():55863T/ts_err#0
forward():55863T/No String?
start_tensioning():55863T/ts_err#0
init(HX711):55863T/21188/21493/487/90
```

### 穿線記錄 `logs.txt`

可以直接在 LCD 上查看，最大記錄值為 LOG_MAX 定義參數。

**格式:**
```
總張緊計數,計時器時間,張力單位,設定張力(LB),最大張力(G),預拉(%),張緊時間,恆拉增加張力次數,恆拉減少張力次數,張力參數,張力校正參數,FT參數,打結功能SW,打結(%)
```

**示例:**
```
60384,72719,1,21,10477,10,3,0,0,1.03852,18.17,1,0,15
60385,72736,1,22,10976,10,3,0,37,1.048519,18.17,1,0,15
60386,72753,1,23,11475,10,3,4,23,1.03852,18.17,1,0,15
60387,72770,1,24,11974,10,3,5,41,1.02852,18.17,1,0,15
60388,72785,1,25,12473,10,3,7,43,1.03852,18.17,1,0,15
60389,72803,1,26,12972,10,3,6,49,1.048519,18.17,1,0,15
```

### 可靠度測試記錄 `rt_logs.txt`

需透過電腦觀看，此記錄檔在測試達到 1000 次時，會自動更名並複寫。

**格式:**
```
可靠度測試計數/總張緊計數/自動張力參數/測試張力參數/張緊完成時間(秒)
```

**示例:**
```
4521/60384T/1.03/0.97/13
4522/60385T/1.04/0.97/12
4523/60386T/1.05/0.97/13
4524/60387T/1.04/0.97/13
4525/60388T/1.03/0.97/12
4526/60389T/1.04/0.97/13
```

# 常見問與答

## Q: 我想製作這個專案，但我不知道我能不能完成
A: 建議先看我 YouTube 頻道的 [製作合集](https://www.youtube.com/playlist?list=PLN3s8Sz8h_G_Dp-Vqi42OujVhEX1pyrGo) 的 EP.1 ~ EP.3 前三集，需購買 Raspberry Pico、HX711稱重放大器、NJ5傳感器(YZC-133)、TB6600 步進碼達控製器、57x56 步進碼達，這些材料不難準備，單價也不高，如果範例程式可以順利執行就可以準備剩下的材料，後續的製作偏向機械加工部份，當然你還需要一些工具如台鑽、砂輪機、電烙鐵，以及一些基本的機械加工技術，再根據教學影片一步一步的製作即可完成。

## Q: 我想改用其它的步進馬達驅動器，如更好的 DM542C 可以嗎？
A: 換成 DM542C 理論上可以，但驅動方式可能需要修改，例如程式碼中控制正轉逆轉的 MOTO_FORW_W、MOTO_BACK_W 參數、控制速度的 MOTO_SPEED_V1、MOTO_SPEED_V2 參數，建議先修改 [EP.2](https://youtu.be/7eG5W6a95h0) 中的範例程式中可以使用此驅動器正常驅動馬達，並且確保滑台在移動的過程中沒有異音後再移植至主程式中。我沒有試過，但已經有別的分支開發者移植成功，可以參考 [Pico-Badminton-Stringer](https://github.com/HsuKaoPang/Pico-Badminton-Stringer) 專案

## Q: 我的 HX711 RATE 只有 10Hz 沒有 80Hz 可以使用嗎？
A: 不行，此專案一開始也是用 10Hz 的取樣頻率製作，是能正常使用，但經過後來測試，80Hz 的取樣頻率對於張力的控制會更加的精準、細膩及有較快的反應速度，所以在 1.96 版本中我加入檢查 80Hz 的動作。

## Q: 什麼是 HX711 的飄移？
A: 可以參考 [EP.3](https://youtu.be/pZT4ccE3bZk) 中的測試程式，經過測試，正常的 HX711 在 80Hz 下的飄移值約在 0.5 ~ 1公克以內，所以我在 1.96版本後加入開機時取樣 1秒中的飄移值，如果超過 1公克就無法使用，如果通過檢查，一般來說待機時的 LCD右下角的即時張力顯示在 -10 ~ 10公克以內的線性飄移是正常的。

## Q: 一定要使用 SparkFun 的 HX711 稱重放大器嗎？
A: 當然可以使用其它廠牌的 HX711 稱重放大器，但前提是能通過 [EP.3](https://youtu.be/pZT4ccE3bZk) 中的測試程式，我的經驗是其它廠牌正常的 HX711 會與 SparkFun 的一樣穩定，不幸的是其它廠牌會有許多會飄移的瑕疵品，只要飄移超過 50公克就是 0.1 LB的誤差值，並會造成 Constant-pull system 的反覆微調。

## Q: 關於開機時顯示 ERR: HX711@Zero #3
A: 最近有些人回報已通過 [EP.3](https://youtu.be/pZT4ccE3bZk) HX711 測試，但開機時還是出現此錯誤，此檢查是 load sensor (YZC-133) 上的惠登斯電橋經過 HX711 放大後得到的一個值，做為零點校正的最初基準，在 EP3 測試程式中輸出用 v0 顯示。我在開發時發現我購買中會飄移的 HX711 此值都是負的，這些會飄移的機板修復後此值又變為正的，所以我才加此檢查條件，也許我測試的量不夠多，正值或負值不會影響使用，如果後續確認負值沒問題我會拿掉此檢查，如果你現在不幸遇到了，請先註解掉此檢查(在v2.12版本中的第 447 與 448 行程式碼)，再跟我回報是否正常。

## Q: 可以自製珠夾頭嗎？
A: 這也一直是我想做的事，2086 珠夾頭是整個專案成本最高的硬體，但也是因為他能很容易的安裝在 NJ5傳感器(YZC-133)上以及很好的夾線功能，讓我暫時還沒想到如何取代，如果你有好的珠夾頭設計可以自行裝上，只要注意好 [EP.9](https://youtu.be/Ax4agdsqyms) 中提到的注意事項即可。

## Q: 此電腦拉線機頭的耐用度如何？
A: 如果都使用高品質的零件，理論上耐用度會蠻高的，就算未來需要維修，所有的零件也都相當的便宜，更換也相當簡單。

## Q: 這個專案可以給網球拍穿線嗎？
A: 理論上是可以的，但有些硬體需要升級，例如 NJ5傳感器(YZC-133)需從 20KG 換成 50KG、更大的步進馬達、更大的電源、更強狀的平台與滑台，並修改一些程式碼參數，如果有興趣的可以自行開分支專案開發。

## Q: YouTube 頻道中的製作合集我看不懂中文，有英文的字幕嗎？
A: 我有計劃在未來加入英文字幕，但因為平常工作較為忙碌，每天僅有一些時間可以製作專案，如果可以請幫我在影片上點讚並加入訂閱，這對我是很大的鼓勵。

## Q: 2004 LCD 沒有畫面
A: 請翻到背面試著旋轉調整LCD對比度的藍色可變電阻，以及檢查開啟 LCD 背光的 JUMP 是否有插著。如果都正常，你可以嘗試只連接 5V 電源、GND 以及 LCD 的 4根引腳至 Raspberry Pi Pico，沒意外的話，通電後會出現開機畫面，如果還沒有，請檢查 Raspberry Pi Pico 內是否有 main.py src\hx711.py src\lcd_api src\pico_i2c_lcd.py 4個必要的檔案。

## Q: 穿線功能正常但蜂鳴器一直響不停
A: 請確認是否錯誤的買到低平電觸發的版本(Active Low Trigger)，正確的版本是高平電觸發(Active High Trigger)。

# 最後
如果有製作上的問題，可以直接在 youtube 製作影片下留言，如果您完成了專案，非常歡迎在討論區留下你完成品的照片。

# 致謝

- [HX711 驅動模組適用於 Raspberry Pi Pico](https://github.com/endail/hx711-pico-mpy)
- [2004 I2C 液晶顯示模組適用於 Raspberry Pi Pico](https://github.com/T-622/RPI-PICO-I2C-LCD)

# License

PicoBETH is licensed under Apache 2.0

# Pico 線譜

我也有自已的線譜，暫時取名為Pico Stringing Pattern，我不知道是否已經有人在使用，如果有一樣的線譜請告訴我線譜的名子。

此線譜穿線展示影片

[![stringing demo](https://img.youtube.com/vi/2QjT0JGiluk/0.jpg)](https://www.youtube.com/watch?v=2QjT0JGiluk)

## 線譜圖
![images2-2](docs/img_pico_stringing_pattern.jpg)

1. 短邊約 5個拍長，長邊約 8個拍長。
2. 豎線走線同 Yonex穿線法，最旁邊二條豎線同時張緊。
3. 橫線先穿短邊至底部打結，後穿長邊至頂部打結。
4. 橫線加磅用意在於維持拍框型狀，因機器及個人手法不同，可以試著找出符合自已最小變型量加磅幅度。

## 各弦線張力參考
![images2-2](docs/img_pico_stringing_tension.jpg)

1. 使用 25磅預拉 10%穿好線後靜置 48小時後所量測出來的數值。
2. 所量測是各弦線相對張力參考值，不是準確的絕對張力。
3. 張力測試器校正方法: [https://youtu.be/xYqu03XBzFU](https://youtu.be/xYqu03XBzFU)
