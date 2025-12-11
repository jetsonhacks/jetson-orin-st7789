#!/usr/bin/env python3
"""
Waveshare ST7789 Configuration Test
Tests the Waveshare pinout (pins 13 and 22) 

This script:
1. Checks GPIO pin configuration for pins 13 and 22
2. Tests SPI connectivity
3. Verifies display initialization with Waveshare pins
4. Runs basic display tests
5. Provides diagnostic information

Waveshare Pinout:
  DC  = Pin 22 (spi3_miso_py1)
  RST = Pin 13 (spi3_sck_py0)

Run with: sudo python3 test_waveshare_default.py
"""

import sys
import time
import os

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def print_header(msg):
    print(f"\n{'='*70}")
    print(f"  {msg}")
    print(f"{'='*70}\n")


def check_root():
    """Check if running as root"""
    if os.geteuid() != 0:
        print_error("This script must be run as root (use sudo)")
        print_info("Run: sudo python3 test_waveshare_default.py")
        return False
    print_success("Running as root")
    return True


def check_gpio_pins():
    """Check if pins 13 and 22 are configured as GPIO"""
    print_header("Checking GPIO Pin Configuration")
    
    pins_to_check = [13, 22]
    all_ok = True
    
    for pin in pins_to_check:
        print(f"\nChecking Pin {pin}...")
        
        # Run pin inspector if available
        if os.path.exists('tools/pin_inspector.py'):
            result = os.system(f"python3 tools/pin_inspector.py {pin} 2>/dev/null | grep 'Pin is'")
            if result == 0:
                print_success(f"Pin {pin} is properly configured")
            else:
                print_error(f"Pin {pin} may not be configured as GPIO")
                print_info(f"Run: sudo python3 tools/pin_inspector.py {pin}")
                print_warning("You may need to install device tree overlay for Waveshare pins")
                all_ok = False
        else:
            print_warning("Pin inspector tool not found, skipping detailed check")
            print_info("Continuing with basic test...")
    
    return all_ok


def check_spi():
    """Check if SPI is available"""
    print_header("Checking SPI Configuration")
    
    spi_devices = ['/dev/spidev0.0', '/dev/spidev0.1']
    found = False
    
    for device in spi_devices:
        if os.path.exists(device):
            print_success(f"Found {device}")
            found = True
        else:
            print_warning(f"{device} not found")
    
    if not found:
        print_error("No SPI devices found")
        print_info("SPI may not be enabled in device tree")
        return False
    
    return True


def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("Checking Python Dependencies")
    
    packages = [
        ('jetson_orin_st7789', 'ST7789 driver'),
        ('PIL', 'Pillow (PIL)'),
        ('numpy', 'NumPy'),
    ]
    
    all_ok = True
    for package, name in packages:
        try:
            __import__(package)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} not installed")
            all_ok = False
    
    # Special check for Jetson.GPIO
    try:
        import Jetson.GPIO as GPIO
        print_success("Jetson.GPIO installed")
    except ImportError:
        print_error("Jetson.GPIO not installed")
        print_info("Install with: sudo pip3 install Jetson.GPIO")
        all_ok = False
    
    return all_ok


def test_display_init():
    """Test display initialization with Waveshare pins"""
    print_header("Testing Display Initialization")
    
    try:
        from jetson_orin_st7789 import ST7789
        print_info("Importing ST7789 driver...")
        
        print_info("Initializing display with Waveshare pinout:")
        print_info("  DC  = Pin 22 (spi3_miso_py1)")
        print_info("  RST = Pin 13 (spi3_sck_py0)")
        
        display = ST7789(
            spi_port=0,
            spi_cs=0,
            dc_pin=22,      # Waveshare DC pin
            rst_pin=13,     # Waveshare RST pin
            width=240,
            height=320,
            rotation=0,
            spi_speed_hz=125000000
        )
        
        print_success("Display initialized successfully")
        print_info(f"Display: {display}")
        
        return display
        
    except Exception as e:
        print_error(f"Display initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_display_colors(display):
    """Test basic color display"""
    print_header("Testing Display Output")
    
    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("White", (255, 255, 255)),
        ("Black", (0, 0, 0)),
    ]
    
    try:
        for name, color in colors:
            print(f"  Displaying {name} {color}...", end='', flush=True)
            display.fill(color)
            time.sleep(0.5)
            print(" OK")
        
        print_success("All colors displayed successfully")
        return True
        
    except Exception as e:
        print_error(f"\nColor display failed: {e}")
        return False


def test_display_pattern(display):
    """Test pattern display"""
    print_header("Testing Pattern Display")
    
    try:
        from PIL import Image, ImageDraw
        
        print_info("Creating test pattern...")
        image = Image.new('RGB', (display.width, display.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw color bars
        bar_width = display.width // 4
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        for i, color in enumerate(colors):
            x0 = i * bar_width
            x1 = x0 + bar_width
            draw.rectangle([x0, 0, x1, display.height], fill=color)
        
        # Draw test text
        draw.text((10, 10), "Waveshare Test", fill=(255, 255, 0))
        draw.text((10, 30), "Pin 22: DC", fill=(255, 255, 0))
        draw.text((10, 50), "Pin 13: RST", fill=(255, 255, 0))
        
        print_info("Displaying pattern...")
        display.display(image)
        
        print_success("Pattern displayed successfully")
        return True
        
    except Exception as e:
        print_error(f"Pattern display failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_diagnostics():
    """Run full diagnostic suite"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║       Waveshare ST7789 Configuration Test                        ║
║                                                                  ║
║  Testing Waveshare 2inch LCD pinout on Jetson                   ║
║  Pins: DC=22, RST=13, SPI0, CS0                                 ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    # Step 1: Check root
    if not check_root():
        return False
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print_error("\nMissing dependencies. Install them first:")
        print_info("  uv sync --extra dev")
        print_info("  sudo pip3 install Jetson.GPIO")
        return False
    
    # Step 3: Check SPI
    if not check_spi():
        print_error("\nSPI not available")
        return False
    
    # Step 4: Check GPIO pins
    gpio_ok = check_gpio_pins()
    if not gpio_ok:
        print_error("\n❌ GPIO PINS NOT CONFIGURED")
        print_info("\nWaveshare pins 13 and 22 need device tree configuration!")
        print_info("\nTo configure:")
        print_info("  1. Run: sudo ./install_display_overlay.sh")
        print_info("  2. Select option 1 (Waveshare)")
        print_info("  3. Reboot")
        print_info("  4. Run this test again")
        print_info("\nAlternatively, check individual pins:")
        print_info("  sudo python3 tools/pin_inspector.py 13")
        print_info("  sudo python3 tools/pin_inspector.py 22")
        return False
    
    # Step 5: Test display initialization
    display = test_display_init()
    if not display:
        print_error("\n❌ DISPLAY INITIALIZATION FAILED")
        print_info("\nTroubleshooting steps:")
        print_info("  1. Check GPIO pins: sudo python3 tools/pin_inspector.py 13")
        print_info("  2. Check GPIO pins: sudo python3 tools/pin_inspector.py 22")
        print_info("  3. Verify physical connections")
        print_info("  4. Check device tree overlay is installed")
        return False
    
    # Step 6: Test colors
    if not test_display_colors(display):
        display.cleanup()
        return False
    
    # Step 7: Test pattern
    if not test_display_pattern(display):
        display.cleanup()
        return False
    
    # Success!
    print_header("Test Results")
    print_success("✓ All tests passed!")
    print_success("✓ Display is working correctly")
    print_success("✓ Waveshare pinout verified")
    
    print_info("\nDisplay showing test pattern. Press Enter to exit...")
    input()
    
    # Cleanup
    print_info("Cleaning up...")
    display.cleanup()
    print_success("Cleanup complete")
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    ✓ SUCCESS!                                    ║
║                                                                  ║
║  Waveshare pinout is working correctly.                          ║
║  You can now use: from_preset('waveshare')                       ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    return True


def main():
    """Main entry point"""
    try:
        success = run_diagnostics()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
