#!/usr/bin/env python3
"""
Basic Colors Example
====================

Demonstrates basic usage of the ST7789 display driver by cycling through
primary and secondary colors.

Hardware Requirements:
    - Jetson board (Orin Nano, Xavier NX, etc.)
    - ST7789-based LCD display (e.g., Waveshare 2inch LCD Module)
    - Proper wiring (see README.md)

Usage:
    python3 basic_colors.py [--rotation ANGLE] [--wiring PRESET]
    
    --rotation: 0, 90, 180, or 270 (default: 0)
    --wiring: jetson, waveshare, or adafruit (default: jetson)

Examples:
    python3 basic_colors.py --rotation 90
    python3 basic_colors.py --wiring waveshare --rotation 180
    python3 basic_colors.py 90  # Legacy positional syntax
"""

import sys
import time
import argparse
from jetson_orin_st7789 import ST7789


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
        description='ST7789 Basic Colors Example',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Wiring Presets:
  jetson    : DC=29, RST=31 (BOARD numbering)
  waveshare : DC=25, RST=27 (BOARD numbering)
  adafruit  : DC=24, RST=25 (BOARD numbering)
  
Examples:
  %(prog)s --rotation 90
  %(prog)s --wiring waveshare --rotation 180
  %(prog)s 90  # Legacy positional syntax
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
    
    # Support legacy positional rotation argument
    parser.add_argument(
        'legacy_rotation',
        nargs='?',
        type=int,
        help=argparse.SUPPRESS
    )
    
    return parser.parse_args()


def main():
    """Display a sequence of solid colors."""
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        if args.legacy_rotation not in [0, 90, 180, 270]:
            print(f"Error: Invalid rotation {args.legacy_rotation}. Must be 0, 90, 180, or 270")
            sys.exit(1)
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    print(f"Initializing ST7789 display")
    print(f"  Wiring: {args.wiring} - {wiring['description']}")
    print(f"  Rotation: {args.rotation}°")
    
    # Initialize display with context manager (auto cleanup)
    with ST7789(
        spi_port=0,
        spi_cs=0,
        dc_pin=wiring['dc_pin'],
        rst_pin=wiring['rst_pin'],
        rotation=args.rotation,
        spi_speed_hz=125000000
    ) as display:
        
        print(f"Display ready: {display.width}x{display.height} pixels")
        print("Cycling through colors...")
        print("Press Ctrl+C to exit\n")
        
        # Define colors to cycle through
        colors = [
            ("Red",     (255, 0,   0)),
            ("Green",   (0,   255, 0)),
            ("Blue",    (0,   0,   255)),
            ("Cyan",    (0,   255, 255)),
            ("Magenta", (255, 0,   255)),
            ("Yellow",  (255, 255, 0)),
            ("White",   (255, 255, 255)),
            ("Black",   (0,   0,   0)),
        ]
        
        try:
            # Cycle through colors
            while True:
                for name, color in colors:
                    print(f"Displaying {name:8s} {color}")
                    display.fill(color)
                    time.sleep(2)
                    
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            print("Clearing display...")
            display.clear()


if __name__ == "__main__":
    main()
