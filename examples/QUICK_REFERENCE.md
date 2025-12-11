# ST7789 Wiring Presets - Quick Reference

## Command-Line Usage

```bash
# General syntax
python example.py --wiring PRESET --rotation ANGLE

# Common examples
python basic_colors_demo.py --wiring waveshare --rotation 90
python text_demo.py --wiring adafruit --rotation 180
python shapes_demo.py --wiring jetson --rotation 0

# Legacy syntax (still supported)
python example.py 90
```

## Wiring Pin Configurations

| Preset    | DC Pin | RST Pin | Description                    |
|-----------|--------|---------|--------------------------------|
| jetson    | 29     | 31      | Jetson default (BOARD numbers) |
| waveshare | 25     | 27      | Waveshare 2" LCD Module        |
| adafruit  | 24     | 25      | Adafruit ST7789 breakout       |

*All pin numbers use BOARD numbering (physical header pin positions)*

## Display Rotations

| Angle | Orientation              |
|-------|--------------------------|
| 0     | Portrait (default)       |
| 90    | Landscape                |
| 180   | Portrait (upside down)   |
| 270   | Landscape (upside down)  |

## Available Examples

| Script                    | Description                           |
|---------------------------|---------------------------------------|
| basic_colors.py           | Simple color cycling                  |
| basic_colors_demo.py      | Extended color demonstrations         |
| shapes_demo.py            | Geometric shapes and patterns         |
| text_demo.py              | Text rendering examples               |
| system_monitor_demo.py    | Real-time system stats dashboard      |
| st7789_unit_tests.py      | Comprehensive functionality tests     |

## Help

Every script supports `--help`:
```bash
python script_name.py --help
```
