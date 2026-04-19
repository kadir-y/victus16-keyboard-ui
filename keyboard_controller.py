#!/usr/bin/env python3
"""
HP Victus 16 Keyboard Backlight Controller
Native GTK4 app for controlling keyboard RGB colors and brightness.
"""

import subprocess
import gi
import math
import colorsys
import os
import json
import cairo

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Gio, Graphene

# ─── Sysfs Paths ───
LED_BASE = '/sys/class/leds/hp::kbd_backlight'
BRIGHTNESS_PATH = f'{LED_BASE}/brightness'
MAX_BRIGHTNESS_PATH = f'{LED_BASE}/max_brightness'
INTENSITY_PATH = f'{LED_BASE}/multi_intensity'

CONFIG_DIR = os.path.expanduser('~/.config/victus16-keyboard')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'templates.json')

# ─── Color Templates ───
DEFAULT_TEMPLATES = [
    {"name": "Day",       "icon": "", "hue": 190, "sat": 0.1, "val": 1.0, "brightness": 255, "desc": "Bright clear daylight"},
    {"name": "Night",     "icon": "", "hue": 220, "sat": 0.8, "val": 1.0, "brightness": 100, "desc": "Dim, easy on the eyes"},
    {"name": "Cyberpunk", "icon": "", "hue": 285, "sat": 0.9, "val": 1.0, "brightness": 200, "desc": "Vibrant neon purple"},
    {"name": "Ocean",     "icon": "", "hue": 195, "sat": 0.9, "val": 1.0, "brightness": 180, "desc": "Deep aquatic blue"},
    {"name": "Lava",      "icon": "", "hue": 5,   "sat": 0.9, "val": 1.0, "brightness": 220, "desc": "Intense molten red"},
]
def load_templates():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading templates: {e}")
    return DEFAULT_TEMPLATES.copy()

def save_templates(templates):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving templates: {e}")


CSS = """
window {
    background-color: #121212;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.main-box {
    padding: 32px 28px;
}
.app-title {
    font-size: 24px;
    font-weight: 500;
    color: #ffffff;
    margin-bottom: 2px;
    letter-spacing: -0.5px;
}
.app-subtitle {
    font-size: 13px;
    font-weight: 400;
    color: #888888;
    margin-bottom: 24px;
    letter-spacing: 0.2px;
}
.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #999999;
    margin-bottom: 12px;
    margin-top: 12px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.card {
    background-color: #1a1a1a;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.03);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* ── Template Cards ── */
.template-btn {
    background-color: #222222;
    border-radius: 8px;
    padding: 12px 14px;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 250ms ease;
    min-width: 100px;
}
.template-btn:hover {
    border-color: rgba(255,255,255,0.15);
    background-color: #282828;
}
.template-btn.active {
    border-color: #4a90e2;
    background-color: rgba(74, 144, 226, 0.05);
}
.template-icon {
    font-size: 18px;
}
.template-name {
    font-size: 13px;
    font-weight: 500;
    color: #eeeeee;
    margin-top: 4px;
}
.template-desc {
    font-size: 11px;
    font-weight: 400;
    color: #777777;
    margin-top: 2px;
}

/* ── Template Adjustments ── */
.adjust-card {
    background-color: #1a1a1a;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.03);
}
.adjust-label {
    font-size: 12px;
    font-weight: 500;
    color: #aaaaaa;
    margin-bottom: 2px;
}
.adjust-value {
    font-size: 12px;
    font-weight: 500;
    color: #cccccc;
}
.hue-scale trough {
    border-radius: 4px;
    min-height: 4px;
}
.hue-scale highlight {
    border-radius: 4px;
    min-height: 4px;
    background: transparent;
}
.hue-scale slider {
    background-color: #ffffff;
    border-radius: 50%;
    min-width: 16px;
    min-height: 16px;
    margin: 0;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
    transition: transform 150ms ease;
}
.hue-scale slider:hover {
    transform: scale(1.15);
}
.sat-scale trough {
    background-color: #222222;
    border-radius: 4px;
    min-height: 4px;
}
.sat-scale highlight {
    border-radius: 4px;
    min-height: 4px;
}
.sat-scale slider {
    background-color: #ffffff;
    border-radius: 50%;
    min-width: 16px;
    min-height: 16px;
    margin: 0;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
    transition: transform 150ms ease;
}
.sat-scale slider:hover {
    transform: scale(1.15);
}

.brightness-scale trough {
    background-color: #222222;
    border-radius: 4px;
    min-height: 4px;
}
.brightness-scale highlight {
    background: #4a90e2;
    border-radius: 4px;
    min-height: 4px;
}
.brightness-scale slider {
    background-color: #ffffff;
    border-radius: 50%;
    min-width: 16px;
    min-height: 16px;
    margin: 0;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
    transition: transform 150ms ease;
}
.brightness-scale slider:hover {
    transform: scale(1.15);
}
.brightness-label {
    font-size: 24px;
    font-weight: 300;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.brightness-pct {
    font-size: 14px;
    font-weight: 400;
    color: #666;
}
.color-label {
    font-size: 12px;
    font-weight: 500;
    color: #888888;
    margin-top: 8px;
    letter-spacing: 0.5px;
}
.off-btn {
    background-color: transparent;
    color: #888888;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 500;
    font-size: 13px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 250ms ease;
}
.off-btn:hover {
    background-color: rgba(255,255,255,0.05);
    color: #ffffff;
}

.preview-area {
    border-radius: 4px;
    min-height: 4px;
    margin-top: 12px;
    margin-bottom: 24px;
    transition: all 300ms ease;
    opacity: 0.8;
}
.status-text {
    font-size: 12px;
    color: #666666;
    margin-top: 12px;
}
.rgb-input {
    background-color: #222222;
    color: #e0e0e0;
    border-radius: 6px;
    padding: 6px 10px;
    border: 1px solid rgba(255,255,255,0.05);
    min-width: 50px;
    font-size: 12px;
}
.rgb-input:focus {
    border-color: #4a90e2;
}
.rgb-label {
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 6px;
    text-transform: uppercase;
}
.rgb-label-r { color: #ff5e5e; }
.rgb-label-g { color: #4bcf66; }
.rgb-label-b { color: #4a90e2; }
.color-swatch {
    border-radius: 50%;
    min-width: 20px;
    min-height: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
"""


def read_sysfs(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return None


def write_sysfs(path, value):
    try:
        proc = subprocess.run(
            ['sudo', '-n', 'tee', path],
            input=value.encode(),
            capture_output=True,
            timeout=5
        )
        return proc.returncode == 0
    except:
        return False


class ColorWheelWidget(Gtk.DrawingArea):
    """Custom color wheel drawn with Cairo."""

    def __init__(self, on_color_picked):
        super().__init__()
        self.on_color_picked = on_color_picked
        self.set_size_request(220, 220)
        self.set_draw_func(self._draw)
        self._selected_hue = 0
        self._selected_sat = 1.0

        click = Gtk.GestureClick()
        click.connect('pressed', self._on_click)
        self.add_controller(click)

        drag = Gtk.GestureDrag()
        drag.connect('drag-begin', self._on_drag_begin)
        drag.connect('drag-update', self._on_drag_update)
        self.add_controller(drag)

    def _pick_at(self, x, y):
        w = self.get_width()
        h = self.get_height()
        cx, cy = w / 2, h / 2
        radius = min(cx, cy) - 8
        dx, dy = x - cx, y - cy
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > radius:
            dist = radius
        angle = math.atan2(dy, dx)
        self._selected_hue = (math.degrees(angle) + 360) % 360
        self._selected_sat = dist / radius
        self.queue_draw()
        r, g, b = self._hsv_to_rgb(self._selected_hue / 360, self._selected_sat, 1.0)
        self.on_color_picked(int(r * 255), int(g * 255), int(b * 255))

    def _on_click(self, gesture, n, x, y):
        self._pick_at(x, y)

    def _on_drag_begin(self, gesture, x, y):
        self._drag_start_x = x
        self._drag_start_y = y
        self._pick_at(x, y)

    def _on_drag_update(self, gesture, off_x, off_y):
        self._pick_at(self._drag_start_x + off_x, self._drag_start_y + off_y)

    @staticmethod
    def _hsv_to_rgb(h, s, v):

        return colorsys.hsv_to_rgb(h, s, v)

    def set_color(self, r, g, b):

        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self._selected_hue = h * 360
        self._selected_sat = s
        self.queue_draw()

    def _draw(self, area, cr, width, height):
        cx, cy = width / 2, height / 2
        radius = min(cx, cy) - 8

        # Draw color wheel
        steps = 360
        for i in range(steps):
            angle1 = math.radians(i)
            angle2 = math.radians(i + 1.5)
            for j in range(0, int(radius), 2):
                sat = j / radius
                r, g, b = self._hsv_to_rgb(i / 360, sat, 1.0)
                cr.set_source_rgb(r, g, b)
                x = cx + j * math.cos(angle1)
                y = cy + j * math.sin(angle1)
                cr.rectangle(x - 1, y - 1, 3, 3)
                cr.fill()

        # Draw selector circle
        sel_dist = self._selected_sat * radius
        sel_x = cx + sel_dist * math.cos(math.radians(self._selected_hue))
        sel_y = cy + sel_dist * math.sin(math.radians(self._selected_hue))

        cr.set_source_rgb(1, 1, 1)
        cr.arc(sel_x, sel_y, 8, 0, 2 * math.pi)
        cr.set_line_width(2.5)
        cr.stroke()

        r, g, b = self._hsv_to_rgb(self._selected_hue / 360, self._selected_sat, 1.0)
        cr.set_source_rgb(r, g, b)
        cr.arc(sel_x, sel_y, 5.5, 0, 2 * math.pi)
        cr.fill()


class KeyboardControllerApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.victus16.keyboard',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.current_r = 255
        self.current_g = 255
        self.current_b = 255
        self.current_brightness = 128
        self.active_template_btn = None
        self.active_template = None
        self._adjusting = False  # Flag to prevent loops
        self.templates = load_templates()
        
    def do_activate(self):
        # Load CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Window
        self.win = Gtk.ApplicationWindow(application=self)
        self.win.set_title("Victus 16 Keyboard")
        self.win.set_default_size(480, 720)
        self.win.set_resizable(True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.win.set_child(scroll)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.add_css_class('main-box')
        scroll.set_child(main_box)

        # ─── Header ───
        title = Gtk.Label(label="Victus 16 Keyboard")
        title.add_css_class('app-title')
        title.set_halign(Gtk.Align.START)
        main_box.append(title)

        subtitle = Gtk.Label(label="RGB Backlight Controller")
        subtitle.add_css_class('app-subtitle')
        subtitle.set_halign(Gtk.Align.START)
        main_box.append(subtitle)

        # ─── Preview Bar ───
        self.preview = Gtk.Box()
        self.preview.add_css_class('preview-area')
        self.preview.set_size_request(-1, 8)
        main_box.append(self.preview)

        # ─── Responsive Content Grid ───
        content_flow = Gtk.FlowBox()
        content_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        content_flow.set_max_children_per_line(2)
        content_flow.set_min_children_per_line(1)
        content_flow.set_column_spacing(16)
        content_flow.set_row_spacing(16)
        content_flow.set_homogeneous(False)
        content_flow.set_valign(Gtk.Align.START)
        main_box.append(content_flow)

        left_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_col.set_valign(Gtk.Align.START)
        right_col.set_valign(Gtk.Align.START)
        # FlowBox child elements need to expand to fill the homogeneous cell
        left_col.set_hexpand(True)
        right_col.set_hexpand(True)
        left_col.set_size_request(300, -1)
        right_col.set_size_request(300, -1)
        content_flow.append(left_col)
        content_flow.append(right_col)

        # ─── Brightness Card ───
        bright_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bright_card.add_css_class('card')
        left_col.append(bright_card)

        bright_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        bright_header.set_spacing(8)
        bright_card.append(bright_header)

        bl = Gtk.Label(label="Brightness")
        bl.add_css_class('section-title')
        bl.set_halign(Gtk.Align.START)
        bl.set_hexpand(True)
        bright_header.append(bl)

        self.brightness_value_label = Gtk.Label(label="50%")
        self.brightness_value_label.add_css_class('brightness-label')
        bright_header.append(self.brightness_value_label)

        self.brightness_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 0, 255, 1)
        self.brightness_scale.set_value(128)
        self.brightness_scale.set_draw_value(False)
        self.brightness_scale.add_css_class('brightness-scale')
        self.brightness_scale.set_hexpand(True)
        self.brightness_scale.set_margin_top(10)
        self.brightness_scale.connect('value-changed', self._on_brightness_changed)
        bright_card.append(self.brightness_scale)

        # ─── Color Wheel Card ───
        wheel_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        wheel_card.add_css_class('card')
        left_col.append(wheel_card)

        wl = Gtk.Label(label="Color Wheel")
        wl.add_css_class('section-title')
        wl.set_halign(Gtk.Align.START)
        wheel_card.append(wl)

        self.color_wheel = ColorWheelWidget(self._on_wheel_color)
        self.color_wheel.set_halign(Gtk.Align.CENTER)
        self.color_wheel.set_margin_top(8)
        wheel_card.append(self.color_wheel)

        # RGB Inputs
        rgb_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        rgb_box.set_halign(Gtk.Align.CENTER)
        rgb_box.set_margin_top(14)
        wheel_card.append(rgb_box)

        self.r_entry, self.g_entry, self.b_entry = (
            self._make_rgb_input("R", "rgb-label-r"),
            self._make_rgb_input("G", "rgb-label-g"),
            self._make_rgb_input("B", "rgb-label-b"),
        )
        for box, _ in [self.r_entry, self.g_entry, self.b_entry]:
            rgb_box.append(box)



        # ─── Templates Card ───
        template_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        template_card.add_css_class('card')
        right_col.append(template_card)

        pl = Gtk.Label(label="Color Templates")
        pl.add_css_class('section-title')
        pl.set_halign(Gtk.Align.START)
        template_card.append(pl)

        self.template_grid = Gtk.FlowBox()
        self.template_grid.set_max_children_per_line(4)
        self.template_grid.set_min_children_per_line(2)
        self.template_grid.set_row_spacing(8)
        self.template_grid.set_column_spacing(8)
        self.template_grid.set_homogeneous(True)
        self.template_grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.template_grid.set_margin_top(8)
        template_card.append(self.template_grid)

        self.template_buttons = []
        self._refresh_template_grid()

        # Actions for templates
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        action_box.set_halign(Gtk.Align.CENTER)
        action_box.set_margin_top(10)
        
        self.btn_save_new = Gtk.Button(label="Save as New")
        self.btn_save_new.connect('clicked', self._on_save_new_template_dialog)
        action_box.append(self.btn_save_new)
        
        self.btn_update = Gtk.Button(label="Update Selected")
        self.btn_update.connect('clicked', self._on_update_template)
        action_box.append(self.btn_update)
        
        self.btn_delete = Gtk.Button(label="Delete Selected")
        self.btn_delete.connect('clicked', self._on_delete_template)
        action_box.append(self.btn_delete)
        
        template_card.append(action_box)

        # ─── New Template Revealer ───
        self.new_tmpl_revealer = Gtk.Revealer()
        new_tmpl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        new_tmpl_box.set_margin_top(10)
        new_tmpl_box.set_halign(Gtk.Align.CENTER)
        
        self.tmpl_name_entry = Gtk.Entry(placeholder_text="Template Name")
        new_tmpl_box.append(self.tmpl_name_entry)
        
        self.tmpl_icon_entry = Gtk.Entry(placeholder_text="Icon")
        self.tmpl_icon_entry.set_max_length(2)
        self.tmpl_icon_entry.set_width_chars(4)
        new_tmpl_box.append(self.tmpl_icon_entry)
        
        self.tmpl_desc_entry = Gtk.Entry(placeholder_text="Description")
        new_tmpl_box.append(self.tmpl_desc_entry)
        
        confirm_btn = Gtk.Button(label="Save")
        confirm_btn.connect('clicked', self._confirm_save_new_template)
        new_tmpl_box.append(confirm_btn)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect('clicked', lambda b: self.new_tmpl_revealer.set_reveal_child(False))
        new_tmpl_box.append(cancel_btn)
        
        self.new_tmpl_revealer.set_child(new_tmpl_box)
        template_card.append(self.new_tmpl_revealer)

        # ─── Template Adjustment Sliders ───
        self.adjust_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.adjust_card.add_css_class('adjust-card')
        right_col.append(self.adjust_card)

        adj_title = Gtk.Label(label="Template Adjustments")
        adj_title.add_css_class('section-title')
        adj_title.set_halign(Gtk.Align.START)
        self.adjust_card.append(adj_title)

        self.adjust_info_label = Gtk.Label(label="Select a template")
        self.adjust_info_label.add_css_class('adjust-label')
        self.adjust_info_label.set_halign(Gtk.Align.START)
        self.adjust_card.append(self.adjust_info_label)

        # Hue slider
        hue_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hue_row.set_margin_top(6)
        hl = Gtk.Label(label="Hue")
        hl.add_css_class('adjust-label')
        hl.set_hexpand(False)
        hl.set_size_request(80, -1)
        hue_row.append(hl)
        self.hue_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 360, 1)
        self.hue_scale.set_value(0)
        self.hue_scale.set_draw_value(False)
        self.hue_scale.add_css_class('hue-scale')
        self.hue_scale.set_hexpand(True)
        self.hue_scale.connect('value-changed', self._on_adjust_changed)
        hue_row.append(self.hue_scale)
        self.hue_value_label = Gtk.Label(label="0°")
        self.hue_value_label.add_css_class('adjust-value')
        self.hue_value_label.set_size_request(40, -1)
        hue_row.append(self.hue_value_label)
        self.adjust_card.append(hue_row)

        # Update hue slider trough with rainbow gradient
        hue_trough_css = Gtk.CssProvider()
        hue_trough_css.load_from_data(
            ".hue-scale trough { background: linear-gradient(to right, "
            "hsl(0,100%,50%), hsl(60,100%,50%), hsl(120,100%,50%), "
            "hsl(180,100%,50%), hsl(240,100%,50%), hsl(300,100%,50%), hsl(360,100%,50%)); }".encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), hue_trough_css,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Saturation slider
        sat_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sl = Gtk.Label(label="Saturation")
        sl.add_css_class('adjust-label')
        sl.set_hexpand(False)
        sl.set_size_request(80, -1)
        sat_row.append(sl)
        self.sat_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.sat_scale.set_value(100)
        self.sat_scale.set_draw_value(False)
        self.sat_scale.add_css_class('sat-scale')
        self.sat_scale.set_hexpand(True)
        self.sat_scale.connect('value-changed', self._on_adjust_changed)
        sat_row.append(self.sat_scale)
        self.sat_value_label = Gtk.Label(label="100%")
        self.sat_value_label.add_css_class('adjust-value')
        self.sat_value_label.set_size_request(40, -1)
        sat_row.append(self.sat_value_label)
        self.adjust_card.append(sat_row)

        # Template brightness slider
        tbright_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        tbl = Gtk.Label(label="Brightness")
        tbl.add_css_class('adjust-label')
        tbl.set_hexpand(False)
        tbl.set_size_request(80, -1)
        tbright_row.append(tbl)
        self.tmpl_brightness_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 255, 1)
        self.tmpl_brightness_scale.set_value(180)
        self.tmpl_brightness_scale.set_draw_value(False)
        self.tmpl_brightness_scale.add_css_class('brightness-scale')
        self.tmpl_brightness_scale.set_hexpand(True)
        self.tmpl_brightness_scale.connect('value-changed', self._on_tmpl_brightness_changed)
        tbright_row.append(self.tmpl_brightness_scale)
        self.tmpl_bright_value_label = Gtk.Label(label="70%")
        self.tmpl_bright_value_label.add_css_class('adjust-value')
        self.tmpl_bright_value_label.set_size_request(40, -1)
        tbright_row.append(self.tmpl_bright_value_label)
        self.adjust_card.append(tbright_row)

        # ─── Hex Input ───
        hex_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hex_card.add_css_class('card')
        left_col.append(hex_card)

        hex_label = Gtk.Label(label="HEX")
        hex_label.add_css_class('section-title')
        hex_card.append(hex_label)

        self.hex_entry = Gtk.Entry()
        self.hex_entry.set_placeholder_text("#FF00FF")
        self.hex_entry.add_css_class('rgb-input')
        self.hex_entry.set_hexpand(True)
        self.hex_entry.set_max_length(7)
        self.hex_entry.connect('activate', self._on_hex_apply)
        hex_card.append(self.hex_entry)

        # ─── Current Color Info ───
        self.color_info_label = Gtk.Label(label="")
        self.color_info_label.add_css_class('color-label')
        self.color_info_label.set_halign(Gtk.Align.CENTER)
        main_box.append(self.color_info_label)

        # ─── Off Button ───
        off_btn = Gtk.Button(label="Turn Off Backlight")
        off_btn.add_css_class('off-btn')
        off_btn.set_halign(Gtk.Align.CENTER)
        off_btn.set_margin_top(10)
        off_btn.set_margin_bottom(20)
        off_btn.connect('clicked', self._on_off)
        main_box.append(off_btn)

        # ─── Status ───
        self.status_label = Gtk.Label(label="")
        self.status_label.add_css_class('status-text')
        self.status_label.set_halign(Gtk.Align.CENTER)
        main_box.append(self.status_label)

        # Load current state
        self._load_current_state()
        self.win.present()

    def _make_rgb_input(self, label_text, css_class):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl = Gtk.Label(label=label_text)
        lbl.add_css_class('rgb-label')
        lbl.add_css_class(css_class)
        box.append(lbl)
        entry = Gtk.Entry()
        entry.add_css_class('rgb-input')
        entry.set_max_length(3)
        entry.set_text("255")
        entry.set_alignment(0.5)
        entry.connect('activate', self._on_rgb_entry_activate)
        box.append(entry)
        return box, entry

    def _load_current_state(self):
        brightness = read_sysfs(BRIGHTNESS_PATH)
        intensity = read_sysfs(INTENSITY_PATH)

        if brightness:
            self.current_brightness = int(brightness)
            self.brightness_scale.set_value(self.current_brightness)

        if intensity:
            parts = intensity.split()
            self.current_r, self.current_g, self.current_b = (
                int(parts[0]), int(parts[1]), int(parts[2]))

        self._update_ui_color()
        self._update_status("Current settings loaded")

    def _update_ui_color(self):
        r, g, b = self.current_r, self.current_g, self.current_b

        # Update preview bar
        css_p = Gtk.CssProvider()
        css_p.load_from_data(
            f".preview-area {{ background: linear-gradient(90deg, "
            f"rgb({r},{g},{b}), rgba({r},{g},{b},0.3)); }}".encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_p,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Update RGB entries
        self.r_entry[1].set_text(str(r))
        self.g_entry[1].set_text(str(g))
        self.b_entry[1].set_text(str(b))

        # Update hex
        self.hex_entry.set_text(f"#{r:02X}{g:02X}{b:02X}")

        # Update color wheel
        self.color_wheel.set_color(r, g, b)

        # Update info label
        self.color_info_label.set_text(
            f"RGB({r}, {g}, {b})  •  #{r:02X}{g:02X}{b:02X}")

    def _update_status(self, msg):
        self.status_label.set_text(msg)
        GLib.timeout_add(3000, lambda: self.status_label.set_text(""))

    def _apply_color(self, r, g, b):
        self.current_r, self.current_g, self.current_b = r, g, b
        ok = write_sysfs(INTENSITY_PATH, f"{r} {g} {b}")
        self._update_ui_color()
        if ok:
            self._update_status(f"Color set: RGB({r}, {g}, {b})")
        else:
            self._update_status("⚠ Could not set color! Check sudo permissions.")

    def _on_brightness_changed(self, scale):
        val = int(scale.get_value())
        pct = int(val / 255 * 100)
        self.brightness_value_label.set_text(f"{pct}%")
        self.current_brightness = val

        # Sync template brightness slider
        if not self._adjusting:
            self._adjusting = True
            self.tmpl_brightness_scale.set_value(val)
            self.tmpl_bright_value_label.set_text(f"{pct}%")
            self._adjusting = False

        if not hasattr(self, '_bright_timeout_id'):
            self._bright_timeout_id = None
        if self._bright_timeout_id:
            GLib.source_remove(self._bright_timeout_id)
        self._bright_timeout_id = GLib.timeout_add(100, self._apply_brightness, val)

    def _apply_brightness(self, val):
        self._bright_timeout_id = None
        ok = write_sysfs(BRIGHTNESS_PATH, str(val))
        if ok:
            self._update_status(f"Brightness: {int(val/255*100)}%")
        else:
            self._update_status("⚠ Could not set brightness!")
        return False

    def _refresh_template_grid(self):
        # Remove all existing children
        child = self.template_grid.get_first_child()
        while child is not None:
            next_child = child.get_next_sibling()
            self.template_grid.remove(child)
            child = next_child

        self.template_buttons.clear()

        for tmpl in self.templates:
            btn = Gtk.Button()
            btn.add_css_class('template-btn')

            btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            btn_box.set_halign(Gtk.Align.CENTER)

            top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            top_row.set_halign(Gtk.Align.CENTER)

            tr, tg, tb = colorsys.hsv_to_rgb(tmpl['hue'] / 360, tmpl['sat'], tmpl['val'])
            swatch = Gtk.Box()
            swatch.add_css_class('color-swatch')
            swatch.set_size_request(28, 28)
            swatch_css = Gtk.CssProvider()
            # Use unique class for each color
            swatch_class = f"swatch-{abs(hash(tmpl['name']))}"
            swatch_css.load_from_data(
                f".{swatch_class} {{ background-color: rgb({int(tr*255)},{int(tg*255)},{int(tb*255)}); }}"
                .encode())
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(), swatch_css,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            swatch.add_css_class(swatch_class)
            top_row.append(swatch)

            icon_label = Gtk.Label(label=tmpl['icon'])
            icon_label.add_css_class('template-icon')
            top_row.append(icon_label)
            btn_box.append(top_row)

            name_label = Gtk.Label(label=tmpl['name'])
            name_label.add_css_class('template-name')
            btn_box.append(name_label)

            desc_label = Gtk.Label(label=tmpl['desc'])
            desc_label.add_css_class('template-desc')
            desc_label.set_wrap(True)
            desc_label.set_max_width_chars(14)
            btn_box.append(desc_label)

            btn.set_child(btn_box)
            btn.set_tooltip_text(f"{tmpl['name']} - {tmpl['desc']}")
            btn.connect('clicked', self._on_template_clicked, tmpl)
            self.template_grid.append(btn)
            self.template_buttons.append(btn)

        if self.active_template:
            # Try to re-select if active template is still there
            for btn, tmpl in zip(self.template_buttons, self.templates):
                if tmpl == self.active_template:
                    btn.add_css_class('active')

    def _on_save_new_template_dialog(self, btn):
        self.new_tmpl_revealer.set_reveal_child(not self.new_tmpl_revealer.get_reveal_child())

    def _confirm_save_new_template(self, btn):
        name = self.tmpl_name_entry.get_text().strip()
        icon = self.tmpl_icon_entry.get_text().strip() or "✨"
        desc = self.tmpl_desc_entry.get_text().strip()
        if name:
            new_tmpl = {
                "name": name,
                "icon": icon,
                "hue": self.hue_scale.get_value(),
                "sat": self.sat_scale.get_value() / 100.0,
                "val": self.active_template['val'] if self.active_template else 1.0,
                "brightness": int(self.tmpl_brightness_scale.get_value()),
                "desc": desc
            }
            self.templates.append(new_tmpl)
            save_templates(self.templates)
            self._refresh_template_grid()
            self._update_status(f"Template '{name}' saved.")
            self.new_tmpl_revealer.set_reveal_child(False)
            self.tmpl_name_entry.set_text("")
            self.tmpl_icon_entry.set_text("")
            self.tmpl_desc_entry.set_text("")
        else:
            self._update_status("⚠ Template name cannot be empty!")

    def _on_update_template(self, btn):
        if self.active_template and self.active_template in self.templates:
            self.active_template['hue'] = self.hue_scale.get_value()
            self.active_template['sat'] = self.sat_scale.get_value() / 100.0
            self.active_template['brightness'] = int(self.tmpl_brightness_scale.get_value())
            save_templates(self.templates)
            self._refresh_template_grid()
            self._update_status(f"Template '{self.active_template['name']}' updated.")
        else:
            self._update_status("⚠ Please select a template to update.")

    def _on_delete_template(self, btn):
        if self.active_template and self.active_template in self.templates:
            name = self.active_template['name']
            self.templates.remove(self.active_template)
            self.active_template = None
            save_templates(self.templates)
            self._refresh_template_grid()
            self._update_status(f"Template '{name}' deleted.")
        else:
            self._update_status("⚠ Please select a template to delete.")

    def _on_template_clicked(self, btn, tmpl):

        # Update active state visually
        for tb in self.template_buttons:
            tb.remove_css_class('active')
        btn.add_css_class('active')
        self.active_template = tmpl

        # Set adjustment sliders from template values
        self._adjusting = True
        self.hue_scale.set_value(tmpl['hue'])
        self.sat_scale.set_value(tmpl['sat'] * 100)
        self.tmpl_brightness_scale.set_value(tmpl['brightness'])
        self._adjusting = False

        # Update adjustment info
        self.adjust_info_label.set_text(f"{tmpl['icon']}  {tmpl['name']} — {tmpl['desc']}")

        # Apply color + brightness
        r, g, b = colorsys.hsv_to_rgb(tmpl['hue'] / 360, tmpl['sat'], tmpl['val'])
        self._apply_color(int(r * 255), int(g * 255), int(b * 255))

        # Also set brightness
        self.brightness_scale.set_value(tmpl['brightness'])

        # Update saturation slider gradient
        self._update_sat_slider_gradient(tmpl['hue'])

    def _on_adjust_changed(self, scale):
        """Called when hue or saturation sliders are changed."""

        if self._adjusting:
            return

        hue = self.hue_scale.get_value()
        sat = self.sat_scale.get_value() / 100.0
        val = self.active_template['val'] if self.active_template else 1.0

        self.hue_value_label.set_text(f"{int(hue)}°")
        self.sat_value_label.set_text(f"{int(sat * 100)}%")

        r, g, b = colorsys.hsv_to_rgb(hue / 360, sat, val)
        self._apply_color(int(r * 255), int(g * 255), int(b * 255))

        # Update saturation slider gradient to match hue
        self._update_sat_slider_gradient(hue)

    def _on_tmpl_brightness_changed(self, scale):
        """Called when the template brightness slider is changed."""
        if self._adjusting:
            return
        val = int(scale.get_value())
        pct = int(val / 255 * 100)
        self.tmpl_bright_value_label.set_text(f"{pct}%")
        # Sync main brightness
        self.brightness_scale.set_value(val)

    def _update_sat_slider_gradient(self, hue):
        """Update saturation slider trough to show white→full color gradient."""

        r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
        ri, gi, bi = int(r * 255), int(g * 255), int(b * 255)
        sat_css = Gtk.CssProvider()
        sat_css.load_from_data(
            f".sat-scale trough {{ background: linear-gradient(to right, "
            f"rgb(255,255,255), rgb({ri},{gi},{bi})); }}".encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), sat_css,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def _on_wheel_color(self, r, g, b):

        for tb in self.template_buttons:
            tb.remove_css_class('active')
        self.active_template = None
        self.adjust_info_label.set_text("Selected from Color Wheel")

        # Update hue/sat sliders to match wheel selection
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self._adjusting = True
        self.hue_scale.set_value(h * 360)
        self.sat_scale.set_value(s * 100)
        self.hue_value_label.set_text(f"{int(h * 360)}°")
        self.sat_value_label.set_text(f"{int(s * 100)}%")
        self._adjusting = False
        self._update_sat_slider_gradient(h * 360)

        self._apply_color(r, g, b)

    def _on_rgb_entry_activate(self, entry):
        try:
            r = max(0, min(255, int(self.r_entry[1].get_text())))
            g = max(0, min(255, int(self.g_entry[1].get_text())))
            b = max(0, min(255, int(self.b_entry[1].get_text())))
            self._apply_color(r, g, b)
        except ValueError:
            self._update_status("⚠ Invalid RGB value!")

    def _on_hex_apply(self, *args):
        hex_text = self.hex_entry.get_text().strip().lstrip('#')
        try:
            if len(hex_text) == 6:
                r = int(hex_text[0:2], 16)
                g = int(hex_text[2:4], 16)
                b = int(hex_text[4:6], 16)
                self._apply_color(r, g, b)
            else:
                self._update_status("⚠ Invalid HEX code! (e.g. #FF00FF)")
        except ValueError:
            self._update_status("⚠ Invalid HEX code!")

    def _on_off(self, btn):
        ok = write_sysfs(BRIGHTNESS_PATH, '0')
        if ok:
            self.brightness_scale.set_value(0)
            self._update_status("Keyboard backlight turned off")
        else:
            self._update_status("⚠ Could not turn off!")

    def _on_off(self, btn):
        ok = write_sysfs(BRIGHTNESS_PATH, '0')
        if ok:
            self.brightness_scale.set_value(0)
            self._update_status("Keyboard backlight turned off")
        else:
            self._update_status("⚠ Could not turn off!")

if __name__ == '__main__':
    app = KeyboardControllerApp()
    app.run(None)
