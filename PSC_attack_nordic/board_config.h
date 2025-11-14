/*
 * Board Configuration for Nordic Semiconductor nRF52 Series
 * 
 * This file contains pin mappings for different Nordic development boards.
 * Uncomment the board you're using, or define custom pins below.
 */

#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

// Uncomment ONE of the following board definitions:

// ============================================================================
// ADAFRUIT FEATHER nRF52840 EXPRESS
// ============================================================================
// #define BOARD_ADAFRUIT_FEATHER_NRF52840
#ifdef BOARD_ADAFRUIT_FEATHER_NRF52840
  #define BUZZER_PIN A0      // Pin A0 / D14
  #define BUTTON1_PIN 7      // Pin D7
  #define BUTTON2_PIN 11     // Pin D11
  #define BUTTON3_PIN 15     // Pin A1 / D15
  #define BUTTON4_PIN 16     // Pin A2 / D16
#endif

// ============================================================================
// ARDUINO NANO 33 BLE / NANO 33 BLE SENSE
// ============================================================================
// #define BOARD_ARDUINO_NANO33BLE
#ifdef BOARD_ARDUINO_NANO33BLE
  #define BUZZER_PIN 2       // Pin D2
  #define BUTTON1_PIN 3      // Pin D3
  #define BUTTON2_PIN 4      // Pin D4
  #define BUTTON3_PIN 5      // Pin D5
  #define BUTTON4_PIN 6      // Pin D6
#endif

// ============================================================================
// NORDIC nRF52840 DK (Development Kit)
// ============================================================================
// #define BOARD_NRF52840_DK
#ifdef BOARD_NRF52840_DK
  #define BUZZER_PIN 13      // LED1 on DK
  #define BUTTON1_PIN 11     // Button 1 on DK
  #define BUTTON2_PIN 12     // Button 2 on DK
  #define BUTTON3_PIN 24     // Button 3 on DK
  #define BUTTON4_PIN 25     // Button 4 on DK
  // Note: DK has built-in buttons on these pins
#endif

// ============================================================================
// SEEED XIAO BLE (nRF52840)
// ============================================================================
// #define BOARD_SEEED_XIAO_BLE
#ifdef BOARD_SEEED_XIAO_BLE
  #define BUZZER_PIN 0       // Pin D0
  #define BUTTON1_PIN 1      // Pin D1
  #define BUTTON2_PIN 2      // Pin D2
  #define BUTTON3_PIN 3      // Pin D3
  #define BUTTON4_PIN 4      // Pin D4
#endif

// ============================================================================
// PARTICLE XENON (nRF52840)
// ============================================================================
// #define BOARD_PARTICLE_XENON
#ifdef BOARD_PARTICLE_XENON
  #define BUZZER_PIN D2      // Pin D2
  #define BUTTON1_PIN D3     // Pin D3
  #define BUTTON2_PIN D4     // Pin D4
  #define BUTTON3_PIN D5     // Pin D5
  #define BUTTON4_PIN D6     // Pin D6
#endif

// ============================================================================
// CUSTOM / DEFAULT CONFIGURATION
// ============================================================================
// If no board is defined above, use these default pins
#ifndef BUZZER_PIN
  #define BUZZER_PIN 3
  #define BUTTON1_PIN 8
  #define BUTTON2_PIN 7
  #define BUTTON3_PIN 6
  #define BUTTON4_PIN 5
#endif

// ============================================================================
// NORDIC-SPECIFIC FEATURES
// ============================================================================

// Enable Nordic-specific optimizations
#if defined(NRF52832_XXAA) || defined(NRF52840_XXAA) || defined(ARDUINO_ARCH_NRF52)
  #define NORDIC_HARDWARE
  
  // Nordic nRF52 has 8 configurable priority levels (0-7)
  // Lower number = higher priority
  #define GPIO_IRQ_PRIORITY 3
  
  // Nordic SAADC (ADC) settings for power monitoring
  #define POWER_MONITOR_PIN A0
  #define ADC_RESOLUTION 12  // 12-bit ADC
  
  // Enable Nordic-specific features
  #define ENABLE_DCDC        // Enable DC/DC converter for better efficiency
  #define USE_LFXO           // Use external 32.768 kHz crystal
#endif

#endif // BOARD_CONFIG_H
