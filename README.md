# jetson-orin-st7789

Python driver for ST7789 LCD displays on NVIDIA Jetson Orin platforms.

[![Hardware Setup](https://img.shields.io/badge/Hardware_Setup-jetson--orin--spi--overlay--guide-blue)](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide/tree/main/examples/st7789)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

High-performance ST7789 display driver for Jetson Orin Nano with:
- Multiple wiring configurations (Jetson default, Waveshare, Adafruit)
- PIL/Pillow integration for easy image rendering
- Command-line tools and examples
- Comprehensive test suite

**Platform Support:** Jetson Orin Nano with JetPack 6.0+

## Prerequisites

**Hardware configuration required before software installation.**

This Python driver requires SPI and GPIO pins to be configured via device tree overlays. Install the appropriate overlay for your wiring:

**→ [Device Tree Overlay Installation Guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide/tree/main/examples/st7789)**

Available configurations:
- **Jetson Default** - Pins 29, 31 (standard Jetson Orin wiring)
- **Waveshare** - Pins 13, 22 (Waveshare 2inch LCD module)
- **Adafruit** - Pins 18, 22 (Adafruit ST7789 displays)

## Installation

After installing the device tree overlay:

```bash
git clone https://github.com/jetsonhacks/jetson-orin-st7789.git
cd jetson-orin-st7789

# Using uv (recommended)
uv sync

# Using pip
pip install -e .
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## Usage

```python
from jetson_orin_st7789 import ST7789

# Initialize with wiring preset matching your overlay
display = ST7789(wiring='jetson')  # or 'waveshare', 'adafruit'

# Fill screen with color
display.fill(0xFF0000)  # Red
display.show()

# Display an image
from PIL import Image
image = Image.open('photo.jpg')
display.display_image(image)
```

## Wiring Presets

Your Python wiring preset must match the device tree overlay you installed:

| Python Preset | Overlay Required | DC Pin | RST Pin |
|---------------|------------------|--------|---------|
| `'jetson'` | jetson-orin-st7789-default | 29 | 31 |
| `'waveshare'` | jetson-orin-st7789-waveshare | 13 | 22 |
| `'adafruit'` | jetson-orin-st7789-adafruit | 18 | 22 |

## Examples

```bash
# Basic colors demo
st7789-demo --wiring jetson

# With rotation
st7789-demo --wiring jetson --rotation 90

# Run test suite
st7789-test --wiring jetson

# Other examples
st7789-shapes
st7789-text
st7789-sysmon  # Requires: uv sync --extra examples
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Complete setup walkthrough
- **[Hardware Setup Guide](docs/HARDWARE_SETUP.md)** - Device tree overlay installation
- **[Wiring Guide](docs/WIRING_GUIDE.md)** - Pin configurations and diagrams
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Platform Support

**Tested on:**
- Jetson Orin Nano Developer Kit
- JetPack 6.0+
- Python 3.10+

**Note:** This driver is specifically designed for Jetson Orin platforms. Device tree overlays and pin configurations are Orin-specific and will not work on other Jetson platforms (Xavier, Nano, TX2) without modification.

## Development

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
pytest tests/ -v

# Format code
black src/ examples/ tests/

# Lint
ruff check src/ examples/ tests/
```

## Related Projects

- **[jetson-orin-spi-overlay-guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide)** - Device tree overlay guide for SPI devices on Jetson Orin (required for hardware setup)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues:** [GitHub Issues](https://github.com/jetsonhacks/jetson-orin-st7789/issues)
- **Hardware Setup:** [jetson-orin-spi-overlay-guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide)

## Acknowledgments

Created by JetsonHacks for the Jetson Orin community.

## December, 2025
* Initial Release
* Tested on NVIDIA Jetson Orin Nano Super Developer Kit
* JetPack 6.2.1
