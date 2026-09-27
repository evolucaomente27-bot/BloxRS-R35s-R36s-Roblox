#!/bin/bash
# =============================================================
# BloxRS - Port Nativo de Roblox Clássico para R35S / ArkOS
# =============================================================

# 1. Localiza a pasta do PortMaster e variáveis do sistema
if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/roms/ports/PortMaster/" ]; then
  controlfolder="/roms/ports/PortMaster"
elif [ -d "/roms2/ports/PortMaster/" ]; then
  controlfolder="/roms2/ports/PortMaster"
elif [ -d "$HOME/PortMaster/" ]; then
  controlfolder="$HOME/PortMaster"
fi

# Carrega os controles e funções padrão do PortMaster (se disponível)
if [ -f "$controlfolder/control.txt" ]; then
  source "$controlfolder/control.txt"
  [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
  get_controls
fi

# 2. Identifica o diretório do jogo (suporta SD1 e SD2)
GAMEDIR="/roms/ports/bloxrs"
if [ -d "/roms2/ports/bloxrs" ]; then
  GAMEDIR="/roms2/ports/bloxrs"
fi

cd "$GAMEDIR"

# 3. Configuração de Logs detalhados
> "$GAMEDIR/log.txt"
exec > >(tee "$GAMEDIR/log.txt") 2>&1

echo "========================================================"
echo "  BloxRS - Roblox Clássico para R35S (RK3326)"
echo "========================================================"

# Previne que o motor FRT feche sozinho com atalhos de botões do controle:
export FRT_NO_EXIT_SHORTCUTS=FRT_NO_EXIT_SHORTCUTS

# 4. AUTO-CONVERSÃO DE MAPAS .rbxl NO PRÓPRIO R35S
USER_MAPS_DIR="$HOME/.local/share/godot/app_userdata/BloxRS/maps"
mkdir -p "$USER_MAPS_DIR"

if [ -d "$GAMEDIR/maps" ] && [ -f "$GAMEDIR/converter/convert_rbxl.py" ]; then
  for rbxl in "$GAMEDIR/maps"/*.rbxl; do
    [ -e "$rbxl" ] || continue
    filename=$(basename "$rbxl" .rbxl)
    target_tscn="$USER_MAPS_DIR/${filename}.tscn"
    
    if [ ! -f "$target_tscn" ] || [ "$rbxl" -nt "$target_tscn" ]; then
      echo "[Auto-Port] Convertendo: $filename ..."
      python3 "$GAMEDIR/converter/convert_rbxl.py" "$rbxl" "$target_tscn"
    fi
  done
fi

# 5. MONTA O RUNTIME GODOT (FRT 3.5.2)
runtime="frt_3.5.2"
godot_dir="$HOME/godot"
godot_file=""

# Procura o squashfs na pasta libs do PortMaster ou na pasta do jogo
if [ -f "$controlfolder/libs/${runtime}.squashfs" ]; then
  godot_file="$controlfolder/libs/${runtime}.squashfs"
elif [ -f "$GAMEDIR/${runtime}.squashfs" ]; then
  godot_file="$GAMEDIR/${runtime}.squashfs"
elif [ -f "$controlfolder/libs/godot_3.5.2.squashfs" ]; then
  godot_file="$controlfolder/libs/godot_3.5.2.squashfs"
fi

RUNNER=""
[ -n "$ESUDO" ] || ESUDO="sudo"

if [ -n "$godot_file" ] && [ -f "$godot_file" ]; then
  echo "Montando runtime Godot: $godot_file em $godot_dir"
  $ESUDO mkdir -p "$godot_dir"
  $ESUDO umount "$godot_dir" 2>/dev/null || true
  $ESUDO mount "$godot_file" "$godot_dir"
  PATH="$godot_dir:$PATH"
  
  if [ -f "$godot_dir/frt_3.5.2" ]; then
    RUNNER="$godot_dir/frt_3.5.2"
  elif [ -f "$godot_dir/bin/godot" ]; then
    RUNNER="$godot_dir/bin/godot"
  elif [ -f "$godot_dir/frt" ]; then
    RUNNER="$godot_dir/frt"
  fi
fi

# Fallback se tiver o binário extraído solto na pasta do jogo
if [ ! -x "$RUNNER" ] && [ -x "$GAMEDIR/$runtime" ]; then
  RUNNER="$GAMEDIR/$runtime"
fi

if [ ! -x "$RUNNER" ]; then
  echo "ERRO: O executável do Godot ($runtime) não foi encontrado!"
  sleep 4
  exit 1
fi

# 6. CONFIGURAÇÃO DE CONTROLES DO R35S (GPTOKEYB + SDL2)
$ESUDO chmod 666 /dev/uinput 2>/dev/null
chmod +x "$RUNNER" 2>/dev/null

RUNNER_NAME=$(basename "$RUNNER")

# Localiza e inicializa o gptokeyb
GPTOKEYB_CMD=""
for gpath in "$GPTOKEYB" "/usr/bin/gptokeyb" "$controlfolder/gptokeyb" "/opt/system/Tools/PortMaster/gptokeyb" "/opt/inttools/gptokeyb"; do
  if [ -x "$gpath" ]; then
    GPTOKEYB_CMD="$gpath"
    break
  fi
done

if [ -n "$GPTOKEYB_CMD" ] && [ -f "$GAMEDIR/bloxrs.gptk" ]; then
  echo "Ativando controles R35S com gptokeyb: $GPTOKEYB_CMD ($RUNNER_NAME)"
  "$GPTOKEYB_CMD" "$RUNNER_NAME" -c "$GAMEDIR/bloxrs.gptk" &
fi

if [ -n "$sdl_controllerconfig" ]; then
  export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
elif [ -f "/usr/lib/gamecontrollerdb.txt" ]; then
  export SDL_GAMECONTROLLERCONFIG_FILE="/usr/lib/gamecontrollerdb.txt"
fi

export SPA_PLUGIN_DIR="/usr/lib/aarch64-linux-gnu/spa-0.2"
export PIPEWIRE_MODULE_DIR="/usr/lib/aarch64-linux-gnu/pipewire-0.3"

echo "Iniciando BloxRS a 60 FPS..."
echo "Runner: $RUNNER"
"$RUNNER" $GODOT_OPTS --main-pack "$GAMEDIR/bloxrs.pck"

# 7. FINALIZAÇÃO E LIMPEZA
$ESUDO kill -9 $(pidof gptokeyb) 2>/dev/null

if [ -d "$godot_dir" ]; then
  $ESUDO umount "$godot_dir" 2>/dev/null || true
fi

printf "\033c" > /dev/tty1
