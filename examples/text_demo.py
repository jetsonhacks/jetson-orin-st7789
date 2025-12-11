#!/usr/bin/env python3
"""
ST7789 Text Demo
Demonstrates text rendering with various fonts, sizes, and styles
"""

import sys
import time
import argparse
from PIL import Image, ImageDraw, ImageFont

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
        description='ST7789 Text Demo',
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


def demo_basic_text(draw, width, height):
    """Basic text rendering with default font"""
    draw.text((10, 10), "Default Font", fill=(255, 255, 255))
    draw.text((10, 30), "Small text example", fill=(200, 200, 200))
    draw.text((10, 50), "Line 1", fill=(255, 100, 100))
    draw.text((10, 65), "Line 2", fill=(100, 255, 100))
    draw.text((10, 80), "Line 3", fill=(100, 100, 255))
    
    # Colored text
    colors = [
        (255, 0, 0), (255, 128, 0), (255, 255, 0),
        (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)
    ]
    for i, color in enumerate(colors):
        draw.text((10, 110 + i * 15), f"Color {i+1}", fill=color)


def demo_multiline_text(draw, width, height):
    """Multiline text rendering"""
    text = """Multiline Text Demo
    
This is a longer piece of text
that spans multiple lines.

You can use \\n for line breaks
and format text in paragraphs.

Great for displaying messages,
instructions, or data."""
    
    draw.multiline_text((10, 10), text, fill=(255, 255, 255), spacing=4)


def demo_text_positioning(draw, width, height):
    """Text positioning and alignment"""
    # Top-left (default)
    draw.text((10, 10), "Top Left", fill=(255, 255, 255))
    
    # Top-right
    text = "Top Right"
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    draw.text((width - text_width - 10, 10), text, fill=(255, 255, 0))
    
    # Center
    text = "Centered Text"
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, height // 2 - 10), 
              text, fill=(0, 255, 255))
    
    # Bottom-left
    draw.text((10, height - 30), "Bottom Left", fill=(255, 0, 255))
    
    # Bottom-right
    text = "Bottom Right"
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    draw.text((width - text_width - 10, height - 30), 
              text, fill=(0, 255, 0))


def demo_text_with_background(draw, width, height):
    """Text with background boxes"""
    messages = [
        ("INFO", (100, 100, 255)),
        ("SUCCESS", (0, 255, 0)),
        ("WARNING", (255, 200, 0)),
        ("ERROR", (255, 0, 0)),
    ]
    
    y_pos = 20
    for label, color in messages:
        text = f"  {label}  "
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw background
        draw.rectangle([10, y_pos, 10 + text_width + 10, y_pos + text_height + 10],
                      fill=color)
        
        # Draw text
        draw.text((15, y_pos + 5), text, fill=(0, 0, 0))
        
        y_pos += text_height + 25


def demo_data_display(draw, width, height):
    """Display formatted data (like a dashboard)"""
    # Title
    draw.rectangle([0, 0, width, 30], fill=(50, 50, 50))
    draw.text((10, 8), "System Monitor", fill=(255, 255, 255))
    
    # Data fields
    data = [
        ("CPU Temp:", "45.2°C", (255, 100, 100)),
        ("GPU Temp:", "42.8°C", (100, 255, 100)),
        ("CPU Usage:", "23%", (100, 200, 255)),
        ("Memory:", "2.1 GB", (255, 200, 100)),
        ("Disk:", "45%", (200, 100, 255)),
    ]
    
    y_pos = 45
    for label, value, color in data:
        # Label
        draw.text((10, y_pos), label, fill=(200, 200, 200))
        
        # Value (right-aligned)
        bbox = draw.textbbox((0, 0), value)
        value_width = bbox[2] - bbox[0]
        draw.text((width - value_width - 10, y_pos), value, fill=color)
        
        # Divider line
        y_pos += 20
        draw.line([10, y_pos, width - 10, y_pos], fill=(70, 70, 70), width=1)
        y_pos += 15
    
    # Status bar
    draw.rectangle([0, height - 25, width, height], fill=(30, 30, 30))
    draw.text((10, height - 20), "Status: OK", fill=(0, 255, 0))
    
    # Timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    bbox = draw.textbbox((0, 0), timestamp)
    ts_width = bbox[2] - bbox[0]
    draw.text((width - ts_width - 10, height - 20), timestamp, fill=(150, 150, 150))


def demo_text_effects(draw, width, height):
    """Text with various visual effects"""
    # Text with outline (shadow effect)
    text = "OUTLINED"
    x, y = 20, 20
    # Draw shadow/outline
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, fill=(0, 0, 0))
    # Draw main text
    draw.text((x, y), text, fill=(255, 255, 0))
    
    # Text with drop shadow
    text = "DROP SHADOW"
    x, y = 20, 60
    draw.text((x + 2, y + 2), text, fill=(0, 0, 0))  # Shadow
    draw.text((x, y), text, fill=(0, 255, 255))      # Main text
    
    # Gradient-like effect (manual)
    base_y = 100
    text = "GRADIENT"
    for i, char in enumerate(text):
        color_val = int((i / len(text)) * 255)
        draw.text((20 + i * 25, base_y), char, 
                 fill=(255, color_val, 255 - color_val))
    
    # Progress bar with text
    progress = 65  # 65%
    bar_y = 150
    bar_height = 30
    
    # Background
    draw.rectangle([10, bar_y, width - 10, bar_y + bar_height],
                  fill=(50, 50, 50))
    
    # Progress
    progress_width = int((width - 20) * (progress / 100))
    draw.rectangle([10, bar_y, 10 + progress_width, bar_y + bar_height],
                  fill=(100, 200, 255))
    
    # Text on bar
    text = f"{progress}%"
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, bar_y + 8), text, fill=(255, 255, 255))
    
    # Box with border and text
    box_y = 200
    draw.rectangle([15, box_y, width - 15, box_y + 60],
                  outline=(255, 255, 0), width=2)
    draw.text((25, box_y + 10), "This is a text box", fill=(255, 255, 255))
    draw.text((25, box_y + 25), "with a border", fill=(200, 200, 200))
    draw.text((25, box_y + 40), "and multiple lines", fill=(150, 150, 150))


def demo_table(draw, width, height):
    """Simple table layout"""
    # Title
    draw.rectangle([0, 0, width, 25], fill=(70, 70, 70))
    draw.text((10, 5), "Data Table", fill=(255, 255, 255))
    
    # Table headers
    headers = ["Item", "Value", "Status"]
    col_width = (width - 20) // 3
    y = 35
    
    for i, header in enumerate(headers):
        x = 10 + i * col_width
        draw.text((x, y), header, fill=(255, 255, 0))
    
    # Divider
    y += 20
    draw.line([10, y, width - 10, y], fill=(100, 100, 100), width=2)
    y += 10
    
    # Table rows
    rows = [
        ("Sensor 1", "23.4", "OK"),
        ("Sensor 2", "45.8", "OK"),
        ("Sensor 3", "12.1", "WARN"),
        ("Sensor 4", "78.9", "HIGH"),
    ]
    
    for row in rows:
        for i, cell in enumerate(row):
            x = 10 + i * col_width
            
            # Color code status column
            if i == 2:
                if cell == "OK":
                    color = (0, 255, 0)
                elif cell == "WARN":
                    color = (255, 200, 0)
                else:
                    color = (255, 100, 100)
            else:
                color = (200, 200, 200)
            
            draw.text((x, y), cell, fill=color)
        
        y += 20
        # Row divider
        draw.line([10, y, width - 10, y], fill=(60, 60, 60), width=1)
        y += 5


def demo_scrolling_text(draw, width, height, offset=0):
    """Simulate scrolling text"""
    messages = [
        "Welcome to ST7789 Display",
        "Text Demo Example",
        "Scroll through messages",
        "Using PIL/Pillow",
        "RGB565 color mode",
        "125 MHz SPI speed",
        "~16 FPS performance",
        "Press Ctrl+C to exit",
    ]
    
    # Background
    draw.rectangle([0, 0, width, height], fill=(20, 20, 60))
    
    # Title bar
    draw.rectangle([0, 0, width, 30], fill=(100, 100, 200))
    draw.text((10, 8), "Scrolling Demo", fill=(255, 255, 255))
    
    # Scrolling messages
    y_start = 50
    line_height = 30
    
    for i, msg in enumerate(messages):
        y = y_start + i * line_height - offset
        
        # Only draw if visible
        if -line_height < y < height:
            # Alternating colors
            color = (255, 255, 255) if i % 2 == 0 else (200, 200, 200)
            draw.text((20, y), msg, fill=color)



def main():
    """Main entry point for text demo"""
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        if args.legacy_rotation not in [0, 90, 180, 270]:
            print(f"Invalid rotation: {args.legacy_rotation}. Must be 0, 90, 180, or 270")
            sys.exit(1)
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    print("ST7789 Text Demo")
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
    print("\nCycling through text demos. Press Ctrl+C to exit.\n")
    
    # Define demos
    demos = [
        ("Basic Text", demo_basic_text),
        ("Multiline Text", demo_multiline_text),
        ("Text Positioning", demo_text_positioning),
        ("Text with Background", demo_text_with_background),
        ("Data Display", demo_data_display),
        ("Text Effects", demo_text_effects),
        ("Table Layout", demo_table),
    ]
    
    try:
        # Cycle through static demos
        for name, draw_func in demos:
            print(f"Displaying: {name}")
            
            # Create canvas
            image = Image.new('RGB', (display.width, display.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw the demo
            draw_func(draw, display.width, display.height)
            
            # Display
            display.display(image)
            time.sleep(3)
        
        # Scrolling demo (animated)
        print("Displaying: Scrolling Text (animated)")
        scroll_offset = 0
        for _ in range(100):  # About 6 seconds at 60ms per frame
            image = Image.new('RGB', (display.width, display.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            demo_scrolling_text(draw, display.width, display.height, scroll_offset)
            display.display(image)
            
            scroll_offset += 2
            if scroll_offset > 240:  # Reset when scrolled through all messages
                scroll_offset = 0
            
            time.sleep(0.06)  # ~16 FPS
                
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    finally:
        print("Cleaning up...")
        display.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()
