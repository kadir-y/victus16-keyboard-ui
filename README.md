> [!IMPORTANT]
> This project and its interface were primarily generated with the assistance of an AI.

# Victus 16 Keyboard Backlight Controller

A native Linux GTK4 GUI application designed specifically to control the RGB keyboard backlight colors and brightness on HP Victus 16 laptops. This application provides a modern, responsive, and customizable interface to seamlessly manage your keyboard lighting on Linux.

![App Preview](com.victus16.keyboard.png) 
*(Note: Visual illustration of the UI layout)*

## ⚠️ Prerequisites & Dependencies

For this application to successfully communicate with your keyboard hardware, you **must** install the HP WMI fan and backlight control kernel module. This module enables the necessary `sysfs` interfaces.

1. Install the required DKMS kernel module from: 
   **[TUXOV/hp-wmi-fan-and-backlight-control](https://github.com/TUXOV/hp-wmi-fan-and-backlight-control)**
   *(Note: This module is currently not provided by AUR and must be installed manually via DKMS as instructed in its repository.)*
2. Follow the installation instructions provided in that repository (e.g., `make dkms-install`).
3. **Reboot your system** after installation to ensure the kernel module is properly loaded into the system.

## 🛠️ How It Works (Behind the Scenes)

This application serves as a user-friendly, graphical wrapper over standard Linux `sysfs` LED interfaces. Under the hood, the app invokes basic system commands using `sudo` to write to specific hardware files.

The core mechanics of the application are built upon these basic terminal commands:

**Changing the Color (RGB):**
```bash
# Sets the keyboard backlight to Red (R:255, G:0, B:0)
echo "255 0 0" | sudo tee /sys/class/leds/hp::kbd_backlight/multi_intensity
```

**Changing the Brightness:**
```bash
# Changes the brightness level to roughly 50% (Accepts values from 0-255)
echo 128 | sudo tee /sys/class/leds/hp::kbd_backlight/brightness
```
*Note: The app executes these tasks automatically when you interact with the UI sliders or color templates.*

## 🚀 Installation

### Option 1: Install from AUR (Recommended)
This package is available on the Arch User Repository (AUR). You can easily install it using an AUR helper like `yay` or `paru`:

```bash
yay -S victus16-keyboard-ui
```

### Option 2: Run from Source (Python)

If you prefer to run the application directly from the source code without installing:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kadir-y/victus16-keyboard-ui.git
   ```

2. **Navigate to the directory:**
   ```bash
   cd victus16-keyboard-ui
   ```

3. **Install Dependencies (Arch Linux example):**
   Ensure you have Python and GTK4 dependencies installed:
   ```bash
   sudo pacman -S python python-gobject gtk4
   ```

4. **Run the application:**
   ```bash
   python keyboard_controller.py
   ```

*Note: Since you are running from source without installing the sudoers file, the application might prompt you for your root password in the terminal when writing to the hardware files.*

## 🎨 Features
- **Color Wheel & Hex Input:** Select precise colors with an interactive wheel or specific hex codes.
- **Customizable Templates:** Save, update, and manage your own favorite RGB configurations with descriptions.
- **Advanced Adjustments:** Fine-tune Hue, Saturation, and individual template brightness.
- **Persistent Data:** Your custom templates are securely saved to `~/.config/victus16-keyboard/templates.json`.
- **System Templates:** Includes default system templates (like "Off") that cannot be accidentally modified or deleted.
- **Restore on Boot:** Automatically restore your last active color and brightness on system startup using the included systemd service.
- **Responsive Layout:** A fluid grid layout that perfectly adapts when resizing the application window.

## 🔄 Restoring State on Boot

If you want your keyboard to automatically light up with your last selected color and brightness when you turn on your computer, you can enable the provided `systemd` user service.

1. **Enable and start the service:**
   ```bash
   systemctl --user enable --now victus16-keyboard-restore.service
   ```

2. **Check the status if it's not working:**
   ```bash
   systemctl --user status victus16-keyboard-restore.service
   ```

*(Troubleshooting: If the service fails, ensure that the `hp-wmi-fan-and-backlight-control` kernel module is installed and loaded. You can verify this by checking if `/sys/class/leds/hp::kbd_backlight/multi_intensity` exists.)*

## 📝 License
This project is open-source under the MIT License. Feel free to fork, modify, or contribute!
