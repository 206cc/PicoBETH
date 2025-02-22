[![cht](https://img.shields.io/badge/lang-cht-green.svg)](README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# PicoBETH on Pico2

由於部分使用者錯誤購買了 Raspberry Pi Pico 2(RP2350)，或有人詢問是否能升級至 Pico 2，本分支說明 **PicoBETH** 移植至 **Pico 2** 的現況與測試結果。

## 影響與問題

Pico 2 採用了 **RP2350** 微控制器，但其硬體存在 **E9 錯誤（Erratum）**，導致內建的 **下拉電阻（pull-down resistor）異常**。  
本專案所有的按鍵偵測均依賴內建下拉電阻，因此 **無法直接相容** Pico 2，解決方案如下：

1. **外拉下拉電阻** 來確保按鍵偵測正常運作。
2. **修改電路設計為上拉按鍵**，改用內建的 **上拉電阻（pull-up resistor）** 以繞過此問題。

有關 RP2350 E9 錯誤的詳細資訊，請參考以下文章：

- [Hardware Bug In Raspberry Pi’s RP2350 Causes Faulty Pull-Down Behavior](https://hackaday.com/2024/08/28/hardware-bug-in-raspberry-pis-rp2350-causes-faulty-pull-down-behavior/)
- [RP2350: Internal pull down issue](https://forums.pimoroni.com/t/rp2350-internal-pull-down-issue/25360)


## 修正與調整

為解決此問題進行了 **硬體修正** 與 **軟體修正**：

### 硬體修正
- **PCB 重新設計**，所有按鍵與微動開關改為上拉按鍵設計

### 軟體修正
- **按鍵與微動開關驅動邏輯調整**，全面改用內建上拉電阻。
- **步進馬達驅動參數微調**，使其可在接近極限轉速運轉。


## 測試結果

以下為 Raspberry Pi **Pico** 與 **Pico 2** 在 PicoBETH 下運行的對比測試：  
[![VIDEO](https://img.youtube.com/vi/p8Iu2A8doCQ/0.jpg)](https://www.youtube.com/watch?v=p8Iu2A8doCQ)

## 結論

1. **Pico 2 主要在開機時略快**，但在按鍵操作、穿線張緊與滑台復位時，並無顯著優勢。
2. **Pico 在本專案已具備穩定性與成熟度**，經過超過百萬次張緊測試，可靠性已獲驗證。
3. **Pico 具備更低的價格與更廣泛的可用性**，相較之下，Pico 2 並無足夠優勢支撐移植。

### 本專案 **不會移植至 Pico 2**，建議使用者繼續使用 **Raspberry Pi Pico** 以確保穩定性與相容性。
