[![cht](https://img.shields.io/badge/lang-cht-green.svg)](https://github.com/206cc/PicoBETH/blob/main/README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/206cc/PicoBETH/blob/main/README.md)

> [!TIP]
> Translated by ChatGPT 3.5 <中文說明請點選上方cht連結>

# PicoBETH
PicoBETH (Raspberry Pico Badminton Electronic Tension Head) is an open-source project that allows hobbyist stringers who enjoy stringing but only have mechanical stringing machines (drop-weight, manual crank) to create their own electronic tensioning head. If you have basic programming skills, this project can be easily completed.

Drop-weight stringing machine and modification parts
![images1-1](docs/images1-1.jpg)

Modified prototype machine
![images1-2](docs/images1-2.jpg)

Final machine
![images1-2](docs/images1-6.jpg)

Improvements in the final machine:
1. Added screw dust cover
2. Upgraded to a 1610 specification screw for increased tensioning speed
3. More rational hardware layout, allowing individual disassembly without the need for complete disassembly
4. Reduced volume by using a stacking approach, avoiding interference with the storage slot
5. Switched to a custom-designed PCB circuit board

Stringing demonstration video

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ygbpYtNiPa4/0.jpg)](https://www.youtube.com/watch?v=ygbpYtNiPa4)

## Background
A year ago, due to company club activities, I started playing badminton. Although my badminton skills weren't great, I became fascinated with stringing. I purchased a drop-weight stringing machine and initially planned to buy an electronic tensioning head. However, I later thought about using my knowledge to create this project on the Raspberry Pico, incorporating a tension sensor, several microswitches, and buttons.

## Current main features:

1. Set tension in pounds or kilograms
2. Pre-Stretch function
3. Automatic tension fine-tuning after tensioning
4. Tension zeroing
5. Tension coefficient setting
6. Tension calibration
7. Stringing timer
8. Tensioning count recording
9. Detailed recording of tensioning logs

## Standby screen
1. Use left and right keys to set pounds, kilograms, and the tens, units, and decimal places of pre-stretch.
2. Use up and down keys to adjust the selected settings.
3. Stringing timer function: Start timing by pressing the exit key, stop timing by pressing it again, and reset the timer on the third press.
![images1-3](docs/images1-3.png)

## Tensioning screen
1. When the set tension is reached, automatically enter the tension fine-tuning mode. Increase tension if it's insufficient, decrease tension if it's too high, until pressing the button on the clamp or exit button to end the tensioning mode.
2. Press the center button of the five-way key to enter manual fine-tuning mode. The automatic fine-tuning mode will be canceled at this time, and tension can be manually adjusted with the up and down keys. Press the center button of the five-way key again to re-enter automatic fine-tuning mode.
3. When the specified tension is reached, the countdown timer will appear.
![images1-4](docs/images1-4.png)

> [!WARNING]
> If the tension fine-tuning amplitude is too high or too low, you can adjust the FT parameter yourself.

## Settings screen
1. UN: Select pounds or kilograms when setting.
2. CC: Fine-tuning parameters (see the first boot chapter for details).
3. HX: Calibration of the tension sensor for HX711 (see the first boot chapter for details).
4. FT: Amplitude of fine-tuning when reaching the specified tension.
![images1-5](docs/images1-5.png)

> [!NOTE]
> Once these parameters are set, there is usually no need to set them again.

## Detailed recording of tensioning logs
On the settings screen, use the left and right keys to select the tensioning count, then press the center key of the five-way key to enter the tensioning log recording page.
On the page, use the left and right keys to browse through the log records.
TIMER: If the timing function is enabled, display the time of tensioning.
LB: Set tension/stop tension.
PS: Set pre-stretch value.
FT: Increase tension fine-tuning count/decrease tension fine-tuning count/fine-tuning parameters.
ST: CC parameter/HX parameter.
![images1-7](docs/images1-7.png)

> [!NOTE]
> The default display is 1-50 log records. If you need to adjust, please modify the LOG_MAX parameter.

> [!WARNING]
> Do not set the LOG_MAX parameter too large, as loading too many logs during startup will cause insufficient memory and result in failure to boot.

## Hardware

Main materials
1. Raspberry Pico H
2. 1610 200MM sliding table
3. 57 stepper motor (2-phase 4-wire 1.8°)
4. TB6600 stepper motor driver
5. NJ5 20KG tension sensor
6. HX711 module (red anti-interference version)
7. 2004 i2c LCD
8. WISE 2086 head
9. Five-way key module
10. Button
11. Micro switch
12. Active buzzer
13. Tri-color LEDs

> [!WARNING]
> Unless you have the ability to modify the code yourself, please purchase materials according to the specified models or specifications.

![images2-1](docs/images2-1.jpg)

## Wiring diagram
![images2-2](docs/images2-2.png)

> [!WARNING]
> Please add safety measures as needed, such as adding pull-up resistors to buttons, fuses to stepper motors, limiting resistors to LEDs, etc., to protect the Raspberry Pi Pico and motors.

## PCB circuit board
![images2-3](docs/images2-4.svg)

> [!NOTE]
> You can download the circuit board for the above image to avoid the trouble of hand-soldering the circuit board.

> [!NOTE]
> The lock points around this circuit board are based on the lock point positions of the 2004 LCD, allowing stacking to reduce volume.

## TB6600 stepper motor parameters
![images2-3](docs/images2-3.png)

> [!WARNING]
> Changing these TB6600 motor parameters may require many modifications in the code.

# Software Installation
Use Thonny to save the following code files to the Raspberry Pico. The src folder contains relevant libraries for hx711 and 2004 LCD.

1. main.py
2. src\hx711.py
3. src\lcd_api.py
4. src\pico_i2c_lcd.py

> [!NOTE]
> Thanks to [https://github.com/endail/hx711-pico-mpy](https://github.com/endail/hx711-pico-mpy) for providing the hx711 library for Pico.

> [!NOTE]
> Thanks to [https://github.com/T-622/RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) for providing the 2004 LCD library for Pico.

# First Boot

## Calibrate the HX Parameter

HX711 tension sensor calibration coefficient. It is necessary to recalibrate it the first time you use it or when replacing the tension sensor or HX711 circuit board.

Calibration method:
1. Attach one end of an external tension gauge to the stringing machine and the other end to the badminton string.
2. Set the HX parameter in the LCD setting page to 20.00.
3. Return to the main menu and set the tension to 20 pounds.
4. Press the up or down key to start stringing. When the LCD displays 20 pounds, note down the tension gauge reading.
5. Enter the recorded tension gauge value in the HX parameter field on the settings page.

> [!WARNING]
> If you skip this calibration, there may be a discrepancy between the actual tension and the tension displayed on the LCD.

> [!IMPORTANT]
> This parameter is mainly based on setting storage (config.cfg).

Reference video: [https://youtu.be/JaplgmXzbjY](https://youtu.be/JaplgmXzbjY)

## Set the CC Parameter
When the motor stops at the specified tension, the actual tension will continue to change. Another coefficient needs to be set to correct this, which can be set manually or automatically on the settings page.

Calibration method:
1. Fix the badminton string, attach one end to the stringing machine and the other end to the clamp.
2. On the LCD settings page, press the AUTO button in the CC field using the up or down key to start stringing.
3. AUTO will automatically fill in the reference CC value.
4. Use this value to string and test. The optimal result is when there is no fine-tuning action when reaching the specified tension with pre-stretch set to 0.
   (You may see the tension on the LCD continue to change beyond the specified tension when the motor stops. This is a normal physical phenomenon. The best parameter is when the tension stabilizes after balancing and there is no fine-tuning action at the specified tension.)
5. If the automatically calculated CC value is not ideal, manually fine-tune the CC value on the settings page and repeat step 4 to find the optimal value.

> [!WARNING]
> If pre-stretch is enabled, a detensioning test will be performed, so set pre-stretch to 0 during testing.

> [!IMPORTANT]
> Changing the HX711 circuit board, sliding table pitch, or motor will affect this coefficient. If you find frequent fine-tuning at pre-stretch 0, you can calibrate this value.

> [!IMPORTANT]
> This parameter is mainly based on setting storage (config.cfg).

Reference video: [https://youtu.be/KuisR6eKiwk](https://youtu.be/KuisR6eKiwk)

# Conclusion
If you encounter any issues during the manufacturing process, feel free to discuss them in the comments or send me an email with your inquiries.
