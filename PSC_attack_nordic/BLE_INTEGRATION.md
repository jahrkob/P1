# BLE Integration Guide for Nordic nRF52

This document provides guidance for adding Bluetooth Low Energy (BLE) capabilities to the PSC attack demonstration, addressing issue #40.

## Overview

Nordic nRF52 series chips have built-in BLE support. This guide shows how to add BLE UART service for wireless password entry and monitoring.

## Prerequisites

- Nordic nRF52840 or nRF52832 board
- Arduino IDE with Nordic board support OR PlatformIO
- BLE UART library (Adafruit Bluefruit nRF52 or Nordic SoftDevice)

## BLE Architecture

### Services to Implement

1. **BLE UART Service** - For wireless password entry
2. **BLE Device Information Service** - Basic device info
3. **Custom PSC Service** (optional) - Power monitoring data

## Code Example - Adding BLE UART

```cpp
#include <bluefruit.h>

// BLE UART Service
BLEUart bleuart;

void setup() {
  Serial.begin(115200);
  
  // Initialize Bluefruit
  Bluefruit.begin();
  Bluefruit.setName("PSC-Attack-Demo");
  
  // Configure and Start BLE UART Service
  bleuart.begin();
  
  // Set up advertising
  startAdv();
  
  // Original PSC setup
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(button3, INPUT_PULLUP);
  pinMode(button4, INPUT_PULLUP);
  pinMode(buzzer, OUTPUT);
  
  Serial.println("PSC Attack Demo - BLE Enabled");
}

void startAdv(void) {
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  
  // Include BLE UART service
  Bluefruit.Advertising.addService(bleuart);
  
  // Set advertising interval (in units of 0.625 ms)
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);
  Bluefruit.Advertising.setFastTimeout(30);
  Bluefruit.Advertising.start(0);
}

void loop() {
  // Check for BLE UART data
  if (bleuart.available()) {
    uint8_t ch = bleuart.read();
    if (ch >= '1' && ch <= '4') {
      curPass += (char)ch;
      bleuart.print((char)ch); // Echo back
    }
  }
  
  // Original button handling code...
  // ... (keep existing button code)
  
  // Password validation
  if (curPass.length() >= 4) {
    buttonBuzz(buzzer);
    if (curPass.equals(pass)) {
      Serial.println("You in");
      bleuart.println("ACCESS GRANTED");
    } else {
      Serial.println("WRONG!");
      bleuart.println("ACCESS DENIED");
    }
    curPass = "";
  }
  
  delay(2);
}
```

## Required Libraries

### Arduino IDE
```cpp
#include <bluefruit.h>  // For Adafruit nRF52 boards
```

Install via Library Manager:
- Adafruit Bluefruit nRF52 Libraries

### PlatformIO
Add to `platformio.ini`:
```ini
lib_deps = 
    adafruit/Adafruit Bluefruit nRF52 Libraries @ ^0.21.0
```

## Testing BLE Connection

### Mobile Apps
- **nRF Connect** (Android/iOS) - Nordic Semiconductor's official app
- **Bluefruit Connect** (Android/iOS) - Adafruit's BLE UART app
- **Serial Bluetooth Terminal** (Android)

### Desktop Tools
- **Web Bluetooth API** - Chrome browser (requires HTTPS)
- **nRF Connect Desktop** - Nordic Semiconductor's desktop app
- **LightBlue** (macOS) - BLE explorer

## Security Considerations

⚠️ **WARNING**: This is an educational demonstration only!

### Known Vulnerabilities
1. **No encryption** - Password transmitted in clear text over BLE
2. **No authentication** - Any device can connect
3. **Side-channel leakage** - BLE transmission patterns reveal timing information
4. **Power analysis** - BLE radio consumption creates additional side-channel vectors

### Improvements for Production
- Implement BLE pairing/bonding
- Use encrypted characteristics
- Add connection authentication
- Implement rate limiting
- Use Nordic's SoftDevice security features

## Power Analysis with BLE

BLE adds interesting power consumption patterns:

1. **Advertising events** - Periodic spikes (~10-20mA)
2. **Connection events** - Regular intervals (7.5-4000ms)
3. **Data transmission** - Additional spikes during TX/RX
4. **Radio calibration** - Temperature-dependent patterns

These can be analyzed for:
- Protocol reverse engineering
- Timing attack vectors
- State machine analysis
- Key extraction from encryption operations

## Advanced Features

### Custom BLE Services

Create a custom GATT service for power monitoring:

```cpp
// Custom PSC Service UUID
#define PSC_SERVICE_UUID "12345678-1234-5678-1234-56789abcdef0"
#define POWER_CHAR_UUID  "12345678-1234-5678-1234-56789abcdef1"

BLEService pscService(PSC_SERVICE_UUID);
BLECharacteristic powerChar(POWER_CHAR_UUID);

void setupCustomService() {
  pscService.begin();
  
  powerChar.setProperties(CHR_PROPS_READ | CHR_PROPS_NOTIFY);
  powerChar.setPermission(SECMODE_OPEN, SECMODE_NO_ACCESS);
  powerChar.setFixedLen(4); // 4 bytes for power reading
  powerChar.begin();
}
```

### Low Power Modes

Nordic chips support multiple power modes:
- **ON mode** - Full functionality (~15mA)
- **Constant Latency** - Quick wake-up (~5mA)
- **Low Power** - Slower wake-up (~1mA)
- **System OFF** - Deepest sleep (<1µA)

```cpp
// Enable DC/DC converter for better efficiency
Bluefruit.configPrphBandwidth(BANDWIDTH_LOW);
```

## Related Issues

- #37 - Brug nordic semiconductor (This implementation)
- #40 - BLE (Bluetooth Low Energy integration)
- #38 - MQTT (Could be bridged via BLE gateway)
- #39 - CoAP (Could be implemented over BLE)

## References

- [Nordic nRF52840 Product Specification](https://infocenter.nordicsemi.com/pdf/nRF52840_PS_v1.7.pdf)
- [Adafruit nRF52 Arduino Core](https://github.com/adafruit/Adafruit_nRF52_Arduino)
- [Nordic SoftDevice Documentation](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.s140.api/index.html)
- [BLE UART Service Specification](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/uart-service)

## Next Steps

1. Implement basic BLE UART service
2. Test wireless password entry
3. Add BLE security features
4. Create custom PSC service for power data
5. Implement BLE-based side-channel analysis
6. Document BLE protocol vulnerabilities
