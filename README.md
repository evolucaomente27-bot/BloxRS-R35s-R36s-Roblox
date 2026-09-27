# 🎮 BloxRS - Port Nativo de Mapas do Roblox para R35S e PC

Suíte completa para portar, testar e jogar mapas clássicos do Roblox (era 2006 a 2008) nativamente no **PC (Windows)** e no console portátil **R35S** (ArkOS / PortMaster) em **640x480 a 60 FPS**.

---

## 🚀 Como Testar Imediatamente no PC

Basta dar dois cliques no arquivo:
👉 **`Rodar_no_PC.bat`**

O jogo abrirá imediatamente na janela configurada com o motor Godot 3.5 portátil (já incluído na pasta `tools/`).

### Controles no PC:
* **WASD:** Andar com o personagem Noob clássico
* **Mouse:** Girar a câmera em 360° (estilo Roblox tradicional)
* **Espaço:** Pular
* **Teclas [1, 2, 3, 4]:** **Troca de mapa instantânea em tempo real!**
  * `[1]` Baseplate Clássica com torres e escadas
  * `[2]` **Crossroads** (1.766 partes)
  * `[3]` **Chaos Canyon** (1.726 partes)
  * `[4]` **Happy Home in Robloxia** (1.964 partes)
* **R:** Resetar / Respawnar o boneco
* **ESC:** Soltar o ponteiro do mouse / Sair do jogo

---

## 🛠️ Como Abrir o Editor da Godot

Para editar mapas, mexer na câmera, adicionar itens ou mudar texturas:
👉 Dê dois cliques em **`Abrir_Editor_Godot.bat`**.

---

## 🗺️ Como Converter Mais Mapas da Pasta `maps/`

No terminal ou prompt de comando:
```bash
python converter/convert_rbxl.py "maps/Glass Houses.rbxl" "godot_project/scenes/GlassHouses.tscn"
```

---

## 🕹️ Como Jogar no R35S (PortMaster)

1. Na Godot (`Abrir_Editor_Godot.bat`), vá em **Project -> Export -> Linux/X11** e clique em **Export PCK/Zip...**.
2. Salve como `bloxrs.pck` dentro da pasta `r35s_package/bloxrs/`.
3. Copie o arquivo `r35s_package/BloxRS.sh` e a pasta `r35s_package/bloxrs` para o cartão SD do R35S em `/roms/ports/`.
4. Leia o arquivo `r35s_package/GUIA_INSTALACAO_R35S.md` para detalhes adicionais.
