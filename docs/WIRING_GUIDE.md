# Wiring Guide

Detailed wiring information for ST7789 displays on Jetson Orin.

## Pin Configurations

### Jetson Default Configuration
- DC (Data/Command): Pin 29 (GPIO)
- RST (Reset): Pin 31 (GPIO)
- Overlay: `jetson-orin-st7789-default.dtbo`

### Waveshare Configuration  
- DC (Data/Command): Pin 13 (GPIO)
- RST (Reset): Pin 22 (GPIO)
- Overlay: `jetson-orin-st7789-waveshare.dtbo`

### Adafruit Configuration
- DC (Data/Command): Pin 18 (GPIO)
- RST (Reset): Pin 22 (GPIO)
- Overlay: `jetson-orin-st7789-adafruit.dtbo`

### Common SPI Pins (All Configurations)
- MOSI: Pin 19 (SPI1_MOSI)
- MISO: Pin 21 (SPI1_MISO)
- SCK: Pin 23 (SPI1_SCK)
- CS: Pin 24 (SPI1_CS0)
- GND: Pin 25 (Ground)
- 3.3V: Pin 17 (3.3V Power)

## Wiring Diagrams

[Add diagrams here or link to external resources]

## Hardware Connection Tips

1. **Power:** Always use 3.3V, never 5V
2. **Ground:** Connect display GND to Jetson GND
3. **Cable Length:** Keep SPI wires short (<6 inches) for reliability
4. **Double Check:** Verify pin numbers before powering on

## Verification

After wiring, before installing overlay:
```bash
# Check pin numbers match your configuration
# Use a multimeter to verify connections if unsure
```
