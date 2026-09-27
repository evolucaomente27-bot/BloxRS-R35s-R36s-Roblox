import os
import urllib.request
import urllib.parse
import sys

BASE_DIR = os.path.abspath(r"C:\Users\user\Desktop\QR35S\.BloxRS")
MAPS_DIR = os.path.join(BASE_DIR, "maps")
os.makedirs(MAPS_DIR, exist_ok=True)

MAPS_TO_DOWNLOAD = [
    # Miscellaneous (Clássicos Fundamentais)
    ("Miscellaneous", "Crossroads.rbxl", "Crossroads - O mapa mais icônico da história do Roblox (2006-2007)"),
    ("Miscellaneous", "Happy Home in Robloxia.rbxl", "Happy Home - A casa inicial padrão clássica onde todos começavam"),
    ("Miscellaneous", "Glass Houses.rbxl", "Glass Houses - Batalha clássica em casas transparentes suspensas"),
    ("Miscellaneous", "Rocket Arena.rbxl", "Rocket Arena - Arena clássica de combate com lança-foguetes"),
    ("Miscellaneous", "ROBLOX World Headquarters.rbxl", "Roblox HQ - O quartel general original dos desenvolvedores"),
    
    # Shedletsky (Telamon)
    ("Shedletsky", "Haunted Mansion.rbxl", "Haunted Mansion - Mansão assombrada clássica de John Shedletsky"),
    ("Shedletsky", "Sword Fight in the Dark.rbxl", "Sword Fight in the Dark - Combate de espadas com visibilidade reduzida"),
    ("Shedletsky", "Pinball Wizards.rbxl", "Pinball Wizards - Mapa clássico de física e pinball"),
    ("Shedletsky", "Dodge Stuff.rbxl", "Dodge Stuff - Mapa clássico de sobrevivência desviando de objetos"),
    ("Shedletsky", "Astroland.rbxl", "Astroland - Parque espacial clássico com montanhas-russas"),

    # Community-created
    ("Community-created", "Chaos Canyon.rbxl", "Chaos Canyon - Mapa lendário de batalha em cânions e pontes"),
    ("Community-created", "Castle Warfare.rbxl", "Castle Warfare - Batalha de castelos e catapultas"),
    ("Community-created", "Four Towers Bridge Battle.rbxl", "Four Towers Bridge Battle - Quatro torres conectadas por pontes"),
    ("Community-created", "Emerald Forest.rbxl", "Emerald Forest - Floresta clássica com exploração e cabanas"),
    
    # Content team
    ("Content team", "Ro-Quake DM17 - The Longest Yard.rbxl", "Ro-Quake DM17 - Recriação clássica do mapa do Quake 3 no Roblox")
]

BASE_URL = "https://raw.githubusercontent.com/Roblox/Old-Open-Source-Levels/master/ROBLOX"

print(f"[*] Baixando mapas clássicos para: {MAPS_DIR}\n")

downloaded_info = []

for category, filename, description in MAPS_TO_DOWNLOAD:
    encoded_category = urllib.parse.quote(category)
    encoded_filename = urllib.parse.quote(filename)
    url = f"{BASE_URL}/{encoded_category}/{encoded_filename}"
    target_path = os.path.join(MAPS_DIR, filename)

    print(f"-> Baixando: {filename} ... ", end="", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            with open(target_path, "wb") as f:
                f.write(data)
        size_kb = len(data) / 1024
        print(f"[OK] ({size_kb:.1f} KB)")
        downloaded_info.append((filename, description, f"{size_kb:.1f} KB"))
    except Exception as e:
        print(f"[ERRO] {e}")

# Gerar arquivo README_MAPAS.md dentro da pasta maps
readme_path = os.path.join(MAPS_DIR, "README_MAPAS.md")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write("# 🗺️ Acervo de Mapas Antigos do Roblox (2006 - 2008)\n\n")
    f.write("Esta pasta contém arquivos originais `.rbxl` clássicos preservados diretamente dos repositórios históricos da Roblox.\n\n")
    f.write("### Lista de Mapas Disponíveis:\n\n")
    f.write("| Arquivo | Descrição | Tamanho |\n")
    f.write("| :--- | :--- | :--- |\n")
    for name, desc, size in downloaded_info:
        f.write(f"| `{name}` | {desc} | {size} |\n")
    
    f.write("\n---\n\n")
    f.write("### 🛠️ Como Converter Qualquer Mapa para o R35S:\n\n")
    f.write("Execute o conversor apontando para o mapa desejado:\n\n")
    f.write("```bash\n")
    f.write('python ../converter/convert_rbxl.py "Crossroads.rbxl" "../godot_project/scenes/Crossroads.tscn"\n')
    f.write("```\n\n")
    f.write("Depois abra o Godot 3.5, defina a cena como mapa e exporte para o R35S!\n")

print(f"\n[OK] Todos os downloads concluidos! Indice gerado em: {readme_path}")
