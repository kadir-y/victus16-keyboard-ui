"""
Custom color wheel widget for the keyboard controller.
Provides an interactive HSV color wheel drawn with Cairo.
"""

import math
import colorsys

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class ColorWheelWidget(Gtk.DrawingArea):
    """Interactive color wheel drawn with Cairo for HSV color selection."""

    def __init__(self, on_color_picked):
        super().__init__()
        self.on_color_picked = on_color_picked
        self.set_size_request(220, 220)
        self.set_draw_func(self._draw)
        self._selected_hue = 0
        self._selected_sat = 1.0

        # Click gesture for instant color selection
        click = Gtk.GestureClick()
        click.connect('pressed', self._on_click)
        self.add_controller(click)

        # Drag gesture for continuous color picking
        drag = Gtk.GestureDrag()
        drag.connect('drag-begin', self._on_drag_begin)
        drag.connect('drag-update', self._on_drag_update)
        self.add_controller(drag)

    def _pick_at(self, x, y):
        """Calculate hue and saturation from a point on the wheel."""
        w = self.get_width()
        h = self.get_height()
        cx, cy = w / 2, h / 2
        radius = min(cx, cy) - 8
        dx, dy = x - cx, y - cy
        dist = math.sqrt(dx * dx + dy * dy)

        # Clamp distance to wheel radius
        if dist > radius:
            dist = radius

        angle = math.atan2(dy, dx)
        self._selected_hue = (math.degrees(angle) + 360) % 360
        self._selected_sat = dist / radius
        self.queue_draw()

        r, g, b = colorsys.hsv_to_rgb(
            self._selected_hue / 360, self._selected_sat, 1.0
        )
        self.on_color_picked(int(r * 255), int(g * 255), int(b * 255))

    def _on_click(self, gesture, n, x, y):
        self._pick_at(x, y)

    def _on_drag_begin(self, gesture, x, y):
        self._drag_start_x = x
        self._drag_start_y = y
        self._pick_at(x, y)

    def _on_drag_update(self, gesture, off_x, off_y):
        self._pick_at(self._drag_start_x + off_x, self._drag_start_y + off_y)

    def set_color(self, r, g, b):
        """Set the wheel's selected color from RGB values (0-255)."""
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self._selected_hue = h * 360
        self._selected_sat = s
        self.queue_draw()

    def _draw(self, area, cr, width, height):
        """Render the color wheel and the selector indicator."""
        cx, cy = width / 2, height / 2
        radius = min(cx, cy) - 8

        # Draw color wheel pixel by pixel
        steps = 360
        for i in range(steps):
            angle = math.radians(i)
            for j in range(0, int(radius), 2):
                sat = j / radius
                r, g, b = colorsys.hsv_to_rgb(i / 360, sat, 1.0)
                cr.set_source_rgb(r, g, b)
                x = cx + j * math.cos(angle)
                y = cy + j * math.sin(angle)
                cr.rectangle(x - 1, y - 1, 3, 3)
                cr.fill()

        # Draw selector circle at the selected position
        sel_dist = self._selected_sat * radius
        sel_x = cx + sel_dist * math.cos(math.radians(self._selected_hue))
        sel_y = cy + sel_dist * math.sin(math.radians(self._selected_hue))

        # White outline ring
        cr.set_source_rgb(1, 1, 1)
        cr.arc(sel_x, sel_y, 8, 0, 2 * math.pi)
        cr.set_line_width(2.5)
        cr.stroke()

        # Filled inner circle showing the selected color
        r, g, b = colorsys.hsv_to_rgb(
            self._selected_hue / 360, self._selected_sat, 1.0
        )
        cr.set_source_rgb(r, g, b)
        cr.arc(sel_x, sel_y, 5.5, 0, 2 * math.pi)
        cr.fill()
