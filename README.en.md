以下是您提供的文本的英文翻譯：

[![cht](https://img.shields.io/badge/lang-cht-green.svg)](https://github.com/206cc/PicoBETH/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/206cc/PicoBETH/blob/main/README.en.md)

# PicoBETH

PicoBETH (Raspberry Pico Badminton Electronic Tension Head) is an open-source project that allows amateur stringers who enjoy stringing but only have mechanical stringing machines (drop weight, crank) to create their own electronic tension head. If you have some basic programming skills, this project can be easily completed.

Modified Prototype
![images1-2](docs/images1-2.jpg)

Stringing Demonstration Video
[https://youtu.be/uSFNzvQrzLI](https://youtu.be/uSFNzvQrzLI)

Final Machine
![images1-2](docs/images1-6.jpg)

Improvements to the Final Machine
1. Added screw dust cover
2. Switched to 1610 specification screws for increased tensioning speed
3. More reasonable hardware layout, parts can be disassembled individually without a full teardown
4. Used a stacking design to reduce size and avoid blocking the storage slot
5. Used a self-designed PCB circuit board

## Motivation
A year ago, due to my company's badminton club, I started playing badminton. Despite not being very skilled, I became fascinated with stringing. I bought a drop-weight stringing machine and originally wanted to purchase an electronic tension head. However, I realized I could use my knowledge to create this project on the Raspberry Pico using a pressure sensor, several microswitches, and buttons.

## Current Key Features:

1. Tension settings in pounds or kilograms
2. Pre-Stretch
3. Automatic fine-tuning of pounds after tensioning
4. Tension zeroing
5. Tension coefficient setting
6. Tension calibration
7. Stringing timer
8. Tensioning count records
9. Detailed tensioning log records

## Standby Screen:
1. Use left and right keys to select tens and ones digits and decimals for adjusting pounds, kilograms, and pre-stretch.
2. Use up and down keys to adjust the selected settings.
3. Stringing timer functionality starts counting when the exit key is pressed, stops when pressed again, and resets on the third press.
![images1-3](docs/images1-3.png)

## Tensioning Screen:
1. When the set tension is reached, the fine-tuning program begins. It adds pounds if the tension is too low or reduces pounds if it's too high, until the pearl clamp button or exit button is pressed to end the tensioning process.
2. You can also enter manual fine-tuning mode by pressing the up and down keys, at which point the automatic fine-tuning program will be canceled. Press the center key of the five-way key to re-enter automatic fine-tuning mode.
3. When the specified tension is reached, the timer starts counting.

> [!WARNING]
> If the fine-tuning range is too high or too low, you can adjust the FT_ADD parameter yourself.

## Settings Screen:
1. UN: Choose between pounds or kilograms as the unit of measurement.
2. CC: Fine-tuning parameters (see the first boot chapter for details).
3. HX: HX711 pressure sensor calibration (see the first boot chapter for details).
4. FT: Range of fine-tuning when the specified tension is reached.
![images1-5](docs/images1-5.png)

> [!NOTE]
> In general, once you've set these parameters, you won't need to come back to this page often.

## Detailed Tensioning Log Records
On the settings screen, use the left and right keys to select tensioning count, and press the center key to enter the tensioning log record page.
On this page, use the left and right keys to browse the log records.
TIMER: If the timer function is activated, it will display the time for this tensioning.
LB: Set tension/stop tension
PS: Set pre-stretch value
FT: Increase tension fine-tuning count/reduce tension fine-tuning count/fine-tuning parameter
S: The number of seconds from this tensioning to release
ST: CC parameter/HX parameter

![images1-7](docs/images1-7.png)

> [!NOTE]
> By default, it displays 1-50 log records. If you need more, you can modify the LOG_MAX parameter.

## Hardware:

Main Materials
1. Raspberry Pico H
2. 1610 200MM Sliding Table
3. 57 Stepper Motor (1.8° Step Angle 2 Phase 4 Line)
4. TB6600 Stepper Motor Driver
5. NJ5 20KG Load Cell
6. HX711 Module (Red)
7. 2004 i2c LCD
8. WISE 2086 Head
9. Five-way Key Module
10. Buttons
11. Micro Switches
12. Active Buzzer
13. Tri-Color LEDs

![images2-1](docs/images2-1.jpg)

## Wiring Diagram
![images2-2](docs/images2-2.png)

> [!WARNING]
> Please add safety measures as needed, such as pull-up resistors for the buttons, fuses for the stepper motor, current-limiting resistors for the LEDs, to protect the Raspberry Pi Pico and the motors.

## PCB Circuit Board
![images2-3](docs/images2-4.svg)

> [!NOTE]
> You can download the PCB layout in the image above to avoid the hassle of hand-soldering the circuit board.

> [!NOTE]
> The locking points around this circuit board are based on the 2004 LCD locking point locations, allowing for stacking to reduce size.

## TB6600 Stepper Motor Parameters
![images2-3](docs/images2-3.png)

> [!WARNING]
> Modifying these motor parameters may require adjusting many parameters in the code.

# Software Installation
Use Thonny to save the following code files to the Raspberry PICO. The "src" folder contains relevant libraries for hx711 and the 2004 LCD.

1. main.py
2. src\hx711.py
3. src\lcd_api.py
4. src\pico_i2c_lcd.py

> [!NOTE]
> Special thanks to [https://github.com/endail/hx711-pico-mpy](https://github.com/endail/hx711-pico-mpy) for providing the hx711 library for Pico.

> [!NOTE]
> Special thanks to [https://github.com/T-622/RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) for providing the 2004 LCD library for Pico.

# First Boot

## Calibrate the HX Parameters

Calibrate the HX711 pressure sensor

 calibration factor. It is essential to recalibrate when using it for the first time or when replacing the load cell or HX711 circuit board.

Calibration method:
1. Attach one end of an external tension gauge to the stringing machine and the other end to a badminton string.
2. Set the HX parameter in the LCD settings page to 20.00.
3. Return to the main menu and set the tension to 20 pounds.
4. Press the up or down key to start stringing. When the LCD displays 20 pounds, write down the value displayed on the tension gauge.
5. Enter the recorded tension gauge value in the HX parameter in the settings page.

> [!WARNING]
> If you skip this calibration, there may be discrepancies between the actual tension and the tension displayed on the LCD.

> [!IMPORTANT]
> This parameter is saved in the configuration file (config.cfg).

Reference Video: [https://youtu.be/JaplgmXzbjY](https://youtu.be/JaplgmXzbjY)

## Set the CC Parameter
When the motor stops at the specified tension, the actual tension may continue to change. Therefore, this coefficient is set for calibration. You can manually set it or automatically calibrate it in the settings page.

Calibration method:
1. Secure the badminton string, with one end tied to the stringing machine and the other to the pearl clamp.
2. In the LCD settings page, select "AUTO" for the CC field and press the up or down key to start stringing.
3. "AUTO" will automatically fill in the reference CC value.
4. Use this value to test stringing. The optimal result is when the pre-stretch is set to 0, the specified tension is reached without fine-tuning. (You may see the tension continue to change beyond the specified tension when the motor stops; this is a normal physical phenomenon. The best parameters ensure that the tension stabilizes, and no fine-tuning is performed after reaching the specified tension.)
5. If the automatic CC value is not ideal, manually fine-tune the CC value in the settings page and repeat step 4 to find the best value.

> [!WARNING]
> If pre-stretch is applied, it will perform a pound reduction calibration. Therefore, set the pre-stretch to 0 for testing.

> [!IMPORTANT]
> Changing the HX711 circuit board, sliding table screw pitch, or motor will affect this coefficient. If you notice frequent fine-tuning when the pre-stretch is set to 0, you may need to calibrate this value.

> [!IMPORTANT]
> This parameter is saved in the configuration file (config.cfg).

Reference Video: [https://youtu.be/KuisR6eKiwk](https://youtu.be/KuisR6eKiwk)

# Conclusion
At present, the project already fulfills my stringing needs in terms of functionality, and I do not plan to add more features. However, if you have any suggestions, please feel free to share them with me.