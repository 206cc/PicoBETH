![images1-1](docs/img_hw3d.jpg)

[![cht](https://img.shields.io/badge/lang-cht-green.svg)](README.cht.md) 
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# PicoBETH HW 3D-Printed Version
> [!CAUTION]
> The documentation for this 3D-Printed project is still being revised. If you have any questions, feel free to ask and discuss in the community.

> [!CAUTION]
> This branch mainly replaces the components in the main branch that require complex machining with 3D-printed parts, significantly simplifying the production process. Before starting this 3D-printed branch, please thoroughly read the [main branch](https://github.com/206cc/PicoBETH) documentation to understand the relevant information and precautions.

## Table of Contents
- [3D-Printed Parts Download](#3d-printed-parts-download)
- [3D Viewing Model (Non-Printable)](#3d-viewing-model-non-printable)
- [Assembly Video](#assembly-video)
- [Parts List](#parts-list)
  - [Main Components](#main-components)
  - [Screw List](#screw-list)
- [Notes](#notes)
  - [3D Part-1](#3d-part-1)
    - [Sliding Table Fixing Screws](#sliding-table-fixing-screws)
  - [3D Part-3](#3d-part-3)
    - [Fixing Screws](#fixing-screws)
  - [Load Cell Signal Wires](#load-cell-signal-wires)
  - [Load Cell Installation Direction](#load-cell-installation-direction)
  - [Adapter Base](#adapter-base)
- [Support](#support)

## 3D-Printed Parts Download
[PicoBETH HW 3D Printed Version](https://www.thingiverse.com/thing:6913170)

> [!CAUTION]
> Avoid using PLA for printing as its strength may degrade over time.

## 3D Viewing Model (Non-Printable)

[PicoBETH HW 3D Viewing Model](https://www.tinkercad.com/things/4lv9ptAmuc4-picobeth-hw-3d-viewing-model)

## Assembly Video

Please refer to the [Assembly Video](https://youtube.com/shorts/kR_JLVGHwB8) on YouTube for detailed instructions.

## Parts List

### Main Components

![parts](docs/img_bomlist.jpg)

| No. | Name                                |
|-----|-------------------------------------|
| 1   | Part-1 Main Body                   |
| 2   | Part-2 Rear Limit Mount          |
| 3   | Part-3 Load Cell bracket             |
| 4   | Part-4 PCB and TB6600 Mount        |
| 5   | Part-5 Power and Switch Cover      |
| 6   | Part-6 LCD and Button Mount        |
| 7   | Part-7 Rear Cover                  |
| 8   | SGX 1610 200mm Sliding Table       |
| 9   | PCB Mainboard, Raspberry Pico, SparkFun HX711, Buzzer |
| 10  | PCB Button Board                   |
| 11  | 2004 i2c LCD                       |
| 12  | TB6600 Stepper Motor Driver        |
| 13  | NJ5 20kg Load Cell (YZC-133)       |
| 14  | WISE 2086 Clip Head                |
| 15  | Activation Switch Mount            |
| 16  | Ø4 20cm Wire Wrap                  |
| 17  | Switch 12cm                        |
| 18  | DC Jack Cable 15cm                 |
| 19  | Mainboard Power Cable 20cm         |
| 20  | TB6600 Power Cable 28cm            |
| 21  | XH2.54mm 4P Stepper Motor Signal Cable 15cm |
| 22  | XH2.54mm 2P Front Limit Switch Cable 20cm |
| 23  | XH2.54mm 2P Rear Limit Switch Cable 20cm |
| 24  | XH2.54mm 4P LED Signal Cable (Same Direction) 25cm |
| 25  | XH2.54mm 2P Cancel Button Cable (Same Direction) 25cm |
| 26  | XH2.54mm 6P Five-Way Button Cable (Same Direction) 25cm |
| 27  | XH2.54mm 4P LCD Signal Cable 40cm |
| 28  | XH2.54mm 2P Clip Activation Switch Cable 50cm |

> [!WARNING]  
> **Note:** Power cables must not be thinner than **18 AWG**.

### Screw List

![parts](docs/img_screw_list.jpg)

| No. | Name                           | Quantity |
|-----|--------------------------------|----------|
| A   | Gray Spring Wire Connectors    | 3        |
| B   | M3 × 10mm Self-Tapping Screws  | 8        |
| C   | M3 × 6mm Self-Tapping Screws   | 15       |
| D   | M2.6 × 10mm Self-Tapping Screws| 4        |
| E   | M3 × 6mm Round-Head Screws     | 2        |
| F   | M4 × 16mm Hex Screws           | 4        |
| G   | M4 × 20mm Hex Screws           | 4        |
| H   | M4 × 30mm Hex Screws           | 2        |
| I   | M4 × 8mm Hex Screws            | 2        |
| J   | M4 Spring Washers              | 10       |
| K   | M4 Flat Washers                | 10       |
| L   | M5 × 70mm Hex Screws + Washers | 2        |

## Notes

### 3D Part-1

![part1](docs/img_3d_part1.jpg)

The main body needs to withstand significant deformation forces. It is recommended to use the following print settings:
- **Wall Thickness:** At least 5mm  
- **Infill:** At least 30%  

#### Sliding Table Fixing Screws
The sliding table screws should protrude 3.5~4.5mm from the platform. If they are too long, the sliding table may not sit flush with the platform. Please add washers as needed for adjustment. It is recommended to first tighten the 2 screws on the bottom in order, followed by the 4 screws on the sides.

- **Bottom Fixing Screws:**  
  2 sets of M4 × 30mm screws, each with a flat washer and a spring washer.
  Torque: 1.5N·m

- **Side Fixing Screws:**  
  4 sets of M4 × 20mm screws, each with a flat washer and a spring washer.
  Torque: 1.5N·m

> [!CAUTION]
> Tighten screws to the recommended torque to avoid damaging the 3D-printed parts.

### 3D Part-3

![part3](docs/img_3d_part3.jpg)

This part serves as the mounting bracket for the Load Cell and the sliding table. It needs to withstand significant forces. Recommended print settings:
- **Infill:** 100%  

#### Fixing Screws
- **Load Cell Fixing Screws:**  
  2 sets of M5 × 70mm screws with flat washers.
  Torque: 2.0N·m

- **Sliding Table Mount Fixing Screws:**  
  4 sets of M4 × 16mm screws, each with a flat washer and a spring washer.
  Torque: 1.5N·m

> [!CAUTION]
> Tighten screws to the recommended torque to avoid damaging the 3D-printed parts.

### Load Cell Signal Wires

![hx711_loadcell](docs/img_hx711_loadcell.jpg)

Due to design constraints, the Load Cell's installation direction is reversed compared to HW1 and HW2. Swap the green and white signal wires on the connector to detect the correct force direction. Incorrect wiring may result in the tension being measured in the opposite direction.

### Load Cell Installation Direction

Pay attention to the installation direction of the Load Cell. The NJ5 YZC-133 shown in the video has a different installation direction compared to most other YZC-133 models. If using other brands, the Load Cell may need to be rotated 180 degrees. Refer to [EP.5 Supplement - Slope Adjustment and YZC-133 Load Cell](https://youtube.com/22Ev_kWTnxk) for details.

### Adapter Base

You will still need to design an adapter base to mount it onto the stringing machine platform. Refer to [EP.9 Positioning and Fixing](https://youtube.com/Ax4agdsqyms). It is recommended to use M8 screws with flat washers and follow the torque specification of 3.0 N·m during installation.

# Support
If you have any questions or suggestions for improvement, feel free to leave a comment in the discussion forum or under the YouTube videos. Once you complete the project, we also welcome you to share photos of your results in the forum.
