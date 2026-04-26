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

from keyboard_controller.app import KeyboardControllerApp

if __name__ == '__main__':
    app = KeyboardControllerApp()
    app.run(None)
