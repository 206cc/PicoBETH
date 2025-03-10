[![cht](https://img.shields.io/badge/lang-cht-green.svg)](README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# 改良珠夾頭啟動按鍵 by jpliew

此次改良使珠夾頭按鍵外觀更美觀，且一樣的低成本。

> [!CAUTION]
> 此為基於 PicoBETH 的改良功能分支，如需瞭解整個專案，請參閱主分支：(https://github.com/206cc/PicoBETH/)

# 成果影片

[![DEMO VIDEO](https://img.youtube.com/vi/U8-CrL-Yr1A/0.jpg)](https://www.youtube.com/watch?v=U8-CrL-Yr1A)

# 硬體

與原專案使用相同的**滾輪式微動開關**，但將原本的 NO（常開）接點改為 NC（常關）。

![sw](docs/sw.jpg)

## 3D 列印支架

使用 jpliew 提供的支架檔案進行 3D 列印：

[下載支架檔案](https://github.com/user-attachments/files/17158580/BadmintonTensionClampSwitch.zip)

下圖為組裝完成品：

![final](docs/final1.jpg)

![final](docs/final2.jpg)

![final](docs/final3.jpg)

## 手動製作支架

如果沒有 3D 列印機，也可以使用 L 型支架手動製作，如下圖所示：

![bracket](docs/bracket.jpg)

# 主程式修改

## v2.80B 版本及之後

在 `EXTRA_CONFIG` 設定中，`jpliew` 參數的值調整為：

- `True` = 開啟  
- `False` = 關閉  

範例設定：

```python
EXTRA_CONFIG = {
    ...
    "jpliew": True
}
```

## v2.80B 版本之前

在 `main.py` 中的 `def start_tensioning():` 函式內，找到以下程式碼：

```python
if button_head_pressed or button_exit_pressed or rt_mode_pressed:
```

需在 `button_head_pressed` 前加上 `not`，修改為：

```python
if not button_head_pressed or button_exit_pressed or rt_mode_pressed:
```

這表示反向按鍵偵測。

> [!CAUTION]
> 若未修改此行程式，張緊完成後將會立即退回。

# 問題

修改後會出現一個小問題，當按下珠夾頭的按鍵時，因為按鍵偵測為非阻塞，需要持續按住按鍵最多 0.5 秒才能退回。在影片的第17秒可以看到這個情況，建議改按 EXIT 鍵則會更快並且即時退回。除此之外，暫時未發現其他問題。

# 致謝

感謝 [jpliew](https://github.com/jpliew) 的貢獻：https://github.com/206cc/PicoBETH/issues/5
