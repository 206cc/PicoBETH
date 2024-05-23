[![cht](https://img.shields.io/badge/lang-cht-green.svg)](https://github.com/206cc/PicoBETH/blob/main/README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/206cc/PicoBETH/blob/main/README.md)

> [!TIP]
> Translated by ChatGPT 3.5  
> 中文說明請點選上方![image](https://img.shields.io/badge/lang-cht-green.svg)連結

# PicoBETH
PicoBETH (Raspberry Pico Badminton Electronic Tension Head) is an open-source project that allows hobbyist stringers who enjoy stringing but only have mechanical stringing machines (drop-weight, manual crank) to create their own electronic tensioning head. If you have basic programming skills, this project can be easily completed.

> Design philosophy: Affordable, Easy , Precision

Drop-weight stringing machine and modification parts
![images1-1](docs/images1-1.jpg)

Modified prototype machine
![images1-2](docs/images1-2.jpg)

Final machine [How to make step by step](https://youtu.be/uJVE3YFJtJA)
![images1-2](docs/images1-6.jpg)

Improvements in the final machine:
1. Added screw dust cover.
2. Upgraded to a 1610 ballscrew for increased tensioning speed.
3. More rational hardware layout, allowing individual disassembly without the need for complete disassembly.
4. Reduced volume by using a stacking approach, avoiding interference with the storage slot.
5. Switched to a custom-designed PCB circuit board.
6. Replacing the HX711 module with one produced by SparkFun.
7. Addition of a UPS battery box that allows continued stringing even in the absence of an external power source.

Stringing demonstration video

[![VIDEO](https://img.youtube.com/vi/ygbpYtNiPa4/0.jpg)](https://www.youtube.com/watch?v=ygbpYtNiPa4)

> [!NOTE]
> If you don't have a stringing machine, you can refer to this project to make one: [Pico-Badminton-Stringer](https://github.com/HsuKaoPang/Pico-Badminton-Stringer)

## Warning
If your badminton stringing machine structure is not robust, I strongly advise against undertaking this project. A weak fixing platform can deform when under tension, causing the racket frame to become rounded and the tension to decrease. As a result, the machine compensates by reinforcing the tension, leading to a cycle that ultimately results in the badminton racket breaking.

> [!CAUTION]
> Extremely important: If your stringing machine is of a simple type, please make sure to reinforce the structure.

## Background
A year ago, due to company club activities, I started playing badminton. Although my badminton skills weren't great, I became fascinated with stringing. I purchased a drop-weight stringing machine and initially planned to buy an electronic tensioning head. However, I later thought about using my knowledge to create this project on the Raspberry Pico, incorporating a load sensor, several microswitches, and buttons.

## Current Main Features

Function demonstration video

[![DEMO VIDEO](https://img.youtube.com/vi/s5no9YdeNnc/0.jpg)](https://www.youtube.com/watch?v=s5no9YdeNnc)

1. LB/KG display and setting
2. Pre-Stretch function
3. Constant-pull system
4. Knot function
5. Tension adjustment manually during tensioning
6. Tension calibration
7. Stringing timer
8. Tension timer
9. Tension counter and boot counter
10. Detailed recording of tensioning logs
11. Pull speed of the string(Switch on the TB6600 stepper motor driver)
12. Real-time UPS Redundancy Feature
13. 0.1LB(50G) accurate

## Standby Screen
1. Use left and right keys to set pounds, kilograms, and the tens, units, and decimal places of pre-stretch.
2. Use up and down keys to adjust the selected settings.
3. Stringing timer function: Start timing by pressing the exit key, stop timing by pressing it again, and reset the timer on the third press.
4. The Pre-Stretch function (PS) and Knot function (KT) are switched using the up and down keys. After using the Knot function, it will automatically switch back to the Pre-Stretch function.
![images1-3](docs/images1-3.png)

## Tensioning Screen
1. When the set tension is reached, automatically enter the constant-pull mode. Increase tension if it's insufficient, decrease tension if it's too high, until pressing the button on the clamp or exit button to end the tensioning mode.
2. Press the center button of the five-way key to enter manual fine-tuning mode. The constant-pull mode will be canceled at this time, and tension can be manually adjusted with the up and down keys. Press the center button of the five-way key again to re-enter constant-pull mode.
3. When the specified tension is reached, the countdown timer will appear.
![images1-4](docs/images1-4.png)

> [!WARNING]
> If the tension fine-tuning amplitude is too high or too low, you can adjust the FT parameter yourself.

## Settings Screen
1. UN: Select pounds or kilograms when setting.
2. AT: Default Constant-Pull Switch.
3. BB: Active buzzer Switch.
4. FT: Amplitude of fine-tuning when reaching the specified tension.
5. HX: Calibration of the load sensor for HX711 (see the Final Settings chapter for details).
6. I: System information.
7. T: Tensioning Count/Log interface
![images1-5](docs/images1-5.png)


## Detailed Recording Of Tensioning Logs
On the settings screen, use the left and right keys to select the tensioning count, then press the center key of the five-way key to enter the tensioning log recording page.
On the page, use the left and right keys to browse through the log records.

TIMER: If the timing function is enabled, display the time of tensioning.<br />
LB: Set tension/stop tension.<br />
PS: Set pre-stretch value.<br />
FT: Increase tension fine-tuning count/decrease tension fine-tuning count/fine-tuning parameters.<br />
C/H: CC parameter/HX parameter.<br />
![images1-7](docs/images1-7.png)

> [!NOTE]
> The default display is 1-50 log records. If you need to adjust, please modify the LOG_MAX parameter.

> [!WARNING]
> Do not set the LOG_MAX parameter too large, as loading too many logs during startup will cause insufficient memory and result in failure to boot.

## System information

![images1-8](docs/images1-8.png)

## Hardware

Main materials
1. Raspberry Pico H
2. CBX/SGX 1610 ballscrew 200MM sliding table
3. 57x56 stepper motor (2-phase 4-wire 1.8°)
4. TB6600 stepper motor driver
5. NJ5 20KG load sensor
6. HX711 module (SparkFun)
7. 2004 i2c LCD
8. Wise 2086 bead clip easy head
9. Five-way key module
10. Button
11. Micro switch
12. Active buzzer
13. Tri-color LEDs
14. 12V 18650 UPS Battery Box

> [!WARNING]
> Unless you have the ability to modify the code yourself, please purchase materials according to the specified models or specifications.

![images2-1](docs/images2-1.jpg)

## Hardware Procurement Recommendations

### Sliding Table

There are many styles of sliding tables, and this project uses the CBX/SGX 1610 ballscrew 200MM sliding table. It is recommended to purchase the CBX version with a bearing fixing seat. Some sliding tables without bearing fixing seat may experience issues under high-speed and high-tension conditions.

Bearing Fixing Seat
![cbx_bracket](docs/cbx_bracket.png)

### TB6600 Stepper Motor Driver

TB6600 is a small, economical stepper motor driver used for 42 and 57 type stepper motors. It is very cheap on online stores. It is recommended to buy TB6600 labeled as "upgraded version" or "enhanced version". Some very cheap TB6600s may have noticeable electrical noise, and I am not aware of any unknown issues.

### HX711 Load Cell Amplifier

HX711 is a simple and easy-to-use amplifier for weight sensors, commonly used in high-precision electronic scales. In this project, it is used to measure the tension of the strings. I have tested many HX711 circuit boards produced by various manufacturers and found a serious issue: many HX711 circuit boards from different manufacturers tend to drift. Of course, this drifting issue can be fixed. I will produce a dedicated episode on my [YouTube channel](https://www.youtube.com/@kuokuo702) on how to fix this issue. It is recommended to directly purchase the HX711 Load Cell Amplifier produced by SparkFun, as it has better quality. Before fabricating the stringing machine head, use the drift test program taught in [EP. 3](https://youtu.be/pZT4ccE3bZk) to test the stability of this board. If you encounter any issues, you can leave a comment on the video.

I tested the HX711 circuit board 
![hx711](docs/hx711.jpg)

## Wiring Diagram
![images2-2](docs/images2-2.png)

> [!WARNING]
> Please add safety measures as needed, such as adding pull-up resistors to buttons, fuses to stepper motors, limiting resistors to LEDs, etc., to protect the Raspberry Pi Pico and motors.

# How To Make

Video Series of the Production Process (Continuously Updating)

[![VIDEO](https://img.youtube.com/vi/oMgVq6rkX_Q/0.jpg)](https://www.youtube.com/playlist?list=PLN3s8Sz8h_G_Dp-Vqi42OujVhEX1pyrGo)

## Software Installation
Use Thonny to save the following code files to the Raspberry Pico. The src folder contains relevant libraries for hx711 and 2004 LCD.

1. main.py
2. src\hx711.py
3. src\lcd_api.py
4. src\pico_i2c_lcd.py

> [!NOTE]
> Thanks to [https://github.com/endail/hx711-pico-mpy](https://github.com/endail/hx711-pico-mpy) for providing the hx711 library for Pico.

> [!NOTE]
> Thanks to [https://github.com/T-622/RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) for providing the 2004 LCD library for Pico.

> [!NOTE]
> Related crafting videos [![VIDEO](https://img.youtube.com/vi/oMgVq6rkX_Q/0.jpg)](https://www.youtube.com/watch?v=oMgVq6rkX_Q)

## TB6600 Stepper Motor Parameters
![images2-3](docs/images2-3.png)

> [!NOTE]
> Related crafting videos [![VIDEO](https://img.youtube.com/vi/7eG5W6a95h0/0.jpg)](https://www.youtube.com/watch?v=7eG5W6a95h0)

## HX711 Load Cell Amplifier

This project demands a higher standard for the HX711, and it is recommended to use the more stable quality provided by SparkFun.
![images2-2](docs/Sparkfun_HX711.jpg)

### Enabling 80Hz

The default setting for SparkFun's HX711 is 10Hz. To enable 80Hz, you'll need to cut the connection wire at the green arrow as indicated below.
![images2-2](docs/Sparkfun_HX711_80Hz.jpg)

### Stability Testing

The quality of each HX711 unit varies. Before installing the equipment, it's advisable to test the stability using a breadboard. A normally stable board should not drift by more than 1G over the course of a whole day.
![images2-2](docs/Sparkfun_HX711_test.jpg)

> [!NOTE]
> The testing script is named TEST_hx711.py.

> [!WARNING]
> Starting from version 1.96, during boot-up, the board will check the RATE. Failure to reach 80Hz or exceeding a drift of 1G will prevent the board from booting up.

> [!WARNING]
> The quality of each HX711 amplifier varies. If there are any issues, it is recommended to switch suppliers.

> [!NOTE]
> Related crafting videos [![VIDEO](https://img.youtube.com/vi/pZT4ccE3bZk/0.jpg)](https://www.youtube.com/watch?v=pZT4ccE3bZk)

## Structural Layout

Components can be freely arranged. The diagram below shows the positioning hole diagram for reference. Refer to the tutorial video for usage instructions.

![EP4](docs/EP4_%E5%AE%9A%E4%BD%8D%E5%AD%94%E5%9C%96_Drawing%20for%20Positioning%20of%20Holes.png)

> [!NOTE]
> Related crafting videos [![VIDEO](https://img.youtube.com/vi/gZF2_dbtVzA/0.jpg)](https://www.youtube.com/watch?v=gZF2_dbtVzA)

## PCB Circuit Board
![images2-3](docs/images2-4.svg)

Gerber PCB [DOWNLOAD](https://github.com/206cc/PicoBETH/tree/main/docs/Gerber_PicoBETH_PCB_2024-05-15.zip)

![images2-3](docs/images2-4_3.svg)

Gerber PCB BTN [DOWNLOAD](https://github.com/206cc/PicoBETH/tree/main/docs/Gerber_PicoBETH_BTN_2024-05-15.zip)

> [!NOTE]
> Related crafting videos [![VIDEO](https://img.youtube.com/vi/0bb_qs8acqc/0.jpg)](https://www.youtube.com/watch?v=0bb_qs8acqc)

## Full System Function Test

Upon completing assembly and powering on the machine for the first time, please conduct tests on all buttons, front and rear limits, and HX711 sensors as instructed on the screen.

> [!NOTE]
> Related crafting videos [![VIDEO](https://img.youtube.com/vi/MN-W57_CqYg/0.jpg)](https://www.youtube.com/watch?v=MN-W57_CqYg)

## Final Settings

### Step 1: Setting FT Parameters

FT Parameter: It determines the magnitude of adjustments after reaching the specified tension. A too large value can cause repeated tension adjustments, while a too small value increases the number of fine-tuning iterations required to reach the specified tension.

The recommended FT parameters:

| Ballscrew | TB6600 Normal Mode | TB6600 Fast Mode |
| -------------------- |:------------------:|:----------------:|
| 1605                 |        14~15       |        7~8       |
| 1610                 |        7~8         |        3~4       |

> [!WARNING]
> Due to differences in hardware brands' precision, the correct FT parameters depend on actual testing.

### Step 2: Calibrate The HX Parameter

HX711 tension sensor calibration coefficient. It is necessary to recalibrate it the first time you use it or when replacing the tension sensor or HX711 circuit board.

Calibration method:
1. Temporarily disable the Constant-pull function on the settings page.
2. Set the HX parameter to 20.00 on the settings page.
3. Return to the main menu and set the tension to 20.3 lb with a Pre-Stretch of 10%.
4. Attach one end of the external tension gauge to the stringing machine and the other end to the badminton string.
5. Start tensioning, and when the LCD displays below 20.0 lb(19.9), note down the reading on the external tension gauge.
6. Enter the recorded tension gauge reading on the settings page and re-enable the constant-pull function.

Reference video

[![Reference video](https://img.youtube.com/vi/r7JQPvqK3No/0.jpg)](https://www.youtube.com/watch?v=r7JQPvqK3No)

> [!IMPORTANT]
> Necessary! If you skip this calibration step, the tension displayed on the LCD will not match the actual tension.

# Frequently Asked Questions

## Q: I want to make this project, but I'm not sure if I can complete it.
A: It is recommended to first watch EP.1 ~ EP.3 of the [project compilation](https://www.youtube.com/playlist?list=PLN3s8Sz8h_G_Dp-Vqi42OujVhEX1pyrGo) on my YouTube channel. You will need to purchase materials such as Raspberry Pico, HX711 load cell amplifier, NJ5 load sensor, TB6600 stepper motor controller, and 57x56 stepper motor. These materials are easy to prepare and not expensive. If the example program runs smoothly, you can prepare the remaining materials. The subsequent production process leans towards mechanical machining. Additionally, you will need tools such as a bench drill, angle grinder, soldering iron, and some basic mechanical machining skills. Follow the tutorial videos step by step to complete the project.

## Q: Can I use other stepper motor drivers, such as the better DM542C?
A: In theory, you can switch to DM542C, but the driving method may need to be modified. For example, parameters such as MOTO_FORW_W, MOTO_BACK_W for controlling forward and reverse in the code, and MOTO_SPEED_V1, MOTO_SPEED_V2 for controlling speed may need to be adjusted. It is recommended to first modify the example program in [EP.2](https://youtu.be/7eG5W6a95h0) to ensure that this driver can drive the motor normally and that there is no abnormal noise from the slide during movement before transplanting it into the main program. Although I haven't tried it myself, there have been successful ports by other branch developers, which you can refer to in the [Pico-Badminton-Stringer](https://github.com/HsuKaoPang/Pico-Badminton-Stringer) project.

## Q: My HX711 RATE is only 10Hz, not 80Hz. Can I still use it?
A: Initially, this project was also made with a sampling frequency of 10Hz, which can be used normally. However, after testing, it was found that a sampling frequency of 80Hz provides more precise, delicate, and faster response control of tension (the time difference between detecting the specified tension and instructing the Raspberry Pico to stop the motor rotation at 10Hz is about 1.3 times that of 80Hz). Therefore, in version 1.96, I added a check for the 80Hz action. If you still want to use 10Hz, please comment out this check and change the tension coefficient CORR_COEF value to 1.3. There may be some parameters or code that need to be adjusted and corrected manually.

## Q: What is drift in HX711?
A: You can refer to the test program in [EP.3](https://youtu.be/pZT4ccE3bZk). After testing, the normal drift value of HX711 at 80Hz is about 0.5 ~ 1 gram. Therefore, in version 1.96, I added a drift value sampling during startup for 1 second. If it exceeds 1 gram, it cannot be used. If the check passes, generally speaking, the real-time tension displayed in the lower right corner of the LCD within -1 ~ 10 grams during standby is normal linear drift.

## Q: Do I have to use SparkFun's HX711 load cell amplifier?
A: Of course, you can use HX711 load cell amplifiers from other brands, but the premise is that they can pass the test program in [EP.3](https://youtu.be/pZT4ccE3bZk). In my experience, other brands' normal HX711s will be as stable as SparkFun's. Unfortunately, other brands may have many defective products that drift. If the drift exceeds 50 grams, it is an error value of 0.1 lb, which will cause repeated fine-tuning of the Constant-pull system.

## Q: Can I make my own bead clip head?
A: This has also been something I've always wanted to do. The Wise 2086 bead clip easy head is the most expensive hardware in the entire project, but it's also because it can be easily installed on the NJ5 load sensor and has excellent clamping functionality. So far, I haven't figured out how to replace it. If you have a good bead clip head design, you can install it yourself. Just make sure to pay attention to the precautions mentioned in [EP.9](https://youtu.be/Ax4agdsqyms).

## Q: How durable is this electronic tension head?
A: Theoretically, if high-quality parts are used, the durability should be quite high. As of today (2024/05/22), the number of tensionings on the formal machine I made has exceeded 7500 times without any problems occurring. Even if maintenance is required in the future, all electronic components are quite inexpensive.

## Q: Can this project be used for stringing tennis rackets?
A: In theory, it is possible, but some hardware needs to be upgraded, such as changing the load sensor from 20KG to 50KG, larger stepper motors, larger power supplies, stronger platforms and slides, and modifying some code parameters. If interested, you can develop your own branch project.

## Q: Are there English subtitles for the project compilation on the YouTube channel?
A: I plan to add English subtitles in the future, but because my usual work is quite busy, I only have some time to work on projects each day. If possible, please give the video a thumbs up and subscribe, as this is a great encouragement for me.

# Conclusion
If you have any questions about making, please leave a comment in the YouTube video.

# Pico Sringing Pattern

I also have my own stringing pattern, temporarily named the Pico Stringing Pattern. I'm not sure if anyone else is using it, so if there is a similar stringing pattern, please let me know the stringing pattern name.

The stringing pattern demo.

[![stringing demo](https://img.youtube.com/vi/2QjT0JGiluk/0.jpg)](https://www.youtube.com/watch?v=2QjT0JGiluk)

## Sringing Pattern
![images2-2](docs/pico_stringing_pattern.png)

1. The short side is approximately 5 racket lengths, and the long side is approximately 8 racket lengths.
2. Follow the Yonex stringing pattern for main strings, pulling the two outermost main strings together for tension.
3. The cross strings are first the bottom of the short side, tying knots at the bottom, and then strings on the long side, tying knots at the top.
4. Increasing the tension of the cross strings will help the racquet maintain its original shape after stringing. Due to variations in stringing machine and individual techniques, you can experiment to find the tension increment that minimizes deformation.

## Tension Of Each String
![images2-2](docs/pico_stringing_tension.png)

1. The measured values were obtained after stringing with a 25lb tension, following a 10% pre-stretch, and allowing it to sit for 48 hours.
2. The measurements represent relative tension reference values for each string, NOT the actual tension.
3. Calibration method for the tension tester: [https://youtu.be/xYqu03XBzFU](https://youtu.be/xYqu03XBzFU)
