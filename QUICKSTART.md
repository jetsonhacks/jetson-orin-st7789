# Quick Start Guide - jetson-orin-st7789

Get your ST7789 display driver up and running in 5 minutes!

## Prerequisites

- NVIDIA Jetson (Orin Nano, Xavier NX, Nano, etc.)
- ST7789-based LCD display (e.g., Waveshare 2inch LCD)
- Display connected to Jetson 40-pin header
- JetPack/Ubuntu installed on Jetson
- `uv` package manager installed

## Step 0: Install uv (if needed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 1: Copy Files (2 minutes)

```bash
# Navigate to your jetson-orin-st7789 directory
cd jetson-orin-st7789

# Copy the driver (you have this from the artifact)
cp /path/to/driver.py src/jetson_orin_st7789/driver.py

# Copy the examples
cp st7789_unit_tests.py examples/unit_tests.py
cp basic_colors_demo.py examples/basic_colors.py
cp examples__init__.py examples/__init__.py
```

## Step 2: Install Package (1 minute)

```bash
# Install with all dependencies (creates venv automatically!)
uv sync --extra dev

# Verify installation (no need to activate venv!)
uv run python -c "from jetson_orin_st7789 import ST7789; print('✓ Success!')"
```

## Step 3: Run Your First Demo (30 seconds)

```bash
# Portrait mode (0°)
uv run st7789-demo

# Landscape mode (90°)  
uv run st7789-demo 90
```

You should see colors cycling on your display! 🎨

## Step 4: Run Full Test Suite (2 minutes)

```bash
# Portrait mode
uv run st7789-test

# Landscape mode
uv run st7789-test 90

# All 4 orientations
uv run st7789-test 0
uv run st7789-test 90
uv run st7789-test 180
uv run st7789-test 270
```

## That's It! 🎉

Your display driver is now installed and tested. 

## Modern uv Workflow

With `uv`, you don't need to manually activate virtual environments:

```bash
# Add a new dependency
uv add pillow

# Add a dev dependency
uv add --dev pytest

# Run any script
uv run python examples/basic_colors.py

# Run tests
uv run pytest

# Format code
uv run black src/

# Lint code
uv run ruff check src/
```

## Traditional Workflow (if you prefer)

If you want to activate the venv manually:

```bash
source .venv/bin/activate
st7789-demo
st7789-test
```

## Common Issues & Solutions

### "Package not found"
```bash
# Make sure you're in the right directory
cd jetson-orin-st7789
uv sync --extra dev
```

### "Jetson.GPIO not found"
```bash
# Install system-wide (required for GPIO access)
sudo pip3 install Jetson.GPIO
```

### "No such device /dev/spidev0.0"
Your device tree needs SPI enabled. Check the documentation.

### "Permission denied"
```bash
# Add your user to required groups
sudo usermod -a -G gpio,spi $USER
# Logout and login again
```

### "uv not found"
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal or run:
source $HOME/.cargo/env
```

## Next Steps

### Create Your Own Scripts

```python
from jetson_orin_st7789 import ST7789
from PIL import Image, ImageDraw

# Initialize display
with ST7789(dc_pin=29, rst_pin=31) as display:
    # Fill screen
    display.fill((255, 0, 0))
    
    # Draw something
    img = Image.new('RGB', (240, 320), (0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Hello World!", fill=(255, 255, 255))
    display.display(img)
    
    input("Press Enter to exit...")
```

Save as `my_display.py` and run:
```bash
uv run python my_display.py
```

### Explore Examples

Check the `examples/` directory for more demos:
- `basic_colors.py` - Simple color cycling
- `unit_tests.py` - Comprehensive test suite

Run them with:
```bash
uv run python examples/basic_colors.py
uv run python examples/unit_tests.py 90
```

### Customize Pins

If your display uses different pins:

```python
display = ST7789(
    spi_port=0,        # SPI port
    spi_cs=0,          # Chip select
    dc_pin=29,         # Data/Command pin (BOARD mode)
    rst_pin=31,        # Reset pin (BOARD mode)
    width=240,         # Display width
    height=320,        # Display height
    rotation=0,        # 0, 90, 180, or 270
    spi_speed_hz=125000000  # 125 MHz
)
```

### Performance Tips

1. **Use `fill()` for solid colors** - Faster than creating an image
2. **Batch updates** - Update once per frame, not per pixel
3. **Use RGB565** - Native format, no conversion needed
4. **High SPI speed** - 125 MHz is optimal on Jetson Orin Nano

## Hardware Setup Reminder

Default pinout for this library:

| Display | Jetson Pin | Signal | Notes |
|---------|------------|--------|-------|
| VCC     | 1 or 17    | 3.3V   | Power |
| GND     | 6, 9, etc  | Ground | |
| DIN     | 19         | MOSI   | Data |
| CLK     | 23         | SCK    | Clock |
| CS      | 24         | CS0    | Chip Select |
| DC      | 29         | GPIO   | Data/Command |
| RST     | 31         | GPIO   | Reset |
| BL      | 1 or 17    | 3.3V   | Backlight |

## Getting Help

1. Check the [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) for detailed steps
2. Read [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) to understand the code
3. Review the main [README.md](README.md) for comprehensive documentation
4. Open an issue on GitHub if you're still stuck

## uv Cheat Sheet

```bash
# Setup and installation
uv sync                    # Install dependencies
uv sync --extra dev        # Install with dev dependencies
uv sync --all-extras       # Install all extras

# Running commands
uv run <command>           # Run command in venv (no activation needed)
uv run python script.py    # Run Python script
uv run st7789-test         # Run entry point

# Managing dependencies
uv add <package>           # Add runtime dependency
uv add --dev <package>     # Add dev dependency
uv remove <package>        # Remove dependency
uv lock                    # Update lockfile

# Traditional venv activation (optional)
source .venv/bin/activate  # Activate venv manually
```

## Time Investment

- **Initial setup**: 5 minutes
- **First successful display**: 10 seconds after setup
- **Learning the API**: 15 minutes
- **Creating custom displays**: 30+ minutes (the fun part!)

## Success Checklist

- [ ] `uv` installed
- [ ] Package installed with `uv sync --extra dev`
- [ ] Basic demo runs and displays colors
- [ ] Unit tests pass
- [ ] Display responds to rotation changes
- [ ] Can create custom displays
- [ ] Ready to build something cool! 🚀

---

**You're all set!** Start building amazing display projects with your Jetson.

Happy coding! 💻🎨