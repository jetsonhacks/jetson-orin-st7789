# Quick Start Guide - jetson-orin-st7789

Get your ST7789 display driver up and running on Jetson Orin Nano!

## Prerequisites

- **NVIDIA Jetson Orin Nano Developer Kit**
- ST7789-based LCD display (Waveshare 2inch LCD, Adafruit ST7789, or similar)
- Display connected to Jetson 40-pin header
- JetPack 6.0+ installed
- `uv` package manager installed (recommended)

**Note:** This driver is specifically tested on Jetson Orin Nano. Other Jetson platforms (Xavier, Nano, TX2) have different device tree configurations and would require different overlays.

## Step 0: Hardware Configuration (Required First!)

**Before installing the Python driver, you MUST install a device tree overlay.**

### Quick Overlay Installation

```bash
# Clone the overlay guide repository
git clone https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide.git
cd jetson-orin-spi-overlay-guide/examples/st7789

# Choose your configuration:
# - jetson-default/  (pins 29, 31) - Standard Jetson Orin wiring
# - waveshare/       (pins 13, 22) - Waveshare 2inch LCD module  
# - adafruit/        (pins 18, 22) - Adafruit ST7789 displays

# Example: Install Waveshare overlay
cd jetson-default
sudo ./install.sh

# Reboot to apply
sudo reboot
```

### Verify Overlay Installation

After reboot:

```bash
# Check SPI device exists
ls -l /dev/spidev1.0
# Should show: crw-rw---- 1 root gpio ...

# Verify pins configured (example for Waveshare pins 13, 22)
sudo gpioinfo | grep -E "spi3_sck|spi3_miso"
```

### Add User to GPIO Group

This allows running examples without sudo:

```bash
# Add your user to gpio and dialout groups
sudo usermod -a -G gpio,dialout $USER

# Log out and log back in for changes to take effect
# Or reboot
sudo reboot
```

See the [Hardware Setup Guide](docs/HARDWARE_SETUP.md) for detailed instructions.

## Step 1: Install uv (if needed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal

```

## Step 2: Clone and Install Package

```bash
# Clone the repository
git clone https://github.com/jetsonhacks/jetson-orin-st7789.git
cd jetson-orin-st7789

# Install with dependencies
uv sync

# Or with examples dependencies (system monitor)
uv sync --extra examples

# Verify installation
uv run python -c "from jetson_orin_st7789 import ST7789; print('✓ Success!')"
```

## Step 3: Run Your First Demo (No sudo needed!)

```bash
# Basic colors demo - use the preset matching your overlay!
# If you installed jetson-default overlay:
uv run python -m jetson_orin_st7789.examples.basic_colors --wiring jetson

# If you installed waveshare overlay:
uv run python -m jetson_orin_st7789.examples.basic_colors --wiring waveshare

# If you installed adafruit overlay:
uv run python -m jetson_orin_st7789.examples.basic_colors --wiring adafruit

# With rotation
uv run python -m jetson_orin_st7789.examples.basic_colors --wiring jetson --rotation 90
```

You should see colors cycling on your display.

## Step 4: Run Full Test Suite

```bash
# Test suite with your wiring preset
uv run python -m jetson_orin_st7789.examples.unit_tests --wiring jetson

# Test different rotations
uv run python -m jetson_orin_st7789.examples.unit_tests --wiring jetson --rotation 90
uv run python -m jetson_orin_st7789.examples.unit_tests --wiring jetson --rotation 180
uv run python -m jetson_orin_st7789.examples.unit_tests --wiring jetson --rotation 270
```

## That's It!

Your display driver is now installed and tested.

## Wiring Preset Reference

**IMPORTANT:** Your Python wiring preset must match the overlay you installed!

| Overlay Installed | Python Preset | DC Pin | RST Pin |
|-------------------|---------------|--------|---------|
| jetson-orin-st7789-default | `wiring='jetson'` | 29 | 31 |
| jetson-orin-st7789-waveshare | `wiring='waveshare'` | 13 | 22 |
| jetson-orin-st7789-adafruit | `wiring='adafruit'` | 18 | 22 |

## Modern uv Workflow

With `uv`, you don't need to manually activate virtual environments:

```bash
# Run any example script
uv run python examples/basic_colors_demo.py

# Run with arguments
uv run python examples/basic_colors_demo.py --wiring jetson --rotation 90

# Or use module syntax
uv run python -m jetson_orin_st7789.examples.basic_colors --wiring jetson
uv run python -m jetson_orin_st7789.examples.shapes_demo --wiring jetson
uv run python -m jetson_orin_st7789.examples.text_demo --wiring jetson
uv run python -m jetson_orin_st7789.examples.system_monitor --wiring jetson  # Requires: uv sync --extra examples
```

## Traditional Workflow (if you prefer)

If you want to activate the venv manually:

```bash
source .venv/bin/activate
python -m jetson_orin_st7789.examples.basic_colors --wiring jetson
python -m jetson_orin_st7789.examples.unit_tests --wiring jetson
```

## Create Your Own Scripts

```python
from jetson_orin_st7789 import ST7789
from PIL import Image, ImageDraw

# Initialize display - use your wiring preset!
display = ST7789(wiring='jetson')  # or 'waveshare', 'adafruit'

# Fill screen with red
display.fill(0xFF0000)
display.show()

# Draw something
img = Image.new('RGB', (display.width, display.height), (0, 0, 255))
draw = ImageDraw.Draw(img)
draw.text((10, 10), "Hello Orin!", fill=(255, 255, 255))
display.display_image(img)

input("Press Enter to exit...")
```

Save as `my_display.py` and run:
```bash
uv run python my_display.py
```

## Common Issues & Solutions

### Display Not Working

1. **Verify overlay is installed:**
   ```bash
   ls /boot/*.dtbo | grep st7789
   # Should show: jetson-orin-st7789-*.dtbo
   ```

2. **Check wiring preset matches overlay:**
   - Installed `jetson-default` overlay? → Use `wiring='jetson'`
   - Installed `waveshare` overlay? → Use `wiring='waveshare'`
   - Installed `adafruit` overlay? → Use `wiring='adafruit'`

3. **Verify SPI device:**
   ```bash
   ls /dev/spidev1.0
   # Should exist
   ```

### "Package not found"
```bash
# Make sure you're in the right directory
cd jetson-orin-st7789
uv sync
```

### "Jetson.GPIO not found"
```bash
# Should be installed automatically, but if needed:
uv add Jetson.GPIO
```

### "Permission denied" on GPIO/SPI
```bash
# Add your user to required groups
sudo usermod -a -G gpio,dialout $USER
# Log out and log back in (or reboot)
```

If you already added yourself to groups but still see permission errors, verify:
```bash
# Check group membership
groups
# Should include: gpio dialout
```

### "No such device /dev/spidev1.0"
Your device tree overlay is not installed or not loaded. See Step 0 above and the [Hardware Setup Guide](docs/HARDWARE_SETUP.md).

## Hardware Pinout

All configurations use the same SPI pins, only DC and RST differ:

**Common SPI Pins (All Configurations):**
| Signal | Jetson Pin | Notes |
|--------|------------|-------|
| 3.3V   | Pin 17     | Power |
| GND    | Pin 25     | Ground |
| MOSI   | Pin 19     | SPI1_MOSI |
| MISO   | Pin 21     | SPI1_MISO |
| SCK    | Pin 23     | SPI1_SCK |
| CS     | Pin 24     | SPI1_CS0 |

**Variable Pins (Depends on Configuration):**
| Configuration | DC Pin | RST Pin |
|---------------|--------|---------|
| Jetson Default | Pin 29 | Pin 31 |
| Waveshare | Pin 13 | Pin 22 |
| Adafruit | Pin 18 | Pin 22 |

## Explore Examples

```bash
# Basic colors cycling
uv run python -m jetson_orin_st7789.examples.basic_colors --wiring jetson

# Geometric shapes
uv run python -m jetson_orin_st7789.examples.shapes_demo --wiring jetson --rotation 90

# Text rendering
uv run python -m jetson_orin_st7789.examples.text_demo --wiring jetson

# System monitor (CPU, RAM, disk)
uv sync --extra examples  # Install psutil
uv run python -m jetson_orin_st7789.examples.system_monitor --wiring jetson
```

## Performance Tips

1. **Use `fill()` for solid colors** - Much faster than creating images
2. **Batch updates** - Update once per frame, not per pixel
3. **Use RGB565 format** - Native display format
4. **High SPI speed** - Default 80 MHz is optimal for Orin Nano

## Getting Help

1. Check the main [README.md](README.md) for comprehensive documentation
2. Review [Hardware Setup Guide](docs/HARDWARE_SETUP.md) for overlay installation
3. See [Wiring Guide](docs/WIRING_GUIDE.md) for pin configurations
4. Visit the [overlay guide](https://github.com/jetsonhacks/jetson-orin-spi-overlay-guide) for device tree help
5. Open an issue on GitHub if you're stuck

## uv Quick Reference

```bash
# Installation
uv sync                    # Install dependencies
uv sync --extra examples   # Install with examples extras
uv sync --all-extras       # Install everything

# Running
uv run <command>           # Run in venv (no activation needed)
uv run python script.py    # Run Python script
uv run st7789-test         # Run entry point

# Dependencies
uv add <package>           # Add dependency
uv add --dev <package>     # Add dev dependency
uv lock                    # Update lockfile
```

## Success Checklist

- [ ] Jetson Orin Nano with JetPack 6.0+
- [ ] Device tree overlay installed (Step 0)
- [ ] User added to gpio and dialout groups
- [ ] Logged out and back in (or rebooted)
- [ ] SPI device `/dev/spidev1.0` exists
- [ ] Python package installed with `uv sync`
- [ ] Demo runs with correct wiring preset (no sudo needed)
- [ ] Tests pass
- [ ] Ready to build!

---

**You're all set!** Start building display projects with your Jetson Orin Nano.

For detailed documentation, see [README.md](README.md).

Happy coding!
