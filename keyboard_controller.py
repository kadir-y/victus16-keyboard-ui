#!/usr/bin/env python3
"""
HP Victus 16 Keyboard Backlight Controller
Entry point for the GTK4 application.
"""

import sys
import os

# Support running locally from source tree as well as from the installed package
local_pkg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keyboard_controller')
if os.path.exists(local_pkg):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
else:
    sys.path.insert(0, '/usr/lib/victus16-keyboard')

import argparse
from keyboard_controller.app import KeyboardControllerApp
from keyboard_controller.templates import load_state
from keyboard_controller.hardware import write_sysfs
from keyboard_controller.constants import BRIGHTNESS_PATH, INTENSITY_PATH

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HP Victus 16 Keyboard Backlight Controller")
    parser.add_argument('--restore', action='store_true', help="Restore the last applied keyboard state and exit")
    args, unknown = parser.parse_known_args()

    if args.restore:
        state = load_state()
        if state:
            r, g, b = state.get('r', 255), state.get('g', 255), state.get('b', 255)
            brightness = state.get('brightness', 128)
            write_sysfs(INTENSITY_PATH, f"{r} {g} {b}")
            write_sysfs(BRIGHTNESS_PATH, str(brightness))
            print("Keyboard state restored.")
        else:
            print("No saved state found to restore.")
        sys.exit(0)

    app = KeyboardControllerApp()
    app.run(sys.argv)
