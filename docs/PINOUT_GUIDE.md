# Pin Configuration Guide

## Overview

The jetson-orin-st7789 driver supports multiple pin configuration presets for popular ST7789 display modules. This makes it easy to use displays from different manufacturers without manually looking up pin numbers.

## Supported Presets

### 1. Waveshare (Raspberry Pi Compatible)

**Display**: Waveshare 2inch LCD Module (ST7789V)  
**Reference**: http://www.waveshare.com/wiki/2inch_LCD_Module

```python
from jetson_orin_st7789 import from_preset

display = from_preset('waveshare')
```

**Pinout**:
| Function | Board Pin | BCM GPIO | Waveshare Pin |
|----------|-----------|----------|---------------|
| VCC      | 1 or 17   | 3.3V     | VCC           |
| GND      | 6, 9, etc | Ground   | GND           |
| MOSI     | 19        | BCM 10   | DIN           |
| SCLK     | 23        | BCM 11   | CLK           |
| CS       | 24        | BCM 8    | CS            |
| DC       | 22        | BCM 25   | DC (DS)       |
| RST      | 13        | BCM 27   | RST           |
| BL       | 12        | BCM 18   | BL            |

**Notes**:
- Backlight (BL) can be connected to 3.3V for always-on
- Uses PH2.0 8-pin connector or standard pin headers

---

### 2. Adafruit (Raspberry Pi Compatible)

**Display**: Adafruit 2.0" 320x240 Color IPS TFT  
**Reference**: https://learn.adafruit.com/2-0-inch-320-x-240-color-ips-tft-display/python-wiring-and-setup

```python
from jetson_orin_st7789 import from_preset

display = from_preset('adafruit')
```

**Pinout**:
| Function | Board Pin | BCM GPIO | Adafruit Pin |
|----------|-----------|----------|--------------|
| VCC      | 1 or 17   | 3.3V     | Vin          |
| GND      | 6, 9, etc | Ground   | GND          |
| MOSI     | 19        | BCM 10   | MOSI         |
| SCLK     | 23        | BCM 11   | CLK          |
| CS       | 24        | BCM 8    | CS           |
| DC       | 22        | BCM 25   | D/C          |
| RST      | 18        | BCM 24   | RST          |

**Notes**:
- No separate backlight control pin
- Uses standard breadboard-friendly headers

---

### 3. Jetson (Default)

**Platform**: NVIDIA Jetson Orin/Xavier/Nano  
**Reference**: Current jetson-orin-st7789 default

```python
from jetson_orin_st7789 import from_preset

display = from_preset('jetson')
```

**Pinout**:
| Function | Board Pin | SoC Name        |
|----------|-----------|-----------------|
| VCC      | 1 or 17   | 3.3V            |
| GND      | 6, 9, etc | Ground          |
| MOSI     | 19        | spi1_mosi_pz5   |
| SCLK     | 23        | spi1_sck_pz3    |
| CS       | 24        | spi1_cs0_pz6    |
| DC       | 29        | soc_gpio32_pq5  |
| RST      | 31        | soc_gpio33_pq6  |

**Notes**:
- Requires device tree configuration for GPIO pins
- Use pin_inspector.py to verify pin configuration
- SPI should be enabled in device tree

---

## Comparison Table

| Preset    | DC Pin | RST Pin | Backlight | Best For |
|-----------|--------|---------|-----------|----------|
| Waveshare | 22     | 13      | Pin 12    | Raspberry Pi, Waveshare displays |
| Adafruit  | 22     | 18      | Always-on | Raspberry Pi, Adafruit displays |
| Jetson    | 29     | 31      | N/A       | NVIDIA Jetson platforms |

## Usage Examples

### Basic Usage with Preset

```python
from jetson_orin_st7789 import from_preset

# Use Waveshare pinout
with from_preset('waveshare') as display:
    display.fill((255, 0, 0))  # Red screen
```

### Preset with Custom Options

```python
from jetson_orin_st7789 import from_preset

# Waveshare in landscape mode
display = from_preset('waveshare', 
                     rotation=90, 
                     spi_speed_hz=100000000)
```

### List Available Presets

```python
from jetson_orin_st7789 import list_presets

for name, description in list_presets().items():
    print(f"{name}: {description}")
```

Output:
```
waveshare: Waveshare 2inch LCD Module (ST7789V) - Raspberry Pi compatible pinout
adafruit: Adafruit 2.0" 320x240 IPS TFT (ST7789) - Raspberry Pi compatible pinout
jetson: Common pinout for Jetson Orin/Xavier (requires device tree config)
```

### Print Preset Details

```python
from jetson_orin_st7789 import print_preset_info

# Print one preset
print_preset_info('waveshare')

# Print all presets
print_preset_info()
```

### Manual Pin Configuration

If you need custom pins:

```python
from jetson_orin_st7789 import ST7789, PinConfig

# Create custom configuration
my_config = PinConfig(
    dc_pin=15,
    rst_pin=16,
    spi_port=0,
    spi_cs=0,
    name="Custom",
    description="My custom pinout"
)

# Use it
display = ST7789(
    dc_pin=my_config.dc_pin,
    rst_pin=my_config.rst_pin
)
```

## Platform-Specific Notes

### Raspberry Pi

Both Waveshare and Adafruit presets are designed for Raspberry Pi and should work out of the box:

```bash
# Enable SPI
sudo raspi-config
# Interface Options -> SPI -> Enable

# Test
python3 -c "from jetson_orin_st7789 import from_preset; \
            d = from_preset('waveshare'); \
            d.fill((0,255,0)); \
            d.cleanup()"
```

### NVIDIA Jetson

The Jetson preset requires device tree configuration:

```bash
# 1. Check pin configuration
sudo python3 tools/pin_inspector.py 29
sudo python3 tools/pin_inspector.py 31

# 2. If not configured, apply device tree overlays
# (See SETUP_CHECKLIST.md for details)

# 3. Test
python3 -c "from jetson_orin_st7789 import from_preset; \
            d = from_preset('jetson'); \
            d.fill((0,255,0)); \
            d.cleanup()"
```

## Wiring Diagrams

### Waveshare Wiring

```
Display          Jetson/RPi
┌─────────┐      ┌──────────┐
│ VCC     ├──────┤ Pin 1    │ (3.3V)
│ GND     ├──────┤ Pin 6    │ (Ground)
│ DIN     ├──────┤ Pin 19   │ (MOSI)
│ CLK     ├──────┤ Pin 23   │ (SCLK)
│ CS      ├──────┤ Pin 24   │ (CE0)
│ DC      ├──────┤ Pin 22   │ (GPIO 25/DC)
│ RST     ├──────┤ Pin 13   │ (GPIO 27/RST)
│ BL      ├──────┤ Pin 12   │ (GPIO 18/PWM - optional)
└─────────┘      └──────────┘
```

### Adafruit Wiring

```
Display          Jetson/RPi
┌─────────┐      ┌──────────┐
│ Vin     ├──────┤ Pin 1    │ (3.3V)
│ GND     ├──────┤ Pin 6    │ (Ground)
│ MOSI    ├──────┤ Pin 19   │ (MOSI)
│ CLK     ├──────┤ Pin 23   │ (SCLK)
│ CS      ├──────┤ Pin 24   │ (CE0)
│ D/C     ├──────┤ Pin 22   │ (GPIO 25/DC)
│ RST     ├──────┤ Pin 18   │ (GPIO 24/RST)
└─────────┘      └──────────┘
```

## Pin Conversion Utilities

The driver includes utilities for converting between BCM and Board pin numbering:

```python
from jetson_orin_st7789.pinouts import bcm_to_board, board_to_bcm

# Convert BCM GPIO 25 to Board pin
board_pin = bcm_to_board(25)  # Returns 22

# Convert Board pin 22 to BCM GPIO
bcm_pin = board_to_bcm(22)    # Returns 25
```

## Troubleshooting

### Display Not Working

1. **Verify preset choice**:
   ```python
   from jetson_orin_st7789 import print_preset_info
   print_preset_info('waveshare')  # Check if pins match your wiring
   ```

2. **Check physical connections**:
   - Ensure all wires are properly seated
   - Verify VCC is connected to 3.3V (NOT 5V!)
   - Check ground connection

3. **Test SPI**:
   ```bash
   # On Raspberry Pi
   ls -l /dev/spidev0.0
   
   # On Jetson
   ls -l /dev/spidev*
   ```

4. **Verify GPIO pins** (Jetson only):
   ```bash
   sudo python3 tools/pin_inspector.py 29
   sudo python3 tools/pin_inspector.py 31
   ```

### Wrong Colors or Garbled Display

- Verify you're using the correct preset for your display
- Check SPI speed (try reducing to 62.5 MHz):
  ```python
  display = from_preset('waveshare', spi_speed_hz=62500000)
  ```

### Preset Not Found

```python
from jetson_orin_st7789 import list_presets

# Check available presets
print("Available presets:", list(list_presets().keys()))
```

## Creating Custom Presets

To add a custom preset to your project:

```python
# my_presets.py
from jetson_orin_st7789.pinouts import PinConfig, PRESETS

# Define your custom configuration
MY_DISPLAY = PinConfig(
    dc_pin=15,
    rst_pin=16,
    spi_port=0,
    spi_cs=0,
    name="MyDisplay",
    description="Custom display configuration"
)

# Add to presets
PRESETS['mydisplay'] = MY_DISPLAY

# Now you can use it
from jetson_orin_st7789 import from_preset
display = from_preset('mydisplay')
```

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [PIN_INSPECTOR_GUIDE.md](docs/PIN_INSPECTOR_GUIDE.md) - GPIO diagnostic tool
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Complete setup guide
- [Waveshare Wiki](http://www.waveshare.com/wiki/2inch_LCD_Module)
- [Adafruit Learn Guide](https://learn.adafruit.com/2-0-inch-320-x-240-color-ips-tft-display)

## Contributing Presets

Have a display configuration to share? Contributions welcome!

1. Test your configuration thoroughly
2. Document the display model and source
3. Submit a pull request with:
   - Pin configuration in `pinouts.py`
   - Wiring diagram or photo
   - Test results on your platform

---

**Last updated**: 2025-12-08  
**Version**: 1.0.0
