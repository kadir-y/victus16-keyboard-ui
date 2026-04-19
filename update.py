import re

with open('keyboard_controller.py', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace('import colorsys', 'import colorsys\nimport os\nimport json')

# 2. TEMPLATES to DEFAULT_TEMPLATES and logic
old_templates = """# ─── Color Templates ───
# Each template defines a base HSV color, recommended brightness, and description.
# Users can adjust hue and saturation after selecting a template.
TEMPLATES = [
    {"name": "Ateş",       "icon": "🔥", "hue": 0,   "sat": 1.0, "val": 1.0, "brightness": 180, "desc": "Kızıl ateş tonu"},
    {"name": "Gün Batımı", "icon": "🌅", "hue": 25,  "sat": 1.0, "val": 1.0, "brightness": 200, "desc": "Sıcak turuncu tonlar"},
    {"name": "Altın",      "icon": "✨", "hue": 45,  "sat": 0.9, "val": 1.0, "brightness": 160, "desc": "Zarif altın parıltısı"},
    {"name": "Orman",      "icon": "🌲", "hue": 120, "sat": 1.0, "val": 1.0, "brightness": 140, "desc": "Doğal yeşil tonlar"},
    {"name": "Neon",       "icon": "💚", "hue": 100, "sat": 1.0, "val": 1.0, "brightness": 220, "desc": "Parlak neon yeşil"},
    {"name": "Okyanus",    "icon": "🌊", "hue": 190, "sat": 0.85,"val": 1.0, "brightness": 170, "desc": "Derin okyanus mavisi"},
    {"name": "Gökyüzü",    "icon": "☁️", "hue": 200, "sat": 0.6, "val": 1.0, "brightness": 200, "desc": "Açık gökyüzü mavisi"},
    {"name": "Gece",       "icon": "🌙", "hue": 240, "sat": 1.0, "val": 1.0, "brightness": 100, "desc": "Derin gece laciverti"},
    {"name": "Eflatun",    "icon": "💜", "hue": 270, "sat": 0.8, "val": 1.0, "brightness": 160, "desc": "Mistik mor tonlar"},
    {"name": "Sakura",     "icon": "🌸", "hue": 330, "sat": 0.6, "val": 1.0, "brightness": 180, "desc": "Yumuşak pembe çiçek"},
    {"name": "Magenta",    "icon": "💎", "hue": 300, "sat": 1.0, "val": 1.0, "brightness": 170, "desc": "Canlı magenta"},
    {"name": "Buz",        "icon": "❄️", "hue": 195, "sat": 0.35,"val": 1.0, "brightness": 220, "desc": "Soğuk buz tonu"},
    {"name": "Saf Beyaz",  "icon": "⬜", "hue": 0,   "sat": 0.0, "val": 1.0, "brightness": 255, "desc": "Saf beyaz ışık"},
    {"name": "Sıcak Beyaz","icon": "🕯️","hue": 30,  "sat": 0.35,"val": 1.0, "brightness": 200, "desc": "Mum ışığı sıcaklığı"},
    {"name": "HP Mavi",    "icon": "💻", "hue": 199, "sat": 0.74,"val": 0.91,"brightness": 180, "desc": "HP imza mavisi"},
    {"name": "Cyberpunk",  "icon": "🤖", "hue": 285, "sat": 0.9, "val": 1.0, "brightness": 200, "desc": "Fütüristik neon mor"},
]"""

new_templates = """CONFIG_DIR = os.path.expanduser('~/.config/victus16-keyboard')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'templates.json')

# ─── Color Templates ───
DEFAULT_TEMPLATES = [
    {"name": "Fire",       "icon": "🔥", "hue": 0,   "sat": 1.0, "val": 1.0, "brightness": 180, "desc": "Red fire tone"},
    {"name": "Sunset",     "icon": "🌅", "hue": 25,  "sat": 1.0, "val": 1.0, "brightness": 200, "desc": "Warm orange tones"},
    {"name": "Gold",       "icon": "✨", "hue": 45,  "sat": 0.9, "val": 1.0, "brightness": 160, "desc": "Elegant gold glow"},
    {"name": "Forest",     "icon": "🌲", "hue": 120, "sat": 1.0, "val": 1.0, "brightness": 140, "desc": "Natural green tones"},
    {"name": "Neon",       "icon": "💚", "hue": 100, "sat": 1.0, "val": 1.0, "brightness": 220, "desc": "Bright neon green"},
    {"name": "Ocean",      "icon": "🌊", "hue": 190, "sat": 0.85,"val": 1.0, "brightness": 170, "desc": "Deep ocean blue"},
    {"name": "Sky",        "icon": "☁️", "hue": 200, "sat": 0.6, "val": 1.0, "brightness": 200, "desc": "Clear sky blue"},
    {"name": "Night",      "icon": "🌙", "hue": 240, "sat": 1.0, "val": 1.0, "brightness": 100, "desc": "Deep night navy"},
    {"name": "Lilac",      "icon": "💜", "hue": 270, "sat": 0.8, "val": 1.0, "brightness": 160, "desc": "Mystic purple tones"},
    {"name": "Sakura",     "icon": "🌸", "hue": 330, "sat": 0.6, "val": 1.0, "brightness": 180, "desc": "Soft pink flower"},
    {"name": "Magenta",    "icon": "💎", "hue": 300, "sat": 1.0, "val": 1.0, "brightness": 170, "desc": "Vivid magenta"},
    {"name": "Ice",        "icon": "❄️", "hue": 195, "sat": 0.35,"val": 1.0, "brightness": 220, "desc": "Cold ice tone"},
    {"name": "Pure White", "icon": "⬜", "hue": 0,   "sat": 0.0, "val": 1.0, "brightness": 255, "desc": "Pure white light"},
    {"name": "Warm White", "icon": "🕯️","hue": 30,  "sat": 0.35,"val": 1.0, "brightness": 200, "desc": "Candle light warmth"},
    {"name": "HP Blue",    "icon": "💻", "hue": 199, "sat": 0.74,"val": 0.91,"brightness": 180, "desc": "HP signature blue"},
    {"name": "Cyberpunk",  "icon": "🤖", "hue": 285, "sat": 0.9, "val": 1.0, "brightness": 200, "desc": "Futuristic neon purple"},
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
"""
content = content.replace(old_templates, new_templates)

# 3. Fix CSS loading
content = content.replace('CSS = b"""', 'CSS = """')
content = content.replace('css_provider.load_from_data(CSS)', "css_provider.load_from_data(CSS.encode('utf-8'))")
# Fix other css_provider.load_from_data encodings if any
content = content.replace("b\".hue-scale", "\".hue-scale")
content = content.replace("b\"hsl(0,100%,50%)", "\"hsl(0,100%,50%)")
content = content.replace("b\"hsl(180,100%,50%)", "\"hsl(180,100%,50%)")
content = content.replace(")); }\"", ")); }\".encode('utf-8')")

with open('keyboard_controller.py', 'w') as f:
    f.write(content)
