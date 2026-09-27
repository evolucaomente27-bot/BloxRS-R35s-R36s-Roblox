@echo off
title Abrir Projeto no Editor Godot 3.5
cd /d "%~dp0"
start "" "tools\Godot.exe" -e --path "godot_project"
