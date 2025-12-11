#!/usr/bin/env python3
"""
ST7789 Display Unit Test Suite
Comprehensive testing of display functionality using the jetson_orin_st7789 package
For Jetson Orin Nano with Waveshare 2inch LCD
"""

import sys
import time
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Import the actual driver from the package
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
        description='ST7789 Unit Test Suite',
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


class DisplayTests:
    """Unit tests for ST7789 display"""
    
    def __init__(self, display):
        self.display = display
        self.test_count = 0
        self.pass_count = 0
        
    def run_test(self, name, test_func, duration=2):
        """Run a single test"""
        self.test_count += 1
        print(f"\n{'='*60}")
        print(f"TEST {self.test_count}: {name}")
        print(f"{'='*60}")
        
        try:
            test_func()
            self.pass_count += 1
            print(f"✓ PASS - Displaying for {duration}s...")
            time.sleep(duration)
            return True
        except Exception as e:
            print(f"✗ FAIL - {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def test_primary_colors(self):
        """Test primary colors: Red, Green, Blue"""
        print("Testing primary colors...")
        
        colors = [
            ("RED", (255, 0, 0)),
            ("GREEN", (0, 255, 0)),
            ("BLUE", (0, 0, 255))
        ]
        
        for name, color in colors:
            print(f"  Displaying {name} {color}")
            self.display.fill(color)
            time.sleep(1)
            
    def test_secondary_colors(self):
        """Test secondary colors: Cyan, Magenta, Yellow"""
        print("Testing secondary colors...")
        
        colors = [
            ("CYAN", (0, 255, 255)),
            ("MAGENTA", (255, 0, 255)),
            ("YELLOW", (255, 255, 0))
        ]
        
        for name, color in colors:
            print(f"  Displaying {name} {color}")
            self.display.fill(color)
            time.sleep(1)
            
    def test_grayscale(self):
        """Test grayscale: Black, Gray, White"""
        print("Testing grayscale...")
        
        colors = [
            ("BLACK", (0, 0, 0)),
            ("DARK GRAY", (64, 64, 64)),
            ("GRAY", (128, 128, 128)),
            ("LIGHT GRAY", (192, 192, 192)),
            ("WHITE", (255, 255, 255))
        ]
        
        for name, color in colors:
            print(f"  Displaying {name} {color}")
            self.display.fill(color)
            time.sleep(0.8)
            
    def test_color_bars(self):
        """Test vertical color bars"""
        print("Creating color bars pattern...")
        
        image = Image.new('RGB', (self.display.width, self.display.height))
        draw = ImageDraw.Draw(image)
        
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 255, 255),# White
            (0, 0, 0)       # Black
        ]
        
        bar_width = self.display.width // len(colors)
        
        for i, color in enumerate(colors):
            x0 = i * bar_width
            x1 = x0 + bar_width
            draw.rectangle([x0, 0, x1, self.display.height], fill=color)
            
        self.display.display(image)
        
    def test_gradient(self):
        """Test smooth gradient"""
        print("Creating gradient pattern...")
        
        image = Image.new('RGB', (self.display.width, self.display.height))
        pixels = image.load()
        
        for y in range(self.display.height):
            color_value = int((y / self.display.height) * 255)
            for x in range(self.display.width):
                pixels[x, y] = (color_value, color_value, color_value)
                
        self.display.display(image)
        
    def test_checkerboard(self):
        """Test checkerboard pattern"""
        print("Creating checkerboard pattern...")
        
        image = Image.new('RGB', (self.display.width, self.display.height))
        draw = ImageDraw.Draw(image)
        
        square_size = 20
        
        for y in range(0, self.display.height, square_size):
            for x in range(0, self.display.width, square_size):
                if ((x // square_size) + (y // square_size)) % 2:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                draw.rectangle([x, y, x + square_size, y + square_size], fill=color)
                
        self.display.display(image)
        
    def test_shapes(self):
        """Test geometric shapes"""
        print("Drawing geometric shapes...")
        
        image = Image.new('RGB', (self.display.width, self.display.height), (0, 0, 64))
        draw = ImageDraw.Draw(image)
        
        # Rectangle
        draw.rectangle([20, 20, 100, 80], outline=(255, 0, 0), width=3)
        
        # Filled rectangle
        draw.rectangle([120, 20, 220, 80], fill=(0, 255, 0))
        
        # Circle
        draw.ellipse([40, 100, 120, 180], outline=(255, 255, 0), width=3)
        
        # Filled circle
        draw.ellipse([140, 100, 200, 160], fill=(255, 0, 255))
        
        # Line
        draw.line([20, 200, 220, 200], fill=(0, 255, 255), width=5)
        
        # Triangle
        draw.polygon([(120, 220), (70, 300), (170, 300)], outline=(255, 255, 255), width=3)
        
        self.display.display(image)
        
    def test_text(self):
        """Test text rendering"""
        print("Rendering text...")
        
        image = Image.new('RGB', (self.display.width, self.display.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Orientation-specific text
        orientation = {0: "Portrait", 90: "Landscape", 180: "Portrait 180°", 270: "Landscape 270°"}
        rot_text = orientation.get(self.display.rotation, "Unknown")
        
        # Use default font
        texts = [
            (10, 20, "ST7789 Display", (255, 255, 255)),
            (10, 50, f"{self.display.width}x{self.display.height} px", (255, 255, 0)),
            (10, 80, f"Rotation: {self.display.rotation}°", (0, 255, 255)),
            (10, 110, rot_text, (255, 0, 255)),
            (10, 140, "RGB565 color", (0, 255, 0)),
            (10, 170, f"{self.display.spi_speed_hz/1e6:.0f} MHz SPI", (255, 128, 0)),
        ]
        
        # Add final test status lower on screen
        status_y = self.display.height - 80
        texts.append((10, status_y, "All Tests", (255, 128, 0)))
        texts.append((10, status_y + 30, "PASSED!", (0, 255, 0)))
        
        for x, y, text, color in texts:
            draw.text((x, y), text, fill=color)
            
        # Draw border
        draw.rectangle([0, 0, self.display.width-1, self.display.height-1], 
                      outline=(255, 255, 255), width=2)
        
        self.display.display(image)
        
    def test_clear_method(self):
        """Test clear() convenience method"""
        print("Testing clear() method...")
        
        # Clear to different colors
        colors = [
            ("BLACK", (0, 0, 0)),
            ("WHITE", (255, 255, 255)),
            ("RED", (255, 0, 0)),
        ]
        
        for name, color in colors:
            print(f"  Clearing to {name}")
            self.display.clear(color)
            time.sleep(0.5)
            
    def test_context_manager(self):
        """Test that display works as context manager"""
        print("Testing context manager usage...")
        
        # This test validates the __enter__ and __exit__ methods exist
        # The actual display object is already created, so we just verify the methods
        assert hasattr(self.display, '__enter__'), "Missing __enter__ method"
        assert hasattr(self.display, '__exit__'), "Missing __exit__ method"
        
        print("  Context manager methods validated")
        self.display.fill((0, 128, 0))
        
    def test_all(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("ST7789 DISPLAY UNIT TEST SUITE")
        print("Using jetson_orin_st7789 package driver")
        print("="*60)
        
        tests = [
            ("Primary Colors (R,G,B)", self.test_primary_colors, 1),
            ("Secondary Colors (C,M,Y)", self.test_secondary_colors, 1),
            ("Grayscale Levels", self.test_grayscale, 1),
            ("Color Bars Pattern", self.test_color_bars, 2),
            ("Gradient Pattern", self.test_gradient, 2),
            ("Checkerboard Pattern", self.test_checkerboard, 2),
            ("Geometric Shapes", self.test_shapes, 3),
            ("Text Rendering", self.test_text, 3),
            ("Clear Method", self.test_clear_method, 1),
            ("Context Manager", self.test_context_manager, 2),
        ]
        
        for name, test_func, duration in tests:
            self.run_test(name, test_func, duration)
            
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.test_count}")
        print(f"Passed: {self.pass_count}")
        print(f"Failed: {self.test_count - self.pass_count}")
        print(f"Success Rate: {(self.pass_count/self.test_count)*100:.1f}%")
        print("="*60)
        
        if self.pass_count == self.test_count:
            print("\n✓ ALL TESTS PASSED! Display is working correctly.")
        else:
            print("\n✗ Some tests failed. Check the output above.")



def main():
    """Main entry point for unit tests"""
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        if args.legacy_rotation not in [0, 90, 180, 270]:
            print(f"Invalid rotation: {args.legacy_rotation}. Must be 0, 90, 180, or 270")
            sys.exit(1)
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    print("ST7789 Unit Test Suite")
    print("="*60)
    print(f"Wiring preset: {args.wiring} - {wiring['description']}")
    print(f"  DC Pin:  {wiring['dc_pin']} (BOARD)")
    print(f"  RST Pin: {wiring['rst_pin']} (BOARD)")
    print(f"Rotation: {args.rotation}°")
    print("="*60)
    
    # Initialize display using the package driver
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
        print("3. Check hardware connections")
        print("4. Verify SPI is enabled in device tree")
        sys.exit(1)
    print(f"Display initialized: {display}")
    print("Starting unit tests...\n")
    
    tests = DisplayTests(display)
    
    try:
        tests.test_all()
        
        print("\nTests complete! Press Ctrl+C to exit")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nCleaning up...")
        display.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()
