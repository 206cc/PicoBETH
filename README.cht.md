![images1-1](docs/img_hw3d.jpg)

[![cht](https://img.shields.io/badge/lang-cht-green.svg)](README.cht.md) 
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# PicoBETH HW 3D-Printed Version
> [!CAUTION]
>  本 3D Printed 專案的說明文件仍在持續修訂中，如有任何問題，歡迎在討論區提問交流。

> [!CAUTION]
>  此分支主要將主版本(main-branch)中需要複雜機械加工的零件改為 3D 列印，從而大幅簡化製作流程。在開始進行此 3D 列印分支的製作前，請務必詳閱 [主版本](https://github.com/206cc/PicoBETH) 的說明文件，了解相關知識和注意事項。

## 目錄

- [PicoBETH HW 3D-Printed Version](#picobeth-hw-3d-printed-version)
  - [3D 列印部件下載](#3d-列印部件下載)
  - [3D 展示模型](#3d-展示模型非列印模型)
  - [組裝影片](#組裝影片)

- 零件列表
  - [主要零件](#主要零件)
  - [螺絲清單](#螺絲清單)

- 注意事項
  - [3D 部件 PART-1](#3d-部件-part-1)
    - [滑台固定螺絲](#滑台固定螺絲)
  - [3D 部件 PART-3](#3d-部件-part-3)
    - [固定螺絲](#固定螺絲)
  - [Load Cell 感應線](#load-cell-感應線)
  - [Load Cell 安裝方向](#load-cell-安裝方向)
  - [轉接座](#轉接座)

- [支援](#支援)

## 3D 列印部件下載
[PicoBETH HW 3D Printed Version](https://www.thingiverse.com/thing:6913170)

> [!CAUTION]
>  請勿使用 PLA 材質列印，因其強度隨時間可能會劣化。

## 3D 展示模型(非列印模型)

[PicoBETH HW 3D Viewing Model](https://www.tinkercad.com/things/4lv9ptAmuc4-picobeth-hw-3d-viewing-model)

## 組裝影片

請參考 YouTube 上的 [組裝影片](https://youtube.com/shorts/kR_JLVGHwB8) 完成組裝。

## 零件列表

### 主要零件

![parts](docs/img_bomlist.jpg)

| 編號 | 名稱                                |
|------|-------------------------------------|
| 1    | Part-1 主體                        |
| 2    | Part-2 後限位架                    |
| 3    | Part-3 Load Cell 固定架            |
| 4    | Part-4 PCB 與 TB6600 安裝架        |
| 5    | Part-5 電源與開關飾蓋              |
| 6    | Part-6 LCD 與按鍵架                |
| 7    | Part-7 後飾蓋                      |
| 8    | SGX 1610 200mm 滑台               |
| 9    | PCB 主板、Raspberryy Pico、Spark HX711、蜂鳴器      |
| 10   | PCB 按鍵板                         |
| 11   | 2004 i2c LCD                       |
| 12   | TB6600 步進馬達驅動器             |
| 13   | NJ5 20kg 張力傳感器 (YZC-133)     |
| 14   | WISE 2086 珠夾頭                   |
| 15   | 啟動開關支架                       |
| 16   | 捲繞管Ø4 20cm                     |
| 17   | 開關 12cm                          |
| 18   | DC 插座 15cm                       |
| 19   | 主板電源線 20cm                    |
| 20   | TB6600 電源線 28cm                 |
| 21   | 步進馬達訊號線 XH2.54mm 4P 15cm   |
| 22   | 前限位開關 XH2.54mm 2P 20cm       |
| 23   | 後限位開關 XH2.54mm 2P 20cm       |
| 24   | LED 訊號線 XH2.54mm 4P（同向）25cm|
| 25   | 取消按鍵 XH2.54mm 2P（同向）25cm  |
| 26   | 五向按鍵 XH2.54mm 6P（同向）25cm  |
| 27   | LCD 訊號線 XH2.54mm 4P 40cm       |
| 28   | 珠夾啟動開關 XH2.54mm 2P 50cm     |

> [!WARNING]  
> **注意：** 用於電源的電線線徑請勿小於 **18 AWG**。

### 螺絲清單

![parts](docs/img_screw_list.jpg)

| 編號 | 名稱                           | 數量 |
|------|--------------------------------|------|
| A    | 灰色彈簧螺式電線連接器          | 3    |
| B    | M3 × 10mm 割尾螺絲             | 8    |
| C    | M3 × 6mm 割尾螺絲              | 15   |
| D    | M2.6 × 10mm 割尾螺絲           | 4    |
| E    | M3 × 6mm 圓頭螺絲              | 2    |
| F    | M4 × 16mm 內六角螺絲           | 4    |
| G    | M4 × 20mm 內六角螺絲           | 4    |
| H    | M4 × 30mm 內六角螺絲           | 2    |
| I    | M4 × 8mm 內六角螺絲            | 2    |
| J    | M4 彈簧墊圈                    | 10   |
| K    | M4 平墊圈                      | 10   |
| L    | M5 × 70mm 內六角螺絲 + 平墊圈 | 2    |

## 注意事項

### 3D 部件 PART-1

![part1](docs/img_3d_part1.jpg)

主體需承受較大的變形力，建議至少使用以下列印參數：
- **壁厚：** 5mm 以上  
- **填充：** 30% 以上  

#### 滑台固定螺絲
滑台固定螺絲應突出平台 3.5~4.5mm。若螺絲過長，可能導致滑台無法緊貼平台，可透過加裝墊圈調整突出長度。建議按照順序先鎖緊底部的 2 顆螺絲，再鎖緊側面的 4 顆螺絲。

- **底部固定螺絲：**  
  2 組 M4 × 30mm 螺絲，每組含平墊圈和彈簧墊圈各 1。
  安裝扭力 1.5N·m

- **側面固定螺絲：**  
  4 組 M4 × 20mm 螺絲，每組含平墊圈和彈簧墊圈各 1。
  安裝扭力 1.5N·m

> [!CAUTION]
>  請依照建議的安裝扭力值進行鎖緊，過大的扭力可能導致 3D 列印部件損壞。

### 3D 部件 PART-3

![part3](docs/img_3d_part3.jpg)

作為 Load Cell 與滑台座的固定零件，此部件需承受較大的變形力，建議至少使用以下列印參數：
- **填充：** 100%  

#### 固定螺絲
- **Load Cell 固定螺絲：**  
  2 組 M5 × 70mm 螺絲，含平墊圈。
  安裝扭力 2.0N·m

- **滑台座固定螺絲：**  
  4 組 M4 × 16mm 螺絲，每組含平墊圈和彈簧墊圈各 1。
  安裝扭力 1.5N·m

> [!CAUTION]
>  請依照建議的安裝扭力值進行鎖緊，過大的扭力可能導致 3D 列印部件損壞。

### Load Cell 感應線

![hx711_loadcell](docs/img_hx711_loadcell.jpg)

由於設計佈局的限制，Load Cell 的安裝方向與 HW1 和 HW2 相反。因此，接線時需對調接頭上的綠色與白色訊號線，才能正確偵測受力方向。若未正確接線，可能導致張力偵測方向錯誤。

### Load Cell 安裝方向

請注意 Load Cell 的安裝方向。影片中展示的是 NJ5 出廠的 YZC-133，其安裝方向與大多數 YZC-133 不同。若使用其他廠牌的 YZC-133，安裝方向可能需要旋轉 180 度。詳細說明請參考 [EP.5 補充篇 - 斜度微調與 YZC-133 Load Cell](https://youtube.com/22Ev_kWTnxk)。

### 轉接座

您仍需設計一個底部轉接座以轉接至穿線機平台。可參考 [EP.9 定位與固定](https://youtube.com/Ax4agdsqyms)。建議使用 M8 規格螺絲，安裝時務必搭配平墊片，並遵循建議的扭力值 3.0 N·m。

# 支援
如有任何問題或改進建議，歡迎隨時在討論區或 YouTube 影片下方留言交流。完成專案後，也歡迎在討論區分享您的成果照片。
