"""
Hardware interface for the keyboard backlight.
Provides read/write access to sysfs files via sudo.
"""

import subprocess


def read_sysfs(path):
    """Read a sysfs file and return its stripped content, or None on failure."""
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except (IOError, OSError) as e:
        print(f"Error reading sysfs '{path}': {e}")
        return None


def write_sysfs(path, value):
    """Write a value to a sysfs file using sudo tee. Returns True on success."""
    try:
        proc = subprocess.run(
            ['sudo', '-n', 'tee', path],
            input=value.encode(),
            capture_output=True,
            timeout=5
        )
        return proc.returncode == 0
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Error writing sysfs '{path}': {e}")
        return False
