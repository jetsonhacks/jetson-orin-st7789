# ST7789 Examples - Wiring Preset Support

## Overview

All example files have been updated to support command-line selection of wiring pin configurations through preset profiles. This makes it easier to work with different hardware configurations without modifying code.

## Updated Files

1. **`__init__.py`** - Fixed module documentation
2. **`basic_colors.py`** - Simple color cycling example
3. **`basic_colors_demo.py`** - Extended color demonstration
4. **`shapes_demo.py`** - Geometric shapes and patterns
5. **`text_demo.py`** - Text rendering demonstrations
6. **`system_monitor_demo.py`** - Real-time system statistics display
7. **`st7789_unit_tests.py`** - Comprehensive test suite

## Wiring Presets

Three preset configurations are now available:

### Jetson (Default)
- **DC Pin:** 29 (BOARD numbering)
- **RST Pin:** 31 (BOARD numbering)
- **Description:** Default Jetson wiring configuration

### Waveshare
- **DC Pin:** 25 (BOARD numbering)
- **RST Pin:** 27 (BOARD numbering)
- **Description:** Waveshare 2inch LCD Module default wiring

### Adafruit
- **DC Pin:** 24 (BOARD numbering)
- **RST Pin:** 25 (BOARD numbering)
- **Description:** Adafruit ST7789 breakout board default wiring

## Usage

### New Command-Line Interface

All examples now support two command-line arguments:

```bash
# Using named arguments (recommended)
python script_name.py --wiring PRESET --rotation ANGLE

# Examples:
python basic_colors_demo.py --wiring waveshare --rotation 90
python text_demo.py --wiring adafruit --rotation 180
python st7789_unit_tests.py --wiring jetson --rotation 0
```

### Legacy Compatibility

The old positional rotation argument is still supported for backwards compatibility:

```bash
# Legacy syntax (still works)
python basic_colors_demo.py 90
python shapes_demo.py 180
```

### Help Information

Each script provides detailed help:

```bash
python script_name.py --help
```

Output example:
```
usage: basic_colors_demo.py [-h] [--rotation {0,90,180,270}] 
                            [--wiring {jetson,waveshare,adafruit}]

ST7789 Basic Colors Demo

optional arguments:
  -h, --help            show this help message and exit
  --rotation {0,90,180,270}
                        Display rotation in degrees (default: 0)
  --wiring {jetson,waveshare,adafruit}
                        Wiring preset to use (default: jetson)

Wiring Presets:
  jetson    : DC=29, RST=31 (BOARD numbering)
  waveshare : DC=25, RST=27 (BOARD numbering)
  adafruit  : DC=24, RST=25 (BOARD numbering)
  
Examples:
  basic_colors_demo.py --rotation 90
  basic_colors_demo.py --wiring waveshare --rotation 180
  basic_colors_demo.py --wiring adafruit
```

## Implementation Details

### Code Structure

Each example file now includes:

1. **Wiring Presets Dictionary:**
```python
WIRING_PRESETS = {
    'jetson': {
        'dc_pin': 29,
        'rst_pin': 31,
        'description': 'Jetson default wiring (BOARD numbering)'
    },
    # ... more presets
}
```

2. **Argument Parser Function:**
```python
def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(...)
    parser.add_argument('--rotation', ...)
    parser.add_argument('--wiring', ...)
    parser.add_argument('legacy_rotation', nargs='?', ...)  # For backwards compatibility
    return parser.parse_args()
```

3. **Updated Main Function:**
```python
def main():
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    # Initialize with preset values
    display = ST7789(
        dc_pin=wiring['dc_pin'],
        rst_pin=wiring['rst_pin'],
        rotation=args.rotation,
        # ... other parameters
    )
```

### Benefits

1. **Flexibility:** Easily switch between different hardware configurations
2. **No Code Changes:** Change wiring without editing source files
3. **Clear Documentation:** Presets are self-documenting
4. **Backwards Compatible:** Old scripts still work with positional arguments
5. **Extensible:** Easy to add new presets for custom hardware

## Adding Custom Presets

To add a custom wiring configuration, edit the `WIRING_PRESETS` dictionary:

```python
WIRING_PRESETS = {
    # ... existing presets ...
    'custom': {
        'dc_pin': YOUR_DC_PIN,
        'rst_pin': YOUR_RST_PIN,
        'description': 'Your custom configuration'
    }
}
```

Then use it with:
```bash
python script_name.py --wiring custom --rotation 90
```

## Examples

### Basic Color Demo
```bash
# Using Waveshare wiring in landscape mode
python basic_colors_demo.py --wiring waveshare --rotation 90

# Using Adafruit wiring in portrait mode (upside down)
python basic_colors_demo.py --wiring adafruit --rotation 180
```

### System Monitor
```bash
# Using Jetson default wiring in landscape
python system_monitor_demo.py --wiring jetson --rotation 90
```

### Unit Tests
```bash
# Run tests with Waveshare wiring
python st7789_unit_tests.py --wiring waveshare
```

## Migration Guide

If you have custom scripts using the old format:

**Old:**
```python
display = ST7789(
    dc_pin=29,
    rst_pin=31,
    rotation=0,
    # ...
)
```

**New:**
```python
# Add at the top of your file
WIRING_PRESETS = { ... }  # Copy from any example
def parse_arguments(): ...  # Copy from any example

# In main():
args = parse_arguments()
wiring = WIRING_PRESETS[args.wiring]

display = ST7789(
    dc_pin=wiring['dc_pin'],
    rst_pin=wiring['rst_pin'],
    rotation=args.rotation,
    # ...
)
```

## Notes

- All pin numbers use **BOARD numbering** (physical pin numbers on the header)
- The default preset is **jetson** (DC=29, RST=31)
- SPI settings (port, CS, speed) remain hardcoded as they're typically the same across configurations
- The `--help` flag works with all examples to show usage information
