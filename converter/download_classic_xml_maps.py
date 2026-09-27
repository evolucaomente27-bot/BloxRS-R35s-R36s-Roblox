import os
import urllib.request
import urllib.parse
import bz2

MAPS_DIR = os.path.abspath(r"C:\Users\user\Desktop\QR35S\.BloxRS\maps")
os.makedirs(MAPS_DIR, exist_ok=True)

# Lista de mapas clássicos autênticos em XML (era 2006-2007) do Novetus Map Pack
NOVETUS_MAPS = [
    # 2006L
    ("maps/2006/2006L", "2006L - Chaos Canyon.rbxl.bz2", "Chaos Canyon.rbxl", "Chaos Canyon (2006) - Batalha de canhões e pontes suspensas"),
    ("maps/2006/2006L", "2006L - Haunted Mansion.rbxl.bz2", "Haunted Mansion.rbxl", "Haunted Mansion (2006) - Mansão assombrada de John Shedletsky"),
    ("maps/2006/2006L", "2006L - Pirate Ship.rbxl.bz2", "Pirate Ship.rbxl", "Pirate Ship (2006) - Batalha de navios piratas clássicos"),
    ("maps/2006/2006L", "2006L - Community Construction Site.rbxl.bz2", "Community Construction Site.rbxl", "Canteiro de obras clássico comunitário de 2006"),
    ("maps/2006/2006L", "2006L - Grey City.rbxl.bz2", "Grey City.rbxl", "Cidade cinza clássica com arranha-céus"),
    
    # 2007M
    ("maps/2007/2007M", "2007M -  Happy Home in Robloxia.rbxl.bz2", "Happy Home in Robloxia.rbxl", "Happy Home (2007) - A casa clássica onde todos começavam"),
    ("maps/2007/2007M", "2007M - Glass Houses.rbxl.bz2", "Glass Houses.rbxl", "Glass Houses (2007) - Batalha em casas de vidro transparentes"),
    ("maps/2007/2007M", "2007M - ROBLOX World Headquarters.rbxl.bz2", "ROBLOX World Headquarters.rbxl", "Quartel-general original da equipe Roblox"),
    ("maps/2007/2007M", "2007M - Stairway to Heaven.rbxl.bz2", "Stairway to Heaven.rbxl", "Escadaria clássica para o céu"),
    ("maps/2007/2007M", "2007M - Timmy and the Killbots.rbxl.bz2", "Timmy and the Killbots.rbxl", "Mapa clássico de sobrevivência contra robôs"),
    ("maps/2007/2007M", "2007M - Train Crashing.rbxl.bz2", "Train Crashing.rbxl", "Trem clássico em alta velocidade"),
]

BASE_URL = "https://raw.githubusercontent.com/Novetus/Novetus-Map-Pack/master"

print(f"[*] Baixando e descompactando mapas autenticos em XML para: {MAPS_DIR}\n")

for rel_path, remote_file, local_file, desc in NOVETUS_MAPS:
    url = f"{BASE_URL}/{rel_path}/{urllib.parse.quote(remote_file)}"
    out_path = os.path.join(MAPS_DIR, local_file)
    print(f"-> Baixando {local_file} ... ", end="", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data_bz2 = resp.read()
        raw_xml = bz2.decompress(data_bz2)
        with open(out_path, "wb") as f:
            f.write(raw_xml)
        size_kb = len(raw_xml) / 1024
        print(f"[OK] ({size_kb:.1f} KB - XML Puro)")
    except Exception as e:
        print(f"[ERRO] {e}")

print("\n[OK] Concluido com sucesso!")
