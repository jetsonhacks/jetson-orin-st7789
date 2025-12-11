# Hardware Setup Guide

This guide covers the complete hardware setup process for ST7789 displays on Jetson Orin.

## Overview

Setting up the ST7789 display requires two steps:
1. **Hardware Configuration** - Install device tree overlay (one-time setup)
2. **Software Installation** - Install this Python package

## Step 1: Install Device Tree Overlay

Complete hardware setup instructions are in the overlay repository:

**→ [jetson-orin-spi-overlay-guide: ST7789 Examples](https://github.com/yourusername/jetson-orin-spi-overlay-guide/tree/main/examples/st7789)**

The overlay repository provides:
- Automated installation scripts with FDT auto-detection
- Three wiring configurations (Jetson default, Waveshare, Adafruit)
- Pin verification tools
- Detailed troubleshooting guides

### Choose Your Configuration

| Configuration | DC Pin | RST Pin | Use Case |
|--------------|--------|---------|----------|
| Jetson Default | 29 | 31 | Standard Jetson Orin wiring |
| Waveshare | 13 | 22 | Waveshare 2inch LCD module |
| Adafruit | 18 | 22 | Adafruit ST7789 displays |

### Installation Example (Waveshare)

```bash
# Clone the overlay guide
git clone https://github.com/yourusername/jetson-orin-spi-overlay-guide.git
cd jetson-orin-spi-overlay-guide/examples/st7789/waveshare

# Run installation script (auto-detects FDT)
sudo ./install.sh

# Reboot to apply changes
sudo reboot
```

## Step 2: Verify Hardware Configuration

After reboot:

```bash
# Check SPI device exists
ls -l /dev/spidev1.0
# Should show: crw-rw---- 1 root gpio ... /dev/spidev1.0

# Verify GPIO pins (example for Waveshare pins 13, 22)
sudo gpioinfo | grep -E "spi3_sck|spi3_miso"
# Pins should show as GPIO-capable

# Optional: Use pin inspector tool
cd jetson-orin-spi-overlay-guide/tools
sudo python3 pin_inspector.py 13
sudo python3 pin_inspector.py 22
# Both should show: "✓ Pin is configured as GPIO and ready to use!"
```

## Step 3: Install Python Package

Return to this repository's [README.md](../README.md#installation) for Python package installation.

## Troubleshooting

### SPI Device Not Found

```bash
ls /dev/spidev*
# If empty, overlay not loaded correctly
```

**Solutions:**
1. Check `/boot/extlinux/extlinux.conf` has overlay line
2. Verify overlay file exists: `ls /boot/*.dtbo`
3. Check for typos in overlay name
4. Review dmesg for errors: `dmesg | grep -i overlay`

### GPIO Pins Not Configured

If `gpioinfo` shows pins as "unused" or in wrong function:

**Solutions:**
1. Verify correct overlay installed (match your wiring)
2. Check overlay compiled without errors
3. Ensure reboot after overlay installation

### Display Not Working

Hardware verification passed but display doesn't work:

**Solutions:**
1. Verify wiring matches overlay configuration
2. Check SPI connections (MOSI, MISO, SCK, CS)
3. Verify power supply (3.3V, sufficient current)
4. Test with known-good display
5. Check Python package wiring preset matches overlay

## Additional Resources

- [Overlay Guide Troubleshooting](https://github.com/yourusername/jetson-orin-spi-overlay-guide#troubleshooting)
- [Device Tree Basics](https://github.com/yourusername/jetson-orin-spi-overlay-guide/blob/main/docs/DEVICE_TREE_BASICS.md)
- [FDT Configuration](https://github.com/yourusername/jetson-orin-spi-overlay-guide/blob/main/docs/FDT_CONFIGURATION.md)

## Wiring Diagrams

See [WIRING_GUIDE.md](WIRING_GUIDE.md) for detailed pin diagrams and photos.
