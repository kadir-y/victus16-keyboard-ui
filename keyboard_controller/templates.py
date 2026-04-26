"""
Template management for the keyboard controller.
Handles loading and saving color templates from/to the user config file.
"""

import os
import json

from .constants import CONFIG_DIR, CONFIG_FILE, DEFAULT_TEMPLATES, STATE_FILE


def load_templates():
    """Load templates from the config file, falling back to defaults."""
    templates = []

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                templates = json.load(f)
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error loading templates: {e}")

    if not templates:
        templates = [t.copy() for t in DEFAULT_TEMPLATES]

    # Ensure system templates always exist in user's saved templates
    system_templates = [t for t in DEFAULT_TEMPLATES if t.get('is_system')]
    for sys_tmpl in system_templates:
        if not any(t.get('name') == sys_tmpl['name'] for t in templates):
            templates.append(sys_tmpl.copy())

    return templates


def save_templates(templates):
    """Persist templates to the config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=4, ensure_ascii=False)
    except (IOError, OSError) as e:
        print(f"Error saving templates: {e}")


def save_state(r, g, b, brightness):
    """Save the last applied color and brightness state."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    state = {
        'r': r,
        'g': g,
        'b': b,
        'brightness': brightness
    }
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4)
    except (IOError, OSError) as e:
        print(f"Error saving state: {e}")


def load_state():
    """Load the last applied color and brightness state."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error loading state: {e}")
    return None
