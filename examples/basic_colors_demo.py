#!/usr/bin/env python3
"""
ST7789 Basic Colors Demo
Simple demonstration of color fills using the jetson_orin_st7789 package
"""

import sys
import time
import argparse

try:
    from jetson_orin_st7789 import ST7789
except ImportError:
    print("Error: jetson_orin_st7789 package not found.")
    print("Please install with: uv pip install -e .")
    sys.exit(1)


# Wiring presets for different hardware configurations
WIRING_PRESETS = {
    'jetson': {
        'dc_pin': 29,
        'rst_pin': 31,
        'description': 'Jetson default wiring (BOARD numbering)'
    },
    'waveshare': {
        'dc_pin': 25,
        'rst_pin': 27,
        'description': 'Waveshare 2inch LCD Module default wiring'
    },
    'adafruit': {
        'dc_pin': 24,
        'rst_pin': 25,
        'description': 'Adafruit ST7789 breakout default wiring'
    }
}


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='ST7789 Basic Colors Demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Wiring Presets:
  jetson    : DC=29, RST=31 (BOARD numbering)
  waveshare : DC=25, RST=27 (BOARD numbering)
  adafruit  : DC=24, RST=25 (BOARD numbering)
  
Examples:
  %(prog)s --rotation 90
  %(prog)s --wiring waveshare --rotation 180
  %(prog)s --wiring adafruit
'''
    )
    
    parser.add_argument(
        '--rotation',
        type=int,
        choices=[0, 90, 180, 270],
        default=0,
        help='Display rotation in degrees (default: 0)'
    )
    
    parser.add_argument(
        '--wiring',
        type=str,
        choices=list(WIRING_PRESETS.keys()),
        default='jetson',
        help='Wiring preset to use (default: jetson)'
    )
    
    # Support legacy positional rotation argument for backwards compatibility
    parser.add_argument(
        'legacy_rotation',
        nargs='?',
        type=int,
        help=argparse.SUPPRESS
    )
    
    return parser.parse_args()


def main():
    """Main entry point for basic colors demo"""
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        if args.legacy_rotation not in [0, 90, 180, 270]:
            print(f"Invalid rotation: {args.legacy_rotation}. Must be 0, 90, 180, or 270")
            sys.exit(1)
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    print("ST7789 Basic Colors Demo")
    print("="*60)
    print(f"Wiring preset: {args.wiring} - {wiring['description']}")
    print(f"  DC Pin:  {wiring['dc_pin']} (BOARD)")
    print(f"  RST Pin: {wiring['rst_pin']} (BOARD)")
    print(f"Rotation: {args.rotation}°")
    print("="*60)
    
    # Initialize display
    try:
        display = ST7789(
            spi_port=0,
            spi_cs=0,
            dc_pin=wiring['dc_pin'],
            rst_pin=wiring['rst_pin'],
            width=240,
            height=320,
            rotation=args.rotation,
            spi_speed_hz=125000000
        )
    except Exception as e:
        print(f"Error initializing display: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Jetson.GPIO is installed: sudo pip3 install Jetson.GPIO")
        print("2. Ensure spidev is installed: pip3 install spidev")
        print("3. Check hardware connections match the selected wiring preset")
        print("4. Verify SPI is enabled in device tree")
        sys.exit(1)
    
    print(f"Display initialized: {display}")
    print("\nCycling through colors. Press Ctrl+C to exit.\n")
    
    # Define colors to cycle through
    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("Yellow", (255, 255, 0)),
        ("Cyan", (0, 255, 255)),
        ("Magenta", (255, 0, 255)),
        ("White", (255, 255, 255)),
        ("Black", (0, 0, 0)),
        ("Orange", (255, 165, 0)),
        ("Purple", (128, 0, 128)),
        ("Pink", (255, 192, 203)),
        ("Lime", (0, 255, 0)),
    ]
    
    try:
        # Cycle through colors
        while True:
            for name, color in colors:
                print(f"Displaying {name:12} {color}")
                display.fill(color)
                time.sleep(1.5)
                
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    finally:
        print("Cleaning up...")
        display.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()
