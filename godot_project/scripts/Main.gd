extends Spatial

# BloxRS - Controlador Principal com Auto-Carregador de Mapas
onready var player = $Player
onready var map_container = $Map

var maps = []
var current_map_idx = 0
var label_ui: Label = null

func _ready():
	# Cria UI de informações no topo
	var canvas = CanvasLayer.new()
	add_child(canvas)
	
	label_ui = Label.new()
	label_ui.rect_position = Vector2(10, 10)
	label_ui.text = "BloxRS | Mapa: Baseplate (1/4) | L1/R1: Trocar Mapa"
	canvas.add_child(label_ui)

	# Escaneia mapas disponíveis
	scan_available_maps()

	# Inicia capturando o mouse apenas no PC (Windows)
	if OS.get_name() == "Windows":
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func scan_available_maps():
	maps.clear()
	
	# 1. Mapas Padrão Embutidos
	var defaults = [
		["Baseplate", "res://scenes/Baseplate.tscn"],
		["Crossroads", "res://scenes/Crossroads.tscn"],
		["Chaos Canyon", "res://scenes/ChaosCanyon.tscn"],
		["Happy Home", "res://scenes/HappyHome.tscn"]
	]
	for d in defaults:
		if ResourceLoader.exists(d[1]):
			maps.append({"name": d[0], "path": d[1]})
			
	# 2. Mapas convertidos dinamicamente no R35S / user://maps/
	var dir = Directory.new()
	if dir.open("user://maps") == OK:
		dir.list_dir_begin(true)
		var file_name = dir.get_next()
		while file_name != "":
			if file_name.ends_with(".tscn"):
				var display_name = file_name.replace(".tscn", "").capitalize()
				maps.append({"name": display_name, "path": "user://maps/" + file_name})
			file_name = dir.get_next()
		dir.list_dir_end()
		
	print("[BloxRS] Total de mapas disponíveis: ", maps.size())
	if maps.size() > 0 and label_ui:
		label_ui.text = "BloxRS | Mapa: " + maps[0]["name"] + " (1/" + str(maps.size()) + ") | L1/R1: Trocar"

func _unhandled_input(event):
	if OS.get_name() == "Windows":
		if event is InputEventMouseButton and event.pressed:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _process(_delta):
	# SAÍDA SEGURA NO R35S:
	# Apenas sai se segurar SELECT + START juntos (Joypad 10 e 11)
	# Isso evita que o jogo feche sozinho se o usuário apertar A ou B ao iniciar!
	if Input.is_joy_button_pressed(0, 10) and Input.is_joy_button_pressed(0, 11):
		get_tree().quit()

	# No PC: tecla ESC sai ou libera o mouse
	if Input.is_key_pressed(KEY_ESCAPE) and OS.get_name() == "Windows":
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		else:
			get_tree().quit()

	# Troca de mapas pelos botões L1 / R1 do controle ou Q / E do teclado
	if Input.is_joy_button_just_pressed(0, 4) or Input.is_action_just_pressed("ui_left") or Input.is_key_pressed(KEY_Q):
		change_map(-1)
	elif Input.is_joy_button_just_pressed(0, 5) or Input.is_action_just_pressed("ui_right") or Input.is_key_pressed(KEY_E):
		change_map(1)

	# Teclas numéricas 1 a 9 no teclado do PC
	for i in range(min(9, maps.size())):
		if Input.is_key_pressed(KEY_1 + i):
			load_map(i)

func change_map(offset: int):
	if maps.empty(): return
	var next_idx = (current_map_idx + offset + maps.size()) % maps.size()
	load_map(next_idx)

func load_map(idx: int):
	if idx < 0 or idx >= maps.size(): return
	current_map_idx = idx
	var map_info = maps[idx]
	
	print("[BloxRS] Carregando mapa: ", map_info["name"])
	
	# Remove mapa atual
	for child in map_container.get_children():
		child.queue_free()
	
	# Carrega a cena
	var scene_res = load(map_info["path"])
	if scene_res:
		var new_map = scene_res.instance()
		map_container.add_child(new_map)
		
		# Posiciona o jogador em cima do mapa com segurança
		player.global_transform.origin = Vector3(0, 10, 0)
		player.velocity = Vector3.ZERO
		
		if label_ui:
			label_ui.text = "BloxRS | Mapa: " + map_info["name"] + " (" + str(idx+1) + "/" + str(maps.size()) + ") | L1/R1: Trocar | Select+Start: Sair"
