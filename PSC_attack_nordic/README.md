# PSC Attack Demo - Nordic Semiconductor Version

This version of the PSC (Power Side-Channel) attack demonstration is optimized for Nordic Semiconductor nRF52 series microcontrollers.

## Supported Hardware

- **Nordic nRF52832** - Bluetooth 5.0 SoC with ARM Cortex-M4F
- **Nordic nRF52840** - Advanced Bluetooth 5.2 SoC with ARM Cortex-M4F
- **Compatible development boards:**
  - Adafruit Feather nRF52840
  - Arduino Nano 33 BLE (nRF52840)
  - Particle Xenon (nRF52840)
  - Nordic nRF52840 DK
  - Seeed XIAO BLE (nRF52840)

## Features

- Compatible with Nordic nRF52 series microcontrollers
- Optimized for low-power operation
- Ready for BLE integration (future enhancement)
- Efficient memory usage with bit flag state management
- Suitable for power analysis and side-channel attack demonstrations

## Pin Configuration

The default pin configuration is:

```cpp
#define buzzer 3
#define button1 8
#define button2 7
#define button3 6
#define button4 5
```

**Note:** Adjust these pins based on your specific Nordic development board. Check your board's pinout diagram for available GPIO pins.

## Hardware Setup

1. Connect 4 push buttons to the specified GPIO pins
2. Each button should be connected between the GPIO pin and GND
3. Internal pull-up resistors are enabled in the code
4. Connect a piezo buzzer or LED to pin 3 for feedback

## Installation

### Arduino IDE

1. Install the [Adafruit nRF52 BSP](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup) for Arduino IDE
2. Or install the [Arduino nRF52 mbed core](https://docs.arduino.cc/software/ide-v1/tutorials/getting-started/cores/arduino-mbed_nano) for Arduino Nano 33 BLE
3. Select your Nordic board from the Tools > Board menu
4. Open `PSC_attack_nordic.ino`
5. Upload to your board

### PlatformIO

Add the appropriate platform to your `platformio.ini`:

```ini
[env:nordic_nrf52840]
platform = nordicnrf52
board = adafruit_feather_nrf52840
framework = arduino
```

## Usage

1. Upload the sketch to your Nordic board
2. Open Serial Monitor at 115200 baud
3. Press buttons 1-4 to enter a 4-digit code
4. Default password is "4443"
5. The buzzer will sound when 4 digits are entered
6. Check serial output for "You in" or "WRONG!" message

## Power Side-Channel Analysis

This code is designed for demonstrating power side-channel attacks:

- The password comparison happens in constant time for each character
- Power consumption varies based on button presses
- The Nordic nRF52 series has excellent ADC capabilities for power measurement
- Consider using the built-in SAADC (Successive Approximation ADC) for power analysis

## Future Enhancements

- [ ] Add BLE UART service for wireless password entry
- [ ] Implement Nordic SAADC for self-monitoring power consumption
- [ ] Add encryption demonstration using Nordic hardware AES
- [ ] Low-power mode optimization using Nordic SD (SoftDevice)

## Security Note

This code is for educational purposes only. It demonstrates basic password validation vulnerable to side-channel attacks. Do not use this in production systems.

## License

Part of the COMTEK P1 project "Programming and System Development"
