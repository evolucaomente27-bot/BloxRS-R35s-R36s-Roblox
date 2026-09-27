import os
import urllib.request
from PIL import Image

TEXTURES_DIR = os.path.abspath(r"C:\Users\user\Desktop\QR35S\.BloxRS\godot_project\assets\textures")
os.makedirs(TEXTURES_DIR, exist_ok=True)

DOWNLOADS = [
    # Surfaces (dudeax Roblox HD Studs)
    ("studs.png", "https://raw.githubusercontent.com/dudeax/Roblox-HD-Studs/master/2x2%20Textures/Diffuse%20Maps/Studs%202x2%20AO%20Diffuse.png", 256),
    ("inlets.png", "https://raw.githubusercontent.com/dudeax/Roblox-HD-Studs/master/2x2%20Textures/Diffuse%20Maps/Inlets%202x2%20AO%20Diffuse.png", 256),
    ("weld.png", "https://raw.githubusercontent.com/dudeax/Roblox-HD-Studs/master/2x2%20Textures/Diffuse%20Maps/Weld%202x2%20AO%20Diffuse.png", 256),
    
    # Materials (MaximumADHD Classic Pre-2022 Materials)
    ("brick.png", "https://raw.githubusercontent.com/MaximumADHD/Roblox-Materials/master/PartsPre2022/Brick/color.png", 256),
    ("wood.png", "https://raw.githubusercontent.com/MaximumADHD/Roblox-Materials/master/PartsPre2022/Wood/color.png", 256),
    ("grass.png", "https://raw.githubusercontent.com/MaximumADHD/Roblox-Materials/master/PartsPre2022/Grass/color.png", 256),
    ("concrete.png", "https://raw.githubusercontent.com/MaximumADHD/Roblox-Materials/master/PartsPre2022/Concrete/color.png", 256),
    ("diamond_plate.png", "https://raw.githubusercontent.com/MaximumADHD/Roblox-Materials/master/PartsPre2022/DiamondPlate/color.png", 256),
    ("slate.png", "https://raw.githubusercontent.com/MaximumADHD/Roblox-Materials/master/PartsPre2022/Slate/color.png", 256),
]

print(f"[*] Baixando e otimizando texturas para: {TEXTURES_DIR}\n")

temp_file = os.path.join(TEXTURES_DIR, "_temp.png")

for filename, url, target_size in DOWNLOADS:
    target_path = os.path.join(TEXTURES_DIR, filename)
    print(f"-> Baixando {filename}... ", end="", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        with open(temp_file, "wb") as f:
            f.write(data)
        
        # Redimensiona para resolução ideal (256x256) garantindo 60 FPS no R35S
        with Image.open(temp_file) as im:
            im = im.convert("RGBA")
            im = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
            im.save(target_path, "PNG", optimize=True)
            
        print(f"[OK] ({target_size}x{target_size})")
    except Exception as e:
        print(f"[ERRO] {e}")

if os.path.exists(temp_file):
    os.remove(temp_file)

# Cria também uma textura "smooth.png" (branca com borda sutil de bevel clássico)
smooth_path = os.path.join(TEXTURES_DIR, "smooth.png")
im_smooth = Image.new("RGBA", (128, 128), (250, 250, 250, 255))
from PIL import ImageDraw
draw = ImageDraw.Draw(im_smooth)
draw.rectangle([0, 0, 127, 127], outline=(210, 210, 210, 255), width=2)
im_smooth.save(smooth_path)
print("-> Gerado smooth.png [OK]")

print("\n[OK] Todas as texturas foram baixadas e otimizadas!")
