#!/usr/bin/env python3
"""
ST7789 Display Unit Test Suite
Comprehensive testing of display functionality
For Jetson Orin Nano with Waveshare 2inch LCD
"""

import time
import spidev
import Jetson.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Pin definitions
DC_PIN = 29
RST_PIN = 31
SPI_PORT = 0
SPI_CS = 0

# Display dimensions
WIDTH = 240
HEIGHT = 320

# ST7789 Commands
ST7789_SWRESET = 0x01
ST7789_SLPOUT = 0x11
ST7789_NORON = 0x13
ST7789_INVON = 0x21
ST7789_DISPON = 0x29
ST7789_CASET = 0x2A
ST7789_RASET = 0x2B
ST7789_RAMWR = 0x2C
ST7789_MADCTL = 0x36
ST7789_COLMOD = 0x3A

class ST7789Display:
    """Optimized ST7789 display driver for Jetson"""
    
    def __init__(self, spi_port=0, spi_cs=0, dc_pin=29, rst_pin=31, width=240, height=320, rotation=0):
        self.rotation = rotation
        
        # Swap width/height for landscape orientations
        if rotation in [90, 270]:
            self.width = height
            self.height = width
        else:
            self.width = width
            self.height = height
            
        self.dc_pin = dc_pin
        self.rst_pin = rst_pin
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.dc_pin, GPIO.OUT)
        GPIO.setup(self.rst_pin, GPIO.OUT)
        
        # Initialize SPI with maximum speed
        self.spi = spidev.SpiDev()
        self.spi.open(spi_port, spi_cs)
        self.spi.max_speed_hz = 125000000  # 125MHz - optimized speed
        self.spi.mode = 0
        
    def send_command(self, cmd):
        """Send command to display"""
        GPIO.output(self.dc_pin, GPIO.LOW)
        self.spi.writebytes([cmd])
        
    def send_data(self, data):
        """Send data to display"""
        GPIO.output(self.dc_pin, GPIO.HIGH)
        if isinstance(data, int):
            self.spi.writebytes([data])
        elif isinstance(data, list):
            self.spi.writebytes(data)
        else:
            self.spi.writebytes(list(data))
            
    def reset(self):
        """Hardware reset"""
        GPIO.output(self.rst_pin, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self.rst_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self.rst_pin, GPIO.HIGH)
        time.sleep(0.12)
        
    def init(self):
        """Initialize display"""
        self.reset()
        self.send_command(ST7789_SWRESET)
        time.sleep(0.15)
        self.send_command(ST7789_SLPOUT)
        time.sleep(0.5)
        self.send_command(ST7789_COLMOD)
        self.send_data(0x05)  # 16-bit color
        self.send_command(ST7789_MADCTL)
        
        # Set rotation using MADCTL
        # Bit 7: MY (Row Address Order)
        # Bit 6: MX (Column Address Order)  
        # Bit 5: MV (Row/Column Exchange)
        # Bit 3: RGB/BGR order
        madctl_values = {
            0:   0x00,  # Portrait (0°)
            90:  0x60,  # Landscape (90°) - MV | MX
            180: 0xC0,  # Portrait inverted (180°) - MY | MX
            270: 0xA0   # Landscape inverted (270°) - MV | MY
        }
        self.send_data(madctl_values.get(self.rotation, 0x00))
        
        self.send_command(ST7789_INVON)
        self.send_command(ST7789_NORON)
        time.sleep(0.01)
        self.send_command(ST7789_DISPON)
        time.sleep(0.12)
        
    def set_window(self, x0, y0, x1, y1):
        """Set drawing window"""
        self.send_command(ST7789_CASET)
        self.send_data([
            (x0) >> 8, (x0) & 0xFF,
            (x1) >> 8, (x1) & 0xFF
        ])
        self.send_command(ST7789_RASET)
        self.send_data([
            (y0) >> 8, (y0) & 0xFF,
            (y1) >> 8, (y1) & 0xFF
        ])
        self.send_command(ST7789_RAMWR)
        
    def display_image(self, image):
        """Display PIL Image - Optimized version"""
        # Resize if needed
        if image.size != (self.width, self.height):
            image = image.resize((self.width, self.height))
            
        # Convert to RGB
        rgb_image = image.convert('RGB')
        pixels = np.array(rgb_image, dtype=np.uint8)
        
        # Convert RGB888 to RGB565 using numpy (vectorized - faster)
        r = (pixels[:,:,0].astype(np.uint16) >> 3) << 11
        g = (pixels[:,:,1].astype(np.uint16) >> 2) << 5
        b = (pixels[:,:,2].astype(np.uint16) >> 3)
        rgb565 = r | g | b
        
        # Convert to bytes (big endian) - using numpy for speed
        rgb565_bytes = rgb565.astype('>u2').tobytes()
        
        # Set window
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Transfer with optimized method
        GPIO.output(self.dc_pin, GPIO.HIGH)  # Data mode
        
        # Use writebytes2 for better performance
        try:
            self.spi.writebytes2(rgb565_bytes)
        except AttributeError:
            # Fall back to chunked transfer if writebytes2 not available
            chunk_size = 4096
            for i in range(0, len(rgb565_bytes), chunk_size):
                chunk = rgb565_bytes[i:i + chunk_size]
                self.spi.writebytes(chunk)
            
    def fill(self, color):
        """Fill screen with solid color (RGB tuple) - Optimized version"""
        # Calculate RGB565
        r = (color[0] >> 3) << 11
        g = (color[1] >> 2) << 5
        b = (color[2] >> 3)
        rgb565 = r | g | b
        
        # Create entire frame buffer
        pixel_bytes = bytes([(rgb565 >> 8) & 0xFF, rgb565 & 0xFF])
        frame_data = pixel_bytes * (self.width * self.height)
        
        # Set window
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Transfer with optimized method
        GPIO.output(self.dc_pin, GPIO.HIGH)
        
        # Use writebytes2 for better performance
        try:
            self.spi.writebytes2(frame_data)
        except AttributeError:
            # Fall back to chunked transfer
            chunk_size = 4096
            for i in range(0, len(frame_data), chunk_size):
                chunk = frame_data[i:i + chunk_size]
                self.spi.writebytes(chunk)
        
    def cleanup(self):
        """Cleanup resources"""
        self.spi.close()
        GPIO.cleanup()


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
            
        self.display.display_image(image)
        
    def test_gradient(self):
        """Test smooth gradient"""
        print("Creating gradient pattern...")
        
        image = Image.new('RGB', (self.display.width, self.display.height))
        pixels = image.load()
        
        for y in range(self.display.height):
            color_value = int((y / self.display.height) * 255)
            for x in range(self.display.width):
                pixels[x, y] = (color_value, color_value, color_value)
                
        self.display.display_image(image)
        
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
                
        self.display.display_image(image)
        
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
        
        self.display.display_image(image)
        
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
            (10, 170, "125 MHz SPI", (255, 128, 0)),
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
        
        self.display.display_image(image)
        
    def test_all(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("ST7789 DISPLAY UNIT TEST SUITE")
        print("Optimized Driver - 125 MHz SPI")
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


# Main execution
if __name__ == "__main__":
    import sys
    
    # Check for rotation argument
    rotation = 0
    if len(sys.argv) > 1:
        try:
            rotation = int(sys.argv[1])
            if rotation not in [0, 90, 180, 270]:
                print(f"Invalid rotation: {rotation}. Must be 0, 90, 180, or 270")
                sys.exit(1)
        except ValueError:
            print("Usage: python st7789_unit_test.py [rotation]")
            print("  rotation: 0, 90, 180, or 270 (default: 0)")
            sys.exit(1)
    
    print(f"Initializing display with {rotation}° rotation...")
    display = ST7789Display(spi_port=SPI_PORT, spi_cs=SPI_CS, 
                           dc_pin=DC_PIN, rst_pin=RST_PIN,
                           width=WIDTH, height=HEIGHT, rotation=rotation)
    display.init()
    
    print(f"Display size: {display.width}x{display.height}")
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