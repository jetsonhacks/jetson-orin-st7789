# jetson-orin-st7789

Python driver for ST7789 LCD displays on NVIDIA Jetson Orin platforms.

[![Hardware Setup](https://img.shields.io/badge/Hardware_Setup-jetson--orin--spi--overlay--guide-blue)](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide/tree/main/examples/st7789)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Prerequisites

**Hardware Setup Required First!**

Before using this Python package, you must configure your Jetson Orin's device tree for SPI and GPIO.

**→ Install Device Tree Overlay:** [jetson-orin-spi-overlay-guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide/tree/main/examples/st7789)

Choose the overlay matching your hardware wiring:
- **Jetson Default** (pins 29, 31) - Standard configuration
- **Waveshare** (pins 13, 22) - Waveshare 2inch LCD module
- **Adafruit** (pins 18, 22) - Adafruit ST7789 displays

The overlay repository provides automated installation scripts with FDT auto-detection, pin verification tools, and comprehensive troubleshooting guides.

## Installation

After overlay installation:

```bash
git clone https://github.com/jetsonhacks/jetson-orin-st7789.git
cd jetson-orin-st7789

# Using uv (recommended)
uv sync

# Or with examples dependencies (system monitor, etc.)
uv sync --extra examples

# Or with all extras (dev tools, docs, examples)
uv sync --all-extras
```

### Alternative: Using pip

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install package
pip install -e .

# Or with extras
pip install -e ".[examples]"
```

### Verify Installation

```bash
python -c "from jetson_orin_st7789 import ST7789; print('✓ Installation successful')"
```

## Quick Start

```python
from jetson_orin_st7789 import ST7789

# Use wiring preset matching your overlay
display = ST7789(wiring='waveshare')  # or 'jetson', 'adafruit'

# Fill screen with red
display.fill(0xFF0000)
display.show()

# Display an image
from PIL import Image
image = Image.open('photo.jpg')
display.display_image(image)
```

## Wiring Presets

Your Python wiring preset must match the device tree overlay you installed:

| Python Preset | DC Pin | RST Pin | Required Overlay | Use Case |
|---------------|--------|---------|------------------|----------|
| `'jetson'` | 29 | 31 | jetson-orin-st7789-default | Standard Jetson Orin wiring |
| `'waveshare'` | 13 | 22 | jetson-orin-st7789-waveshare | Waveshare 2inch LCD module |
| `'adafruit'` | 18 | 22 | jetson-orin-st7789-adafruit | Adafruit ST7789 displays |

All configurations use the same SPI pins (19, 21, 23, 24) - only DC and RST differ.

## Examples

The package includes several example programs:

```bash
# Basic colors demo (uses command-line entry point)
st7789-demo

# With rotation
st7789-demo --rotation 90

# With specific wiring preset
st7789-demo --wiring waveshare --rotation 90

# Run comprehensive test suite
st7789-test

# Other examples
st7789-shapes     # Geometric shapes
st7789-text       # Text rendering
st7789-sysmon     # System monitor (requires psutil)
```

### Running Examples Directly

```bash
# Run examples as Python modules
python -m examples.basic_colors_demo --wiring waveshare
python -m examples.shapes_demo --rotation 90
python -m examples.text_demo
```

## Advanced Usage

### Custom Pin Configuration

```python
from jetson_orin_st7789 import ST7789

# Specify pins manually
display = ST7789(
    dc_pin=13,      # Data/Command pin
    rst_pin=22,     # Reset pin
    spi_port=1,     # SPI bus number
    spi_cs=0,       # Chip select
    width=240,
    height=240,
    rotation=90,
    spi_speed_hz=80_000_000
)
```

### Using Presets Helper

```python
from jetson_orin_st7789 import from_preset

# Create display from preset (convenience function)
display = from_preset('waveshare', rotation=90, spi_speed_hz=60_000_000)

# List available presets
from jetson_orin_st7789 import list_presets
list_presets()

# Get preset details
from jetson_orin_st7789 import print_preset_info
print_preset_info('waveshare')
```

### Working with PIL/Pillow

```python
from jetson_orin_st7789 import ST7789
from PIL import Image, ImageDraw, ImageFont

display = ST7789(wiring='waveshare')

# Create image
image = Image.new('RGB', (display.width, display.height), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw shapes
draw.rectangle((10, 10, 100, 100), fill=(255, 0, 0))
draw.text((50, 120), "Hello Jetson!", fill=(255, 255, 255))

# Display
display.display_image(image)
```

## Documentation

- [Hardware Setup Guide](docs/HARDWARE_SETUP.md) - Complete hardware configuration walkthrough
- [Wiring Guide](docs/WIRING_GUIDE.md) - Pin configurations and diagrams
- [Pin Inspector Guide](docs/PIN_INSPECTOR_GUIDE.md) - Using the pin verification tool
- [Pinout Guide](docs/PINOUT_GUIDE.md) - Detailed pinout information

## Troubleshooting

### Display Not Working

1. **Verify overlay is installed:**
   ```bash
   ls /boot/*.dtbo | grep st7789
   # Should show: jetson-orin-st7789-*.dtbo
   ```

2. **Check SPI device exists:**
   ```bash
   ls -l /dev/spidev1.0
   # Should show: crw-rw---- 1 root gpio ... /dev/spidev1.0
   ```

3. **Verify GPIO pins configured:**
   ```bash
   sudo gpioinfo | grep -E "spi3_sck|spi3_miso"
   # Pins should show as GPIO-capable
   ```

4. **Ensure wiring preset matches overlay:**
   - If you installed `waveshare` overlay, use `wiring='waveshare'` in Python
   - Mismatched presets will cause the display not to work

5. **Check permissions:**
   ```bash
   # Add user to gpio and dialout groups
   sudo usermod -a -G gpio,dialout $USER
   # Log out and back in for changes to take effect
   ```

For more troubleshooting, see the [Hardware Setup Guide](docs/HARDWARE_SETUP.md) and [jetson-orin-spi-overlay-guide troubleshooting](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide#troubleshooting).

## Platform Support

**Tested on:**
- Jetson Orin Nano Developer Kit
- JetPack 6.0+
- Python 3.8+

**Note:** This package is specifically designed and tested for Jetson Orin platforms. Device tree overlays and pin configurations are Orin-specific. For other Jetson platforms (Xavier NX, Nano, TX2), different overlays and pin mappings would be required.

## Development

### Running Tests

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=jetson_orin_st7789
```

### Code Quality

```bash
# Format code
black src/ examples/ tests/

# Lint
ruff check src/ examples/ tests/

# Type checking
mypy src/
```

## Related Projects

- [jetson-orin-spi-overlay-guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide) - Device tree overlay guide for SPI devices on Jetson Orin (required for hardware setup)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Created by JetsonHacks for the Jetson Orin community.

Special thanks to:
- NVIDIA for the Jetson platform
- The open-source community for SPI and display driver examples
- Contributors and testers

## Support

- Issues: [GitHub Issues](https://github.com/jetsonhacks/jetson-orin-st7789/issues)
- Discussions: [GitHub Discussions](https://github.com/jetsonhacks/jetson-orin-st7789/discussions)
- Hardware Setup: [jetson-orin-spi-overlay-guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide)
