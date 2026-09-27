@echo off
title BloxRS - Teste no PC
cd /d "%~dp0"

echo ========================================================
echo   Iniciando BloxRS no PC (Godot 3.5 GLES2)...
echo.
echo   Controles no Teclado:
echo     - WASD ou Setas: Andar
echo     - Mouse: Controlar a Camera em 360 graus
echo     - Barra de Espaco: Pular
echo     - Teclas [1, 2, 3, 4]: Trocar de Mapa em Tempo Real
echo         [1] Baseplate Classica
echo         [2] Crossroads
echo         [3] Chaos Canyon
echo         [4] Happy Home in Robloxia
echo     - Tecla R: Resetar / Respawnar o Personagem
echo     - ESC: Liberar cursor / Sair
echo.
echo   Controles com Gamepad (Xbox / R35S / USB):
echo     - Analogico Esquerdo: Andar
echo     - Analogico Direito: Girar Camera
echo     - Botao A / B: Pular
echo     - Botoes L1 / R1: Trocar de Mapa
echo ========================================================
echo.

start "" "tools\Godot.exe" --path "godot_project"
