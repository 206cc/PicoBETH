[![cht](https://img.shields.io/badge/lang-cht-green.svg)](README.cht.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# PicoBETH on Pico2

Some users have mistakenly purchased the Raspberry Pi Pico 2 (RP2350), while others have inquired about upgrading to Pico 2. This branch explains the current status of **PicoBETH** migration to **Pico 2** and the test results.

## Issues and Challenges

Pico 2 uses the **RP2350** microcontroller, which has a known **E9 Erratum**, causing **abnormal behavior in the built-in pull-down resistors**.  
Since this project relies on internal pull-down resistors for all button detections, **Pico 2 is not directly compatible**. The solutions are as follows:

1. **Add external pull-down resistors** to ensure proper button detection.
2. **Modify the circuit design to use pull-up buttons**, utilizing the built-in **pull-up resistors** instead.

For more details on the RP2350 E9 erratum, refer to the following articles:

- [Hardware Bug In Raspberry Pi’s RP2350 Causes Faulty Pull-Down Behavior](https://hackaday.com/2024/08/28/hardware-bug-in-raspberry-pis-rp2350-causes-faulty-pull-down-behavior/)
- [RP2350: Internal pull down issue](https://forums.pimoroni.com/t/rp2350-internal-pull-down-issue/25360)

## Modifications and Adjustments

To resolve this issue, I have implemented **hardware modifications** and **software adjustments**:

### Hardware Modifications
- **Redesigned PCB**, converting all buttons and microswitches to a pull-up button circuit design.

### Software Adjustments
- **Revised button and microswitch input logic**, switching to internal pull-up resistors.
- **Adjusted stepper motor parameters** to allow operation near maximum speed.

## Test Results

The following video compares Raspberry Pi **Pico** and **Pico 2** running PicoBETH:  
[![VIDEO](https://img.youtube.com/vi/p8Iu2A8doCQ/0.jpg)](https://www.youtube.com/watch?v=p8Iu2A8doCQ)

## Conclusion

1. **Pico 2 is only noticeably faster during startup**, but it shows no significant advantage in button operation, string tensioning, or carriage resetting.
2. **Pico has proven stability and maturity in this project**, with over a million tensioning cycles tested and verified for reliability.
3. **Pico is more cost-effective and widely available**, while **Pico 2 does not provide enough benefits to justify migration**.

### **This project will not be migrated to Pico 2**. We recommend continuing to use **Raspberry Pi Pico** to ensure stability and compatibility.
