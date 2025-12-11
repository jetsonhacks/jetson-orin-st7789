#!/usr/bin/env python3
"""
ST7789 System Monitor Demo
Real-time display of system stats with graphs and text
Combines shapes and text for a practical dashboard
"""

import sys
import time
import argparse
from PIL import Image, ImageDraw
import datetime

try:
    from jetson_orin_st7789 import ST7789
except ImportError:
    print("Error: jetson_orin_st7789 package not found.")
    print("Please install with: uv sync --extra dev")
    sys.exit(1)

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. Using simulated data.")
    print("Install with: uv add psutil")


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
        description='ST7789 System Monitor Demo',
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


class SystemMonitor:
    """System stats monitor with display rendering"""
    
    def __init__(self):
        self.cpu_history = []
        self.mem_history = []
        self.max_history = 50
        
    def get_stats(self):
        """Get current system stats"""
        if PSUTIL_AVAILABLE:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'cpu_temp': self._get_cpu_temp(),
                'mem_percent': psutil.virtual_memory().percent,
                'mem_used_gb': psutil.virtual_memory().used / (1024**3),
                'mem_total_gb': psutil.virtual_memory().total / (1024**3),
                'disk_percent': psutil.disk_usage('/').percent,
            }
        else:
            # Simulated data for demo
            import random
            return {
                'cpu_percent': random.uniform(20, 80),
                'cpu_temp': random.uniform(40, 60),
                'mem_percent': random.uniform(30, 70),
                'mem_used_gb': random.uniform(2, 6),
                'mem_total_gb': 8.0,
                'disk_percent': random.uniform(40, 60),
            }
    
    def _get_cpu_temp(self):
        """Get CPU temperature (Jetson-specific)"""
        try:
            # Try Jetson thermal zones
            with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') as f:
                return float(f.read().strip()) / 1000.0
        except:
            try:
                # Fallback to psutil
                temps = psutil.sensors_temperatures()
                if temps:
                    return list(temps.values())[0][0].current
            except:
                pass
        return 0.0
    
    def update_history(self, stats):
        """Update historical data"""
        self.cpu_history.append(stats['cpu_percent'])
        self.mem_history.append(stats['mem_percent'])
        
        if len(self.cpu_history) > self.max_history:
            self.cpu_history.pop(0)
        if len(self.mem_history) > self.max_history:
            self.mem_history.pop(0)
    
    def draw_header(self, draw, width):
        """Draw header bar"""
        draw.rectangle([0, 0, width, 30], fill=(50, 50, 80))
        draw.text((10, 8), "System Monitor", fill=(255, 255, 255))
        
        # Timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        bbox = draw.textbbox((0, 0), timestamp)
        ts_width = bbox[2] - bbox[0]
        draw.text((width - ts_width - 10, 8), timestamp, fill=(200, 200, 200))
    
    def draw_stat_bar(self, draw, x, y, width, height, value, max_value, 
                     label, color, show_text=True):
        """Draw a horizontal bar graph for a stat"""
        # Background
        draw.rectangle([x, y, x + width, y + height], 
                      outline=(100, 100, 100), width=1)
        
        # Fill
        fill_width = int((width - 2) * (value / max_value))
        if fill_width > 0:
            draw.rectangle([x + 1, y + 1, x + 1 + fill_width, y + height - 1],
                         fill=color)
        
        # Label
        if show_text:
            text = f"{label}: {value:.1f}%"
            draw.text((x + 5, y + (height - 10) // 2), text, fill=(255, 255, 255))
    
    def draw_gauge(self, draw, cx, cy, radius, value, max_value, 
                   label, color):
        """Draw a circular gauge"""
        # Outer circle
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                    outline=(100, 100, 100), width=2)
        
        # Value arc (pie slice)
        angle = int((value / max_value) * 360)
        if angle > 0:
            draw.pieslice([cx - radius + 2, cy - radius + 2,
                          cx + radius - 2, cy + radius - 2],
                         start=-90, end=-90 + angle, fill=color)
        
        # Center circle (to make it look like a gauge)
        inner_radius = radius - 8
        draw.ellipse([cx - inner_radius, cy - inner_radius,
                     cx + inner_radius, cy + inner_radius],
                    fill=(0, 0, 0))
        
        # Value text
        text = f"{value:.0f}%"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((cx - text_width // 2, cy - text_height // 2), 
                 text, fill=(255, 255, 255))
        
        # Label below gauge
        bbox = draw.textbbox((0, 0), label)
        label_width = bbox[2] - bbox[0]
        draw.text((cx - label_width // 2, cy + radius + 5), 
                 label, fill=(200, 200, 200))
    
    def draw_line_graph(self, draw, x, y, width, height, data, 
                       max_value, color, fill=False):
        """Draw a line graph"""
        if len(data) < 2:
            return
        
        # Background
        draw.rectangle([x, y, x + width, y + height], 
                      fill=(20, 20, 20), outline=(100, 100, 100), width=1)
        
        # Grid lines
        for i in range(5):
            grid_y = y + (height * i // 4)
            draw.line([x, grid_y, x + width, grid_y], 
                     fill=(40, 40, 40), width=1)
        
        # Calculate points
        points = []
        x_step = width / (len(data) - 1)
        for i, value in enumerate(data):
            px = x + i * x_step
            py = y + height - (height * value / max_value)
            points.append((px, py))
        
        # Draw filled area if requested
        if fill and len(points) > 0:
            polygon_points = [(x, y + height)] + points + [(x + width, y + height)]
            # Create semi-transparent fill effect with darker color
            fill_color = tuple(c // 3 for c in color)
            draw.polygon(polygon_points, fill=fill_color)
        
        # Draw line
        if len(points) > 1:
            draw.line(points, fill=color, width=2)
    
    def draw_text_stat(self, draw, x, y, label, value, unit, color):
        """Draw a text-based stat"""
        draw.text((x, y), label, fill=(180, 180, 180))
        text = f"{value:.1f}{unit}"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        draw.text((x + 150 - text_width, y), text, fill=color)
    
    def render_layout_1(self, draw, width, height, stats):
        """Layout 1: Bars and text"""
        y_pos = 40
        
        # CPU bar
        self.draw_stat_bar(draw, 10, y_pos, width - 20, 30, 
                          stats['cpu_percent'], 100, "CPU", (255, 100, 100))
        y_pos += 40
        
        # Memory bar
        self.draw_stat_bar(draw, 10, y_pos, width - 20, 30,
                          stats['mem_percent'], 100, "Memory", (100, 255, 100))
        y_pos += 40
        
        # Disk bar
        self.draw_stat_bar(draw, 10, y_pos, width - 20, 30,
                          stats['disk_percent'], 100, "Disk", (100, 100, 255))
        y_pos += 50
        
        # Additional stats
        self.draw_text_stat(draw, 10, y_pos, "CPU Temp:", 
                           stats['cpu_temp'], "°C", (255, 150, 100))
        y_pos += 25
        
        self.draw_text_stat(draw, 10, y_pos, "Memory Used:",
                           stats['mem_used_gb'], " GB", (150, 255, 150))
        y_pos += 25
        
        self.draw_text_stat(draw, 10, y_pos, "Memory Total:",
                           stats['mem_total_gb'], " GB", (150, 200, 255))
    
    def render_layout_2(self, draw, width, height, stats):
        """Layout 2: Circular gauges"""
        y_pos = 50
        
        # Three gauges in a row
        gauge_y = y_pos + 45
        gauge_radius = 40
        spacing = width // 3
        
        self.draw_gauge(draw, spacing // 2, gauge_y, gauge_radius,
                       stats['cpu_percent'], 100, "CPU", (255, 100, 100))
        
        self.draw_gauge(draw, spacing + spacing // 2, gauge_y, gauge_radius,
                       stats['mem_percent'], 100, "RAM", (100, 255, 100))
        
        self.draw_gauge(draw, 2 * spacing + spacing // 2, gauge_y, gauge_radius,
                       stats['disk_percent'], 100, "Disk", (100, 150, 255))
        
        # Stats below
        y_pos = gauge_y + gauge_radius + 35
        
        # Draw box for details
        draw.rectangle([10, y_pos, width - 10, y_pos + 80],
                      outline=(100, 100, 100), width=1)
        
        y_pos += 10
        self.draw_text_stat(draw, 20, y_pos, "Temperature:",
                           stats['cpu_temp'], "°C", (255, 200, 100))
        y_pos += 25
        
        self.draw_text_stat(draw, 20, y_pos, "Mem Used:",
                           stats['mem_used_gb'], " GB", (150, 255, 150))
        y_pos += 25
        
        self.draw_text_stat(draw, 20, y_pos, "Mem Total:",
                           stats['mem_total_gb'], " GB", (200, 200, 255))
    
    def render_layout_3(self, draw, width, height, stats):
        """Layout 3: Line graphs"""
        # CPU graph
        graph_height = 60
        y_pos = 40
        
        draw.text((10, y_pos), "CPU Usage History", fill=(255, 200, 200))
        y_pos += 15
        
        self.draw_line_graph(draw, 10, y_pos, width - 20, graph_height,
                            self.cpu_history, 100, (255, 100, 100), fill=True)
        
        # Current value
        draw.text((width - 60, y_pos + graph_height - 15),
                 f"{stats['cpu_percent']:.1f}%", fill=(255, 150, 150))
        
        # Memory graph
        y_pos += graph_height + 20
        draw.text((10, y_pos), "Memory Usage History", fill=(200, 255, 200))
        y_pos += 15
        
        self.draw_line_graph(draw, 10, y_pos, width - 20, graph_height,
                            self.mem_history, 100, (100, 255, 100), fill=True)
        
        # Current value
        draw.text((width - 60, y_pos + graph_height - 15),
                 f"{stats['mem_percent']:.1f}%", fill=(150, 255, 150))
        
        # Stats summary below
        y_pos += graph_height + 20
        draw.text((10, y_pos), f"Temp: {stats['cpu_temp']:.1f}°C", 
                 fill=(255, 200, 100))
        draw.text((10, y_pos + 20), 
                 f"Disk: {stats['disk_percent']:.1f}%", fill=(150, 150, 255))



def main():
    """Main entry point for system monitor demo"""
    args = parse_arguments()
    
    # Handle legacy positional argument
    if args.legacy_rotation is not None:
        if args.legacy_rotation not in [0, 90, 180, 270]:
            print(f"Invalid rotation: {args.legacy_rotation}. Must be 0, 90, 180, or 270")
            sys.exit(1)
        args.rotation = args.legacy_rotation
    
    # Get wiring configuration
    wiring = WIRING_PRESETS[args.wiring]
    
    print("ST7789 System Monitor Demo")
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
    
    if not PSUTIL_AVAILABLE:
        print("\nUsing simulated data (psutil not installed)")
    
    print("\nDisplaying system stats. Press Ctrl+C to exit.\n")
    
    monitor = SystemMonitor()
    layout = 0
    layouts = ["Bars", "Gauges", "Graphs"]
    update_interval = 1.0  # seconds
    layout_switch_time = 10  # seconds between layout changes
    
    try:
        last_update = time.time()
        last_layout_switch = time.time()
        
        while True:
            current_time = time.time()
            
            # Get stats
            stats = monitor.get_stats()
            monitor.update_history(stats)
            
            # Switch layout periodically
            if current_time - last_layout_switch >= layout_switch_time:
                layout = (layout + 1) % 3
                last_layout_switch = current_time
                print(f"Switching to layout: {layouts[layout]}")
            
            # Create canvas
            image = Image.new('RGB', (display.width, display.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw header
            monitor.draw_header(draw, display.width)
            
            # Draw appropriate layout
            if layout == 0:
                monitor.render_layout_1(draw, display.width, display.height, stats)
            elif layout == 1:
                monitor.render_layout_2(draw, display.width, display.height, stats)
            else:
                monitor.render_layout_3(draw, display.width, display.height, stats)
            
            # Display
            display.display(image)
            
            # Wait for next update
            elapsed = time.time() - last_update
            if elapsed < update_interval:
                time.sleep(update_interval - elapsed)
            last_update = time.time()
                
    except KeyboardInterrupt:
        print("\n\nMonitor interrupted by user")
    finally:
        print("Cleaning up...")
        display.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()
