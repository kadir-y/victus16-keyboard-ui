# Maintainer: Kadir <kadir@localhost>
pkgname=victus16-keyboard-ui
pkgver=1.0.0
pkgrel=1
pkgdesc="HP Victus 16 Keyboard RGB Backlight Controller (GTK4)"
arch=('any')
url="https://github.com/kadir/victus16-keyboard-ui"
license=('MIT')
depends=('python' 'gtk4' 'python-gobject')
install=victus16-keyboard.install
source=(
    'keyboard_controller.py'
    'com.victus16.keyboard.desktop'
    'victus16-keyboard-sudoers'
    'victus16-keyboard.install'
    'com.victus16.keyboard.png'
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    # Install main app
    install -Dm755 "$srcdir/keyboard_controller.py" \
        "$pkgdir/usr/bin/victus16-keyboard"

    # Install desktop entry
    install -Dm644 "$srcdir/com.victus16.keyboard.desktop" \
        "$pkgdir/usr/share/applications/com.victus16.keyboard.desktop"

    # Install icon
    install -Dm644 "$srcdir/com.victus16.keyboard.png" \
        "$pkgdir/usr/share/icons/hicolor/256x256/apps/com.victus16.keyboard.png"

    # Install sudoers rule
    install -Dm440 "$srcdir/victus16-keyboard-sudoers" \
        "$pkgdir/etc/sudoers.d/victus16-keyboard"
}
