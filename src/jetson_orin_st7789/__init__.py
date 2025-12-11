"""ST7789 Display Driver for NVIDIA Jetson Orin with Pin Preset Support."""

from .driver import ST7789, ST7789Error, ST7789InitError
from .pinouts import (
    PinConfig,
    WAVESHARE_PINS,
    ADAFRUIT_PINS,
    JETSON_PINS,
    get_preset,
    list_presets,
    print_preset_info,
)

__version__ = "1.0.0"
__all__ = [
    "ST7789",
    "ST7789Error",
    "ST7789InitError",
    "PinConfig",
    "WAVESHARE_PINS",
    "ADAFRUIT_PINS",
    "JETSON_PINS",
    "get_preset",
    "list_presets",
    "print_preset_info",
    "from_preset",
]


# Convenience function for creating display from preset
def from_preset(preset_name: str, **kwargs):
    """
    Create ST7789 display instance from a pin configuration preset.
    
    Args:
        preset_name: Name of preset ('waveshare', 'adafruit', 'jetson')
        **kwargs: Additional arguments to pass to ST7789 (width, height, rotation, etc.)
        
    Returns:
        ST7789 display instance
        
    Example:
        >>> from jetson_orin_st7789 import from_preset
        >>> 
        >>> # Use Waveshare pinout
        >>> display = from_preset('waveshare', rotation=90)
        >>> 
        >>> # Use Adafruit pinout with custom size
        >>> display = from_preset('adafruit', width=240, height=320)
    """
    config = get_preset(preset_name)
    
    return ST7789(
        dc_pin=config.dc_pin,
        rst_pin=config.rst_pin,
        spi_port=config.spi_port,
        spi_cs=config.spi_cs,
        **kwargs
    )
