"""
CSS styles for the keyboard controller GTK4 application.
"""

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
