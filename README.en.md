[![cht](https://img.shields.io/badge/lang-cht-green.svg)](https://github.com/206cc/PicoBETH/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/206cc/PicoBETH/blob/main/README.en.md)
# PicoBETH
PicoBETH (Raspberry Pico Badminton Electronic Tension Head) is an open-source project that allows amateur stringers who enjoy stringing but only have access to mechanical stringing machines (e.g., drop-weight or manual machines) to create their own electronic tensioning head. If you have some basic programming skills, this project should be relatively straightforward to complete.

![images1-1](docs/images1-1.jpg)

Modification with Weight and Components
![images1-2](docs/images1-2.jpg)

15lb and 30lb 10% Pre-Stretch Demonstration Video
[https://youtu.be/82X5WgdFZp8](https://youtu.be/82X5WgdFZp8)

Production Model
![images1-2](docs/images1-6.jpg)

Improvements on the Production Model Include:
1. Added screw dust cover.
2. Switched to 1610 specification for the screw, increasing tensioning speed.
3. More reasonable hardware layout, allowing individual parts to be disassembled without full disassembly.
4. Reduced size by stacking components, avoiding interference with storage trays.
5. Used a custom-designed PCB.

## Motivation
About a year ago, due to a company social club, I began playing badminton. Despite not being very skilled, I became passionate about stringing. I bought a drop-weight stringing machine and initially planned to purchase an electronic tensioning head. However, I realized that I could use my knowledge to create this project with a Raspberry Pico, pressure sensors, microswitches, and buttons.

## Key Features
The main features of PicoBETH include:

1. Tension setting in pounds or kilograms.
2. Pre-Stretch function.
3. Automatic fine-tuning after tensioning.
4. Tension zeroing on startup.
5. Tension coefficient setting.
6. Tension calibration.
7. Stringing timer.
8. Tensioning counter.

## Standby Screen
1. Use the left and right keys to select the settings for adjusting pounds, kilograms, tens, units, and decimals.
2. Use the up and down keys to adjust the selected settings.
3. Stringing timer function: Press the exit key to start the timer, press it again to stop the timer, and press it a third time to reset the timer.
![images1-3](docs/images1-3.png)

## Tensioning Screen
1. When the set tension is reached, the fine-tuning process begins. If the tension is too low, it adds pounds; if it's too high, it reduces pounds until you press the clamp key or exit key to end the tensioning process.
2. You can also enter manual fine-tuning mode by pressing the up and down keys, which cancels the automatic fine-tuning process. Press the center key on the five-way key to re-enter automatic fine-tuning mode.
3. Once the set tension is reached, a timer starts counting.

![images1-4](docs/images1-4.png)

> [!WARNING]
> If the fine-tuning range is too high or too low, you can adjust the FT_ADD parameter.

## Setting Screen
1. UN: Choose between pounds or kilograms as the unit.
2. CC: Fine-tuning parameter (see the First Startup section for details).
3. HX: Calibration of the HX711 pressure sensor (see the First Startup section for details).
4. FT: The amount of fine-tuning to perform when the specified tension is reached.
![images1-5](docs/images1-5.png)
  
> [!NOTE]
> In general, once you've configured the settings, you won't need to revisit this screen frequently.

## Hardware

Primary Materials:
1. Raspberry Pico H
2. 1610 200MM Sliding Table
3. 57 Stepper Motor (1.8° Step Angle, 2 Phase, 4 Wire)
4. TB6600 Stepper Motor Driver
5. NJ5 20KG Load Cell
6. HX711 IC
7. 2004 I2C LCD
8. WISE 2086 Head
9. Five-way Key Module
10. Button
11. Micro Switch
12. Active Buzzer
13. Tri-Color LEDs

![images2-1](docs/images2-1.jpg)

## Wiring Diagram
![images2-2](docs/images2-2.png)
> [!WARNING]
> Be sure to incorporate safety measures, such as pull-up resistors for the buttons, fuses for the stepper motor, and current-limiting resistors for the LEDs to protect the Raspberry Pi Pico and the motor.

## PCB Circuit Board
![images2-3](docs/images2-4.svg)

> [!NOTE]
> You can download the circuit board to avoid the hassle of hand-soldering.

> [!NOTE]
> The locking points around the circuit board correspond to the locations of a 2004 LCD, allowing for stacking to reduce the overall size.

## TB6600 Stepper Motor Parameters
![images2-3](docs/images2-3.png)

> [!WARNING]
> Modifying the parameters of this stepper motor may require adjusting many other parameters in the code.

# Software Installation
Use Thonny to save the following code files to your Raspberry Pico. The `src` folder contains the relevant libraries for HX711 and the 2004 LCD.

1. main.py
2. src\hx711.py
3. src\lcd_api.py
4. src\pico_i2c_lcd.py

> [!NOTE]
> Special thanks to [https://github.com/endail/hx711-pico-mpy](https://github.com/endail/hx711-pico-mpy) for providing the hx711 library for the Raspberry Pi Pico.

> [!NOTE]
> Special thanks to [https://github.com/T-622/RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) for providing the 2004 LCD library for the Raspberry Pi Pico.

# First Startup

## Calibrating the HX Parameters

Calibrate the HX711 pressure sensor coefficient when using it for the first time or when replacing the pressure sensor or HX711 circuit board. Calibration process:

1. Attach the external tension gauge, securing one end to the stringing machine and the other end to the badminton string.
2. Set the HX parameter in the LCD settings to 20.00.
3. Return to the main menu and set the tension to 20 pounds.
4. Use the up or down keys to start the stringing process. When the LCD displays 20 pounds, record the tension gauge reading.
5. Enter the recorded tension gauge value in the settings page.

> [!WARNING]
> Failure to perform this calibration may result in discrepancies between the actual tension and the tension displayed on the LCD.

> [!IMPORTANT]
> This parameter is primarily saved in the configuration file (config.cfg).

Reference Video: [https://youtu.be/JaplgmXzbjY](https://youtu.be/JaplgmXzbjY)

## Setting CC Parameters


When the set tension is reached, the actual tension may continue to change. This CC coefficient should be calibrated manually or automatically from the settings page. Calibration process:

1. Secure the badminton string, with one end attached to the stringing machine and the other end in the clamp.
2. In the LCD settings page, select AUTO in the CC field and use the up or down keys to start the stringing process.
3. AUTO will automatically fill in the reference CC value.
4. Use this value to conduct a stringing test. The optimal result is achieving the specified tension without any fine-tuning when the pre-stretch is set to 0.
   (You may observe that the tension on the LCD continues to change beyond the specified tension when the motor stops. This is a normal physical phenomenon. The best parameter is one where the tension balances once reached, and no fine-tuning is required.)
5. If the automatically determined CC value is not ideal, manually fine-tune the CC value from the settings page and repeat step 4 to find the best value.

> [!WARNING]
> If the pre-stretch is enabled, it will perform a pound-back check, so set the pre-stretch to 0 when testing.

> [!IMPORTANT]
> Changing the HX711 circuit board, lead screw pitch, or motor can impact this coefficient. If you find frequent fine-tuning when the pre-stretch is set to 0, consider calibrating this value.

> [!IMPORTANT]
> This parameter is primarily saved in the configuration file (config.cfg).

Reference Video: [https://youtu.be/KuisR6eKiwk](https://youtu.be/KuisR6eKiwk)

# Conclusion
The current functionality of the machine meets my stringing needs, and there are no plans to add more features at this time. However, if you have any valuable suggestions, please feel free to share them with me.
