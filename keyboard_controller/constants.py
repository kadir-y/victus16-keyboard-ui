"""
Constants and default configuration for the keyboard controller.
Includes sysfs paths, config file paths, and default color templates.
"""

import os

# ─── Sysfs Paths ───
LED_BASE = '/sys/class/leds/hp::kbd_backlight'
BRIGHTNESS_PATH = f'{LED_BASE}/brightness'
MAX_BRIGHTNESS_PATH = f'{LED_BASE}/max_brightness'
INTENSITY_PATH = f'{LED_BASE}/multi_intensity'

# ─── User Configuration Paths ───
CONFIG_DIR = os.path.expanduser('~/.config/victus16-keyboard')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'templates.json')
STATE_FILE = os.path.join(CONFIG_DIR, 'state.json')

# ─── Default Color Templates ───
DEFAULT_TEMPLATES = [
    {
        "name": "Day",
        "icon": "",
        "hue": 190,
        "sat": 0.1,
        "val": 1.0,
        "brightness": 255,
        "desc": "Bright clear daylight",
    },
    {
        "name": "Night",
        "icon": "",
        "hue": 220,
        "sat": 0.8,
        "val": 1.0,
        "brightness": 100,
        "desc": "Dim, easy on the eyes",
    },
    {
        "name": "Cyberpunk",
        "icon": "",
        "hue": 285,
        "sat": 0.9,
        "val": 1.0,
        "brightness": 200,
        "desc": "Vibrant neon purple",
    },
    {
        "name": "Ocean",
        "icon": "",
        "hue": 195,
        "sat": 0.9,
        "val": 1.0,
        "brightness": 180,
        "desc": "Deep aquatic blue",
    },
    {
        "name": "Lava",
        "icon": "",
        "hue": 5,
        "sat": 0.9,
        "val": 1.0,
        "brightness": 220,
        "desc": "Intense molten red",
    },
    {
        "name": "Off",
        "icon": "⏻",
        "hue": 0,
        "sat": 0.0,
        "val": 1.0,
        "brightness": 0,
        "desc": "Turn off backlight",
        "is_system": True,
    },
]
