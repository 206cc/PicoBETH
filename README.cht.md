![images1-1](docs/Pico_Logo.png)

[![cht](https://img.shields.io/badge/lang-cht-green.svg)](README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# PicoBETH
**PicoBETH** (Raspberry Pico Badminton Electronic Tension Head) 是一個開源項目，讓有機械式穿線機的愛好者可以自行製作電子拉線機頭。如果你具備基本的程式能力，這個項目會很容易完成。

> 設計理念：便宜、簡單、精準

## 現有主要功能與特點

[![DEMO VIDEO](https://img.youtube.com/vi/pWgD_OSyc1g/0.jpg)](https://www.youtube.com/watch?v=pWgD_OSyc1g)

### 功能
- **磅/公斤顯示及設定**
- **預拉 (Pre-Stretch)**
- **自動恆拉 (Constant-Pull)**
- **打結加磅 (Knot)**
- **張緊中手動調整張力**
- **張力校正**
- **穿線計時器**
- **張力計數器與開機計數器**
- **張緊 LOG 記錄**
- **9 段速度切換**

### 特點
- **0.05 LB 高精度**
  - 在 Sparkfun HX711 94Hz 及 V2.2 版本後
  - [參考影片](https://youtu.be/Hk7eMABAxT0)
- **低功耗**
  - 僅需 DC19V 4A 電源*
- **UPS 不斷電**
  - 使用 18650 x 5 電池可支持至少完成一次穿線
- **緊湊設計**
  - 大小約 38(L) x 15(W) x 9(H) CM (不含珠夾頭)
- **結構簡單、成本低且易於維修**
  - 所有元件皆易於取得且價格低廉
- **高耐用性**
  - 已完成超過 45.0 萬次張緊可靠度測試（測試仍在進行中）

> [!CAUTION]
> 在 V2.70 版本後的**快速模式**下，當速度設置在 **L7** 以上且**張力超過 30 LB** 時，原本的 12V3A 電源可能不足以支持，可能導致馬達失步(打滑)。因此，更換為 19V4A 的電源。如果你計劃更換 19V 電源，請確保你的 5V 轉換器可以承受 19V 輸入電壓。使用外接 UPS 亦需更換為 19V 兼容版本。

## 開發項目計劃

| 計劃項目           | 進度     | 備註                           |
| ------------------ | -------- | ------------------------------ |
| 可靠度測試         | 進行中   | 張緊次數已達 450,000+，尚未發現故障 (截至 2024/10/14) [測試影片](https://youtube.com/shorts/0TDaBDEwqnI) |
| 適用網球拍         | 測試中   | 使用 GX80 滑台進行 75~85LB 循環張緊可靠度測試中。 張緊次數已達 100,000+ (截至 2024/10/14) |
| 更新結構佈局       | 進行中   | V2.0 將採用更簡單、美觀且更具成本效益的佈局方式 |
| 相容 Pico 2        | 結束 | 受到 [RP2350-E9](https://hackaday.com/2024/09/20/raspberry-pi-rp2350-e9-erratum-redefined-as-input-mode-leakage-current/) BUG 的影響，已確認無法直接使用。 |
| 製作對應 WISE 2086 安裝孔位轉接座 | 尚未開始 | 徵求故障的 WISE 2086 |

## 專案起源
一年前，由於參加公司社團，我開始接觸羽毛球，並對穿線產生濃厚興趣。我購買了重錘式穿線機，原計劃買一個電子拉線機頭，但最終決定利用我所掌握的知識自行設計。這個項目就是結合 Raspberry Pico、張力傳感器、微動開關和按鈕的成果。

**重錘式穿線機與改裝零件**
![img_parts](docs/img_parts.jpg)

**開發中機器**
![img_dev_machine](docs/img_dev_machine.jpg)

**正式機** [製作合集](https://youtu.be/uJVE3YFJtJA)
![img_final_machine](docs/img_final_machine.jpg)

**穿線展示影片**

[![VIDEO](https://img.youtube.com/vi/ygbpYtNiPa4/0.jpg)](https://www.youtube.com/watch?v=ygbpYtNiPa4)

> [!NOTE]
> 如果你沒有穿線機，請參考 [Pico-Badminton-Stringer](https://github.com/HsuKaoPang/Pico-Badminton-Stringer) 項目。

> [!NOTE]
> 如果你正在考慮購買手動穿線機，我建議選擇具備六點固定和底座夾具的重錘式穿線機。重錘機具備恆拉效果，其穿線張力與電子機相差不大。且重錘機在電子拉線頭故障時可以作為替代方案，並且能夠快速安裝回去恢復使用。

# 警告
如果你的穿線機結構不夠堅固，請勿進行此專案。結構不堅固的平臺會在張緊時發生變形，有可能導致球拍損壞。

> [!CAUTION]
> 非常重要：如果你的請補強簡易型穿線機台的結構。

# 其他說明文件

- [操作與設定指南](docs/1.Operation_and_Settings_Guide.cht.md)
- [硬體製作、採購與維護](docs/2.Hardware_Setup.cht.md)
- [維護與日誌管理指南](docs/3.Maintenance_and_Logs_Guide.cht.md)
- [常見問題解答(FAQ)](docs/4.FAQ.cht.md)
- [Pico 線譜](docs/5.Pico_Stringing_Pattern.cht.md)
- [研究室](docs/6.Research_Lab.cht.md)

# 改進分支

| 分支名稱                        | 說明                             |
|----------------------------------|----------------------------------|
| [`imp/beadclip-btn@jpliew`](https://github.com/206cc/PicoBETH/blob/imp/beadclip-btn%40jpliew/README.cht.md) | 改良式珠夾啟動按鍵                |
| `imp/tennis` | 適用網球拍 (測試中，製作方法將在可靠度測試達 10 萬次後發佈)              |


# 支援
有任何問題，可以在 YouTube 影片下方留言。若完成專案，歡迎在討論區分享你的成果照片。

# 致謝

- [HX711 驅動模組適用於 Raspberry Pi Pico](https://github.com/endail/hx711-pico-mpy)
- [2004 I2C 液晶顯示模組適用於 Raspberry Pi Pico](https://github.com/T-622/RPI-PICO-I2C-LCD)

# License

- **Source Code**: Licensed under the Apache License 2.0
- **Hardware Design**: Distributed under the CERN Open Hardware Licence v2 - Weakly Reciprocal
