
"""
ST7789 Display Driver for NVIDIA Jetson
========================================

A high-performance Python driver for ST7789-based LCD displays on NVIDIA Jetson platforms.

Features:
    - Optimized SPI communication (up to 125 MHz)
    - Hardware-accelerated RGB565 conversion using NumPy
    - Support for all orientations (0°, 90°, 180°, 270°)
    - PIL/Pillow image rendering
    - ~16 FPS sustained performance on Jetson Orin Nano

Example:
    >>> from st7789_jetson import ST7789
    >>> from PIL import Image, ImageDraw
    >>> 
    >>> # Initialize display
    >>> display = ST7789(
    ...     spi_port=0,
    ...     spi_cs=0,
    ...     dc_pin=29,
    ...     rst_pin=31,
    ...     width=240,
    ...     height=320,
    ...     rotation=0,
    ...     spi_speed_hz=125000000
    ... )
    >>> 
    >>> # Fill screen with color
    >>> display.fill((255, 0, 0))  # Red
    >>> 
    >>> # Display an image
    >>> image = Image.new('RGB', (240, 320), (0, 0, 255))
    >>> draw = ImageDraw.Draw(image)
    >>> draw.text((10, 10), "Hello World!", fill=(255, 255, 255))
    >>> display.display(image)
    >>> 
    >>> # Cleanup when done
    >>> display.cleanup()

Author: Your Name
License: MIT
Repository: https://github.com/jetsonhacks/st7789-jetson
"""

import time
from typing import Tuple, Optional, Union
import spidev
import numpy as np
from PIL import Image

try:
    import Jetson.GPIO as GPIO
    JETSON_GPIO_AVAILABLE = True
except ImportError:
    JETSON_GPIO_AVAILABLE = False


# ST7789 Command Set
_ST7789_SWRESET = 0x01  # Software reset
_ST7789_SLPOUT = 0x11   # Sleep out
_ST7789_NORON = 0x13    # Normal display mode on
_ST7789_INVON = 0x21    # Display inversion on
_ST7789_DISPON = 0x29   # Display on
_ST7789_CASET = 0x2A    # Column address set
_ST7789_RASET = 0x2B    # Row address set
_ST7789_RAMWR = 0x2C    # Memory write
_ST7789_MADCTL = 0x36   # Memory data access control
_ST7789_COLMOD = 0x3A   # Interface pixel format


class ST7789Error(Exception):
    """Base exception for ST7789 driver errors."""
    pass


class ST7789InitError(ST7789Error):
    """Raised when display initialization fails."""
    pass


class ST7789:
    """
    ST7789 LCD display driver for NVIDIA Jetson platforms.
    
    This driver provides hardware-accelerated SPI communication for ST7789-based
    LCD displays. It uses Jetson.GPIO for control pins and optimized NumPy operations
    for fast RGB565 conversion.
    
    Attributes:
        width (int): Display width in pixels (accounts for rotation)
        height (int): Display height in pixels (accounts for rotation)
        rotation (int): Display rotation in degrees (0, 90, 180, 270)
        spi_speed_hz (int): SPI clock speed in Hz
        
    Args:
        spi_port (int): SPI port number (default: 0 for /dev/spidev0.0)
        spi_cs (int): SPI chip select (default: 0)
        dc_pin (int): Data/Command GPIO pin in BOARD mode (required)
        rst_pin (int): Reset GPIO pin in BOARD mode (required)
        width (int): Display width in pixels (default: 240)
        height (int): Display height in pixels (default: 320)
        rotation (int): Display rotation in degrees - 0, 90, 180, or 270 (default: 0)
        spi_speed_hz (int): SPI clock speed in Hz (default: 125000000)
        
    Raises:
        ST7789InitError: If initialization fails
        ImportError: If Jetson.GPIO is not available
        
    Example:
        >>> display = ST7789(dc_pin=29, rst_pin=31, rotation=90)
        >>> display.fill((0, 255, 0))  # Green screen
        >>> display.cleanup()
    """
    
    def __init__(
        self,
        spi_port: int = 0,
        spi_cs: int = 0,
        dc_pin: int = 29,
        rst_pin: int = 31,
        width: int = 240,
        height: int = 320,
        rotation: int = 0,
        spi_speed_hz: int = 125000000
    ):
        """Initialize ST7789 display driver."""
        
        if not JETSON_GPIO_AVAILABLE:
            raise ImportError(
                "Jetson.GPIO is required but not available. "
                "Install with: sudo pip3 install Jetson.GPIO"
            )
        
        if rotation not in [0, 90, 180, 270]:
            raise ValueError(f"rotation must be 0, 90, 180, or 270, got {rotation}")
        
        self.rotation = rotation
        self.spi_speed_hz = spi_speed_hz
        self._dc_pin = dc_pin
        self._rst_pin = rst_pin
        
        # Swap dimensions for landscape orientations
        if rotation in [90, 270]:
            self.width = height
            self.height = width
        else:
            self.width = width
            self.height = height
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self._dc_pin, GPIO.OUT)
        GPIO.setup(self._rst_pin, GPIO.OUT)
        
        # Initialize SPI
        try:
            self._spi = spidev.SpiDev()
            self._spi.open(spi_port, spi_cs)
            self._spi.max_speed_hz = spi_speed_hz
            self._spi.mode = 0
        except Exception as e:
            raise ST7789InitError(f"Failed to initialize SPI: {e}")
        
        # Initialize display hardware
        try:
            self._init_display()
        except Exception as e:
            self.cleanup()
            raise ST7789InitError(f"Failed to initialize display: {e}")
    
    def _send_command(self, cmd: int) -> None:
        """Send command byte to display."""
        GPIO.output(self._dc_pin, GPIO.LOW)
        self._spi.writebytes([cmd])
    
    def _send_data(self, data: Union[int, bytes, list]) -> None:
        """Send data byte(s) to display."""
        GPIO.output(self._dc_pin, GPIO.HIGH)
        if isinstance(data, int):
            self._spi.writebytes([data])
        else:
            self._spi.writebytes(data)
    
    def _hardware_reset(self) -> None:
        """Perform hardware reset of display."""
        GPIO.output(self._rst_pin, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self._rst_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self._rst_pin, GPIO.HIGH)
        time.sleep(0.12)
    
    def _init_display(self) -> None:
        """Initialize ST7789 display with proper configuration."""
        # Hardware reset
        self._hardware_reset()
        
        # Software reset
        self._send_command(_ST7789_SWRESET)
        time.sleep(0.15)
        
        # Sleep out
        self._send_command(_ST7789_SLPOUT)
        time.sleep(0.5)
        
        # Color mode: 16-bit RGB565
        self._send_command(_ST7789_COLMOD)
        self._send_data(0x05)
        
        # Memory access control (rotation)
        self._send_command(_ST7789_MADCTL)
        madctl_values = {
            0:   0x00,  # Portrait
            90:  0x60,  # Landscape (MV | MX)
            180: 0xC0,  # Portrait inverted (MY | MX)
            270: 0xA0   # Landscape inverted (MV | MY)
        }
        self._send_data(madctl_values[self.rotation])
        
        # Display inversion on
        self._send_command(_ST7789_INVON)
        
        # Normal display mode
        self._send_command(_ST7789_NORON)
        time.sleep(0.01)
        
        # Display on
        self._send_command(_ST7789_DISPON)
        time.sleep(0.12)
    
    def _set_window(self, x0: int, y0: int, x1: int, y1: int) -> None:
        """
        Set the drawing window (address window).
        
        Args:
            x0: Start column
            y0: Start row
            x1: End column
            y1: End row
        """
        # Column address set
        self._send_command(_ST7789_CASET)
        self._send_data([
            (x0 >> 8) & 0xFF, x0 & 0xFF,
            (x1 >> 8) & 0xFF, x1 & 0xFF
        ])
        
        # Row address set
        self._send_command(_ST7789_RASET)
        self._send_data([
            (y0 >> 8) & 0xFF, y0 & 0xFF,
            (y1 >> 8) & 0xFF, y1 & 0xFF
        ])
        
        # Memory write
        self._send_command(_ST7789_RAMWR)
    
    def display(self, image: Image.Image) -> None:
        """
        Display a PIL Image on the screen.
        
        The image is automatically resized to match the display dimensions if needed,
        converted to RGB565 format, and transferred via SPI.
        
        Args:
            image: PIL Image object to display
            
        Example:
            >>> from PIL import Image, ImageDraw
            >>> img = Image.new('RGB', (240, 320), (255, 0, 0))
            >>> draw = ImageDraw.Draw(img)
            >>> draw.text((10, 10), "Hello!", fill=(255, 255, 255))
            >>> display.display(img)
        """
        # Resize if dimensions don't match
        if image.size != (self.width, self.height):
            image = image.resize((self.width, self.height), Image.LANCZOS)
        
        # Convert to RGB
        rgb_image = image.convert('RGB')
        pixels = np.array(rgb_image, dtype=np.uint8)
        
        # Convert RGB888 to RGB565 using vectorized NumPy operations
        r = (pixels[:, :, 0].astype(np.uint16) >> 3) << 11
        g = (pixels[:, :, 1].astype(np.uint16) >> 2) << 5
        b = (pixels[:, :, 2].astype(np.uint16) >> 3)
        rgb565 = r | g | b
        
        # Convert to big-endian bytes
        rgb565_bytes = rgb565.astype('>u2').tobytes()
        
        # Set drawing window to full screen
        self._set_window(0, 0, self.width - 1, self.height - 1)
        
        # Transfer frame data
        GPIO.output(self._dc_pin, GPIO.HIGH)
        try:
            # Use writebytes2 for better performance (no RX buffer)
            self._spi.writebytes2(rgb565_bytes)
        except AttributeError:
            # Fallback to chunked writebytes if writebytes2 unavailable
            chunk_size = 4096
            for i in range(0, len(rgb565_bytes), chunk_size):
                self._spi.writebytes(rgb565_bytes[i:i + chunk_size])
    
    def fill(self, color: Tuple[int, int, int]) -> None:
        """
        Fill the entire screen with a solid color.
        
        This is optimized for solid fills and is faster than creating and
        displaying a PIL Image.
        
        Args:
            color: RGB color tuple (r, g, b) where each value is 0-255
            
        Example:
            >>> display.fill((255, 0, 0))    # Red
            >>> display.fill((0, 255, 0))    # Green
            >>> display.fill((0, 0, 255))    # Blue
            >>> display.fill((255, 255, 255)) # White
        """
        # Convert RGB888 to RGB565
        r = (color[0] >> 3) << 11
        g = (color[1] >> 2) << 5
        b = (color[2] >> 3)
        rgb565 = r | g | b
        
        # Create frame buffer
        pixel_bytes = bytes([(rgb565 >> 8) & 0xFF, rgb565 & 0xFF])
        frame_data = pixel_bytes * (self.width * self.height)
        
        # Set drawing window to full screen
        self._set_window(0, 0, self.width - 1, self.height - 1)
        
        # Transfer frame data
        GPIO.output(self._dc_pin, GPIO.HIGH)
        try:
            self._spi.writebytes2(frame_data)
        except AttributeError:
            chunk_size = 4096
            for i in range(0, len(frame_data), chunk_size):
                self._spi.writebytes(frame_data[i:i + chunk_size])
    
    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Clear the screen to a specific color (default: black).
        
        This is an alias for fill() with a more intuitive name.
        
        Args:
            color: RGB color tuple (default: black)
            
        Example:
            >>> display.clear()  # Clear to black
            >>> display.clear((255, 255, 255))  # Clear to white
        """
        self.fill(color)
    
    def cleanup(self) -> None:
        """
        Release hardware resources.
        
        This closes the SPI connection and cleans up GPIO pins.
        Should be called when done using the display.
        
        Example:
            >>> display = ST7789(dc_pin=29, rst_pin=31)
            >>> try:
            ...     display.fill((255, 0, 0))
            ... finally:
            ...     display.cleanup()
        """
        try:
            self._spi.close()
        except:
            pass
        
        try:
            GPIO.cleanup()
        except:
            pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically cleanup."""
        self.cleanup()
        return False
    
    def __repr__(self) -> str:
        """String representation of display object."""
        return (
            f"ST7789(width={self.width}, height={self.height}, "
            f"rotation={self.rotation}, spi_speed={self.spi_speed_hz/1e6:.0f}MHz)"
        )


__version__ = "1.0.0"
__all__ = ["ST7789", "ST7789Error", "ST7789InitError"]