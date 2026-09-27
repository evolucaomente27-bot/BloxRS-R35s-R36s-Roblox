# 🗺️ Acervo de Mapas Clássicos do Roblox (2006 - 2008)

Esta pasta contém mapas históricos e clássicos do Roblox originais (`.rbxl`), preservados dos repositórios oficiais e do Novetus.

---

### 📦 Mapas em Formato XML (Prontos para Conversão Direta com `convert_rbxl.py`):

| Arquivo `.rbxl` | Descrição | Era | Status |
| :--- | :--- | :--- | :--- |
| `Crossroads.rbxl` | O mapa mais icônico da história do Roblox | 2006-2007 | **Convertido** (`Crossroads.tscn`) |
| `Chaos Canyon.rbxl` | Batalha lendária com pontes suspensas e cânions | 2006 | **Convertido** (`ChaosCanyon.tscn`) |
| `Happy Home in Robloxia.rbxl` | A clássica casa inicial de tijolos | 2007 | **Convertido** (`HappyHome.tscn`) |
| `Glass Houses.rbxl` | Arena de casas de vidro transparentes | 2007 | Pronto para converter |
| `Haunted Mansion.rbxl` | Mansão assombrada clássica de John Shedletsky | 2006 | Pronto para converter |
| `Pirate Ship.rbxl` | Navios piratas clássicos em combate | 2006 | Pronto para converter |
| `Community Construction Site.rbxl` | Canteiro de obras clássico comunitário | 2006 | Pronto para converter |
| `Grey City.rbxl` | Cidade cinza com arranha-céus | 2006 | Pronto para converter |
| `ROBLOX World Headquarters.rbxl` | Quartel-general original da equipe Roblox | 2007 | Pronto para converter |
| `Stairway to Heaven.rbxl` | Escadaria clássica para o céu | 2007 | Pronto para converter |
| `Timmy and the Killbots.rbxl` | Sobrevivência contra robôs assassinos | 2007 | Pronto para converter |
| `Train Crashing.rbxl` | Trenzinhos em alta velocidade | 2007 | Pronto para converter |
| `Astroland.rbxl` | Parque espacial com montanha-russa | 2007 | Pronto para converter |
| `Dodge Stuff.rbxl` | Esquivar de objetos arremessados | 2007 | Pronto para converter |

---

### 📦 Mapas em Formato Binário:
Alguns arquivos mais recentes (`Rocket Arena.rbxl`, `Castle Warfare.rbxl`, etc.) estão no formato binário comprimido moderno do Roblox. Para esses, você pode abri-los no Roblox Studio/Novetus e salvar como **Export Selection (.obj)** ou salvá-los no formato `.rbxlx` (XML).

---

### ⚙️ Como Converter Qualquer Mapa para o R35S:
No terminal, dentro de `.BloxRS`:
```bash
python converter/convert_rbxl.py "maps/NomeDoMapa.rbxl" "godot_project/scenes/NomeDoMapa.tscn"
```
A cena `.tscn` gerada já contém todos os blocos com posições, tamanhos, cores clássicas e colisões físicas automáticas!
