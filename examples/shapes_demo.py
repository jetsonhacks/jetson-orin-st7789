#!/usr/bin/env python3
"""
ST7789 Shapes Demo
Demonstrates drawing various geometric shapes and patterns
"""

import sys
import time
import argparse
from PIL import Image, ImageDraw

try:
    from jetson_orin_st7789 import ST7789
except ImportError:
    print("Error: jetson_orin_st7789 package not found.")
    print("Please install with: uv sync --extra dev")
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
        description='ST7789 Shapes Demo',
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
    
    # Support legacy positional rotation argument
    parser.add_argument(
        'legacy_rotation',
        nargs='?',
        type=int,
        help=argparse.SUPPRESS
    )
    
    return parser.parse_args()


def draw_rectangles(draw, width, height):
    """Draw various rectangles"""
    # Outline rectangles
    draw.rectangle([10, 10, 80, 60], outline=(255, 0, 0), width=2)
    draw.rectangle([90, 10, 160, 60], outline=(0, 255, 0), width=3)
    draw.rectangle([170, 10, 230, 60], outline=(0, 0, 255), width=4)
    
    # Filled rectangles
    draw.rectangle([10, 70, 80, 120], fill=(255, 100, 0))
    draw.rectangle([90, 70, 160, 120], fill=(255, 0, 255))
    draw.rectangle([170, 70, 230, 120], fill=(0, 255, 255))
    
    # Rounded rectangles (if PIL version supports it)
    try:
        draw.rounded_rectangle([10, 130, 110, 190], radius=15, 
                              fill=(100, 100, 255), outline=(255, 255, 255), width=2)
        draw.rounded_rectangle([130, 130, 230, 190], radius=20,
                              fill=(255, 100, 100), outline=(255, 255, 0), width=3)
    except AttributeError:
        # Fallback for older PIL versions
        draw.rectangle([10, 130, 110, 190], fill=(100, 100, 255), outline=(255, 255, 255))
        draw.rectangle([130, 130, 230, 190], fill=(255, 100, 100), outline=(255, 255, 0))


def draw_circles(draw, width, height):
    """Draw various circles and ellipses"""
    # Outline circles
    draw.ellipse([10, 10, 70, 70], outline=(255, 0, 0), width=2)
    draw.ellipse([80, 10, 140, 70], outline=(0, 255, 0), width=3)
    draw.ellipse([150, 10, 210, 70], outline=(0, 0, 255), width=4)
    
    # Filled circles
    draw.ellipse([20, 80, 60, 120], fill=(255, 100, 0))
    draw.ellipse([90, 80, 130, 120], fill=(255, 0, 255))
    draw.ellipse([160, 80, 200, 120], fill=(0, 255, 255))
    
    # Ellipses (stretched circles)
    draw.ellipse([10, 130, 110, 180], outline=(255, 255, 0), width=2)
    draw.ellipse([120, 130, 230, 160], outline=(0, 255, 255), width=2)
    
    # Filled ellipses
    draw.ellipse([60, 190, 120, 260], fill=(255, 192, 203))
    draw.ellipse([140, 200, 200, 250], fill=(173, 216, 230))


def draw_lines(draw, width, height):
    """Draw various lines"""
    # Horizontal lines with different widths
    for i, w in enumerate([1, 2, 3, 4, 5]):
        y = 20 + i * 15
        draw.line([10, y, 230, y], fill=(255, 255, 255), width=w)
    
    # Vertical lines
    for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                               (255, 255, 0), (255, 0, 255)]):
        x = 30 + i * 40
        draw.line([x, 100, x, 200], fill=color, width=3)
    
    # Diagonal lines
    draw.line([10, 210, 230, 310], fill=(255, 100, 0), width=3)
    draw.line([10, 310, 230, 210], fill=(0, 255, 100), width=3)
    
    # Connected lines (polyline)
    points = [(120, 230), (150, 250), (120, 270), (90, 250)]
    for i in range(len(points)):
        start = points[i]
        end = points[(i + 1) % len(points)]
        draw.line([start, end], fill=(255, 255, 0), width=4)


def draw_polygons(draw, width, height):
    """Draw various polygons"""
    # Triangle
    triangle = [(120, 30), (60, 120), (180, 120)]
    draw.polygon(triangle, outline=(255, 0, 0), width=3)
    
    # Filled triangle
    triangle2 = [(120, 140), (70, 220), (170, 220)]
    draw.polygon(triangle2, fill=(0, 255, 0))
    
    # Pentagon
    import math
    center_x, center_y = 120, 270
    radius = 40
    pentagon = []
    for i in range(5):
        angle = (2 * math.pi * i / 5) - (math.pi / 2)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        pentagon.append((x, y))
    draw.polygon(pentagon, outline=(255, 255, 0), width=2)
    
    # Star
    star = []
    for i in range(10):
        angle = (2 * math.pi * i / 10) - (math.pi / 2)
        r = 30 if i % 2 == 0 else 15
        x = center_x + r * math.cos(angle)
        y = center_y + 80 + r * math.sin(angle)
        star.append((x, y))
    draw.polygon(star, fill=(255, 215, 0))


def draw_arcs(draw, width, height):
    """Draw arcs and pie slices"""
    # Arc (part of circle outline)
    draw.arc([20, 20, 100, 100], start=0, end=180, fill=(255, 0, 0), width=4)
    draw.arc([120, 20, 200, 100], start=180, end=360, fill=(0, 255, 0), width=4)
    
    # Pie slices (filled)
    draw.pieslice([30, 120, 110, 200], start=0, end=90, fill=(255, 100, 0))
    draw.pieslice([130, 120, 210, 200], start=90, end=270, fill=(255, 0, 255))
    
    # Clock face with pie slices
    center = [120, 260]
    radius = 50
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    for i, color in enumerate(colors):
        start_angle = i * 90
        end_angle = (i + 1) * 90
        bbox = [center[0] - radius, center[1] - radius,
                center[0] + radius, center[1] + radius]
        draw.pieslice(bbox, start=start_angle, end=end_angle, fill=color)


def draw_patterns(draw, width, height):
    """Draw interesting patterns"""
    # Checkerboard
    square_size = 20
    for y in range(0, 160, square_size):
        for x in range(0, width, square_size):
            if ((x // square_size) + (y // square_size)) % 2:
                draw.rectangle([x, y, x + square_size, y + square_size],
                             fill=(100, 100, 255))
    
    # Concentric circles
    center_x, center_y = width // 2, 230
    for i in range(6):
        radius = 10 + i * 10
        color_val = 255 - i * 40
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    outline=(color_val, 255 - color_val, 255), width=2)
    
    # Grid
    grid_y_start = 200
    grid_spacing = 15
    for i in range(8):
        y = grid_y_start + i * grid_spacing
        draw.line([0, y, width, y], fill=(50, 50, 50), width=1)
    for i in range(17):
        x = i * grid_spacing
        draw.line([x, grid_y_start, x, height], fill=(50, 50, 50), width=1)


def draw_gradients(draw, width, height):
    """Draw gradient effects"""
    # Horizontal gradient
    for x in range(width):
        color_val = int((x / width) * 255)
        draw.line([x, 0, x, 80], fill=(color_val, 0, 255 - color_val), width=1)
    
    # Vertical gradient
    for y in range(80, 160):
        color_val = int(((y - 80) / 80) * 255)
        draw.line([0, y, width, y], fill=(255 - color_val, color_val, 0), width=1)
    
    # Radial gradient (approximation)
    center_x, center_y = width // 2, 240
    max_radius = 80
    import math
    for r in range(max_radius, 0, -2):
        color_val = int((r / max_radius) * 255)
        draw.ellipse([center_x - r, center_y - r,
                     center_x + r, center_y + r],
                    fill=(color_val, 0, 255 - color_val))


def main():
    """Main entry point for shapes demo"""
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        if args.legacy_rotation not in [0, 90, 180, 270]:
            print(f"Invalid rotation: {args.legacy_rotation}. Must be 0, 90, 180, or 270")
            sys.exit(1)
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    print("ST7789 Shapes Demo")
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
        sys.exit(1)
    
    print(f"Display initialized: {display}")
    print("\nCycling through shape demos. Press Ctrl+C to exit.\n")
    
    # Define demos
    demos = [
        ("Rectangles", draw_rectangles),
        ("Circles & Ellipses", draw_circles),
        ("Lines", draw_lines),
        ("Polygons", draw_polygons),
        ("Arcs & Pie Slices", draw_arcs),
        ("Patterns", draw_patterns),
        ("Gradients", draw_gradients),
    ]
    
    try:
        # Cycle through demos
        while True:
            for name, draw_func in demos:
                print(f"Displaying: {name}")
                
                # Create canvas
                image = Image.new('RGB', (display.width, display.height), (0, 0, 0))
                draw = ImageDraw.Draw(image)
                
                # Draw the demo
                draw_func(draw, display.width, display.height)
                
                # Add title
                title_bg = Image.new('RGB', (display.width, 20), (50, 50, 50))
                title_draw = ImageDraw.Draw(title_bg)
                title_draw.text((5, 3), name, fill=(255, 255, 255))
                image.paste(title_bg, (0, 0))
                
                # Display
                display.display(image)
                time.sleep(3)
                
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    finally:
        print("Cleaning up...")
        display.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()
