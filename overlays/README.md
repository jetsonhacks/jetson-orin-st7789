# Device Tree Overlays

Device tree overlays for ST7789 displays are maintained in a separate repository for better reusability and modularity.

## Overlay Repository

**→ [jetson-orin-spi-overlay-guide](https://github.com/yourusername/jetson-orin-spi-overlay-guide/tree/main/examples/st7789)**

The overlay repository provides:
- Three pre-configured overlays (Jetson default, Waveshare, Adafruit)
- Automated installation scripts with FDT auto-detection
- Pin verification tools
- Reusable templates for custom configurations
- Comprehensive documentation on device trees

## Quick Links

### Overlay Files
- [Jetson Default](https://github.com/yourusername/jetson-orin-spi-overlay-guide/tree/main/examples/st7789/jetson-default)
- [Waveshare](https://github.com/yourusername/jetson-orin-spi-overlay-guide/tree/main/examples/st7789/waveshare)
- [Adafruit](https://github.com/yourusername/jetson-orin-spi-overlay-guide/tree/main/examples/st7789/adafruit)

### Documentation
- [Device Tree Basics](https://github.com/yourusername/jetson-orin-spi-overlay-guide/blob/main/docs/DEVICE_TREE_BASICS.md)
- [FDT Configuration](https://github.com/yourusername/jetson-orin-spi-overlay-guide/blob/main/docs/FDT_CONFIGURATION.md)

## Why Separate Repository?

The overlay guide is kept separate because:
1. **Reusability** - The overlay guide supports multiple SPI devices, not just ST7789
2. **Modularity** - Hardware configuration independent of Python driver
3. **Broader Audience** - Users may need overlays without Python driver

## Installation

See [Hardware Setup Guide](../docs/HARDWARE_SETUP.md) for complete installation instructions.
