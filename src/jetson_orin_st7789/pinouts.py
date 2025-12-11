"""
Pin Configuration Presets for ST7789 Displays
===============================================

Predefined pinouts for popular ST7789 display modules to simplify setup.

Supported configurations:
- Jetson (default - recommended for Jetson Orin/Xavier)
- Waveshare (Raspberry Pi compatible)
- Adafruit (Raspberry Pi compatible)
- Custom

All pin numbers use BOARD mode (physical header pin numbers).
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class PinConfig:
    """Display pin configuration"""
    dc_pin: int
    rst_pin: int
    spi_port: int = 0
    spi_cs: int = 0
    bl_pin: int = None  # Backlight pin (optional)
    name: str = "Custom"
    description: str = ""


# Waveshare 2inch LCD Module pinout for Raspberry Pi compatible boards
# http://www.waveshare.com/wiki/2inch_LCD_Module
WAVESHARE_PINS = PinConfig(
    dc_pin=22,      # BCM 25 = Board 22 (DS pin on Waveshare)
    rst_pin=13,     # BCM 27 = Board 13 (RST pin on Waveshare)
    bl_pin=12,      # BCM 18 = Board 12 (BL pin on Waveshare)
    spi_port=0,
    spi_cs=0,       # CE0 = Board 24
    name="Waveshare",
    description="Waveshare 2inch LCD Module (ST7789V) - Raspberry Pi compatible pinout"
)

# Adafruit 2.0" 320x240 Color IPS TFT Display pinout
# https://learn.adafruit.com/2-0-inch-320-x-240-color-ips-tft-display/python-wiring-and-setup
ADAFRUIT_PINS = PinConfig(
    dc_pin=25,      # BCM 25 = Board 25 (D/C pin on Adafruit)
    rst_pin=24,     # BCM 24 = Board 24 (RST pin on Adafruit... wait, that's CE0!)
    spi_port=0,
    spi_cs=0,       # CE0 = Board 24
    name="Adafruit",
    description="Adafruit 2.0\" 320x240 IPS TFT (ST7789) - Raspberry Pi compatible pinout"
)

# CORRECTED Adafruit pinout - Adafruit uses GPIO 24 and 25, let me check board pins
# BCM 24 = Board 18
# BCM 25 = Board 22
ADAFRUIT_PINS = PinConfig(
    dc_pin=22,      # BCM 25 = Board 22 (D/C pin on Adafruit)
    rst_pin=18,     # BCM 24 = Board 18 (RST pin on Adafruit)
    spi_port=0,
    spi_cs=0,       # CE0 = Board 24
    name="Adafruit",
    description="Adafruit 2.0\" 320x240 IPS TFT (ST7789) - Raspberry Pi compatible pinout"
)

# Jetson Orin/Xavier default pinout (RECOMMENDED for Jetson hardware)
# This is the standard pinout for native Jetson displays
JETSON_PINS = PinConfig(
    dc_pin=29,      # GPIO (Board 29) - soc_gpio32_pq5
    rst_pin=31,     # GPIO (Board 31) - soc_gpio33_pq6
    spi_port=0,
    spi_cs=0,
    name="Jetson",
    description="Default pinout for Jetson Orin/Xavier (pins 29, 31 - requires device tree overlay)"
)

# All available presets (Jetson first as recommended default)
PRESETS: Dict[str, PinConfig] = {
    'jetson': JETSON_PINS,
    'waveshare': WAVESHARE_PINS,
    'adafruit': ADAFRUIT_PINS,
}


def get_preset(name: str) -> PinConfig:
    """
    Get a pin configuration preset by name.
    
    Args:
        name: Preset name ('waveshare', 'adafruit', 'jetson', or 'custom')
        
    Returns:
        PinConfig object with pin numbers
        
    Raises:
        ValueError: If preset name is not recognized
        
    Example:
        >>> from jetson_orin_st7789.pinouts import get_preset
        >>> config = get_preset('waveshare')
        >>> display = ST7789(dc_pin=config.dc_pin, rst_pin=config.rst_pin)
    """
    name_lower = name.lower()
    
    if name_lower not in PRESETS:
        available = ', '.join(PRESETS.keys())
        raise ValueError(
            f"Unknown preset '{name}'. Available presets: {available}"
        )
    
    return PRESETS[name_lower]


def list_presets() -> Dict[str, str]:
    """
    List all available pin configuration presets.
    
    Returns:
        Dictionary mapping preset names to descriptions
        
    Example:
        >>> from jetson_orin_st7789.pinouts import list_presets
        >>> for name, desc in list_presets().items():
        ...     print(f"{name}: {desc}")
    """
    return {name: config.description for name, config in PRESETS.items()}


def print_preset_info(name: str = None) -> None:
    """
    Print detailed information about a preset or all presets.
    
    Args:
        name: Optional preset name. If None, prints all presets.
        
    Example:
        >>> from jetson_orin_st7789.pinouts import print_preset_info
        >>> print_preset_info('waveshare')
        >>> print_preset_info()  # Print all
    """
    if name:
        config = get_preset(name)
        _print_single_preset(name, config)
    else:
        print("Available ST7789 Display Pin Presets")
        print("=" * 70)
        for preset_name, config in PRESETS.items():
            _print_single_preset(preset_name, config)
            print()


def _print_single_preset(name: str, config: PinConfig) -> None:
    """Print information about a single preset"""
    print(f"\n{name.upper()}: {config.description}")
    print("-" * 70)
    print(f"  DC Pin:       Board {config.dc_pin}")
    print(f"  RST Pin:      Board {config.rst_pin}")
    print(f"  SPI Port:     {config.spi_port}")
    print(f"  SPI CS:       {config.spi_cs} (Board 24 for CE0)")
    if config.bl_pin:
        print(f"  Backlight:    Board {config.bl_pin}")
    else:
        print(f"  Backlight:    Not specified (connect to 3.3V)")
    
    print(f"\n  Standard SPI pins (same for all presets):")
    print(f"    MOSI:       Board 19")
    print(f"    SCLK:       Board 23")
    print(f"    VCC:        Board 1 or 17 (3.3V)")
    print(f"    GND:        Board 6, 9, 14, 20, 25, 30, 34, or 39")


# Pin mapping reference for common boards
BCM_TO_BOARD = {
    # BCM GPIO : Board Pin
    2: 3,    # I2C SDA
    3: 5,    # I2C SCL
    4: 7,
    17: 11,
    27: 13,
    22: 15,
    10: 19,  # MOSI
    9: 21,   # MISO
    11: 23,  # SCLK
    8: 24,   # CE0
    7: 26,   # CE1
    18: 12,  # PWM
    23: 16,
    24: 18,
    25: 22,
    5: 29,
    6: 31,
    12: 32,
    13: 33,
    19: 35,
    16: 36,
    26: 37,
    20: 38,
    21: 40,
}

BOARD_TO_BCM = {v: k for k, v in BCM_TO_BOARD.items()}


def bcm_to_board(bcm_pin: int) -> int:
    """Convert BCM GPIO number to Board pin number"""
    if bcm_pin not in BCM_TO_BOARD:
        raise ValueError(f"BCM pin {bcm_pin} not found in mapping")
    return BCM_TO_BOARD[bcm_pin]


def board_to_bcm(board_pin: int) -> int:
    """Convert Board pin number to BCM GPIO number"""
    if board_pin not in BOARD_TO_BCM:
        raise ValueError(f"Board pin {board_pin} not found in mapping")
    return BOARD_TO_BCM[board_pin]


__all__ = [
    'PinConfig',
    'WAVESHARE_PINS',
    'ADAFRUIT_PINS', 
    'JETSON_PINS',
    'PRESETS',
    'get_preset',
    'list_presets',
    'print_preset_info',
    'bcm_to_board',
    'board_to_bcm',
]
