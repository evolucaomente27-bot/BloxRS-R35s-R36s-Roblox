#!/usr/bin/env python3
"""
BloxRS Map Converter v2.0 - com suporte completo a Texturas e Cores Clássicas
Converte mapas XML (.rbxl / .rbxlx) para Godot 3.5 com Studs, Materiais e Cores Originais.
"""

import sys
import os
import xml.etree.ElementTree as ET

# Importa tabela de cores clássicas
from brick_colors import ROBLOX_BRICKCOLORS

TEXTURE_MAP = {
    "studs": ("res://assets/textures/studs.png", 1),
    "brick": ("res://assets/textures/brick.png", 2),
    "wood": ("res://assets/textures/wood.png", 3),
    "grass": ("res://assets/textures/grass.png", 4),
    "concrete": ("res://assets/textures/concrete.png", 5),
    "diamond_plate": ("res://assets/textures/diamond_plate.png", 6),
    "slate": ("res://assets/textures/slate.png", 7),
}

MATERIAL_CODE_MAP = {
    "256": "studs",         # Plastic
    "512": "wood",          # Wood
    "768": "slate",         # Slate
    "800": "concrete",      # Concrete
    "816": "diamond_plate", # CorrodedMetal
    "832": "diamond_plate", # DiamondPlate
    "848": "diamond_plate", # Foil
    "864": "grass",         # Grass
    "880": "studs",         # Ice
    "896": "brick",         # Brick
    "912": "concrete",      # Sand
    "1056": "slate",        # Cobblestone
    "1072": "wood",         # WoodPlanks
}

def parse_vector3(node):
    if node is None:
        return (4.0, 1.2, 2.0)
    x = float(node.findtext("X", "0"))
    y = float(node.findtext("Y", "0"))
    z = float(node.findtext("Z", "0"))
    return (x, y, z)

def parse_cframe(node):
    if node is None:
        return (0.0, 0.0, 0.0, [1, 0, 0, 0, 1, 0, 0, 0, 1])
    px = float(node.findtext("X", "0"))
    py = float(node.findtext("Y", "0"))
    pz = float(node.findtext("Z", "0"))
    
    r00 = float(node.findtext("R00", "1"))
    r01 = float(node.findtext("R01", "0"))
    r02 = float(node.findtext("R02", "0"))
    r10 = float(node.findtext("R10", "0"))
    r11 = float(node.findtext("R11", "1"))
    r12 = float(node.findtext("R12", "0"))
    r20 = float(node.findtext("R20", "0"))
    r21 = float(node.findtext("R21", "0"))
    r22 = float(node.findtext("R22", "1"))
    
    return (px, py, pz, [r00, r01, r02, r10, r11, r12, r20, r21, r22])

def convert_rbxl_to_godot(xml_path, output_tscn_path):
    print(f"[*] Processando mapa com texturas: {xml_path}")
    tree = ET.parse(xml_path)
    root = tree.getroot()

    parts = []
    unique_materials = {} # (color_id, texture_key, transparency) -> subresource_id
    subres_counter = 1

    for item in root.iter("Item"):
        item_class = item.get("class", "")
        if item_class in ("Part", "WedgePart", "SpawnLocation", "TrussPart", "CornerWedgePart"):
            props = item.find("Properties")
            if props is None:
                continue
                
            name = "Part"
            color_id = 194
            mat_raw = "256"
            transparency = 0.0
            size = (4.0, 1.2, 2.0)
            cframe = (0.0, 0.0, 0.0, [1, 0, 0, 0, 1, 0, 0, 0, 1])

            for child in props:
                prop_name = child.get("name")
                if prop_name == "Name":
                    name = child.text or "Part"
                elif prop_name == "BrickColor":
                    try:
                        color_id = int(child.text or "194")
                    except ValueError:
                        color_id = 194
                elif prop_name == "Material":
                    mat_raw = (child.text or "256").strip()
                elif prop_name == "Transparency":
                    try:
                        transparency = float(child.text or "0.0")
                    except ValueError:
                        transparency = 0.0
                elif prop_name in ("size", "Size"):
                    size = parse_vector3(child)
                elif prop_name == "CFrame":
                    cframe = parse_cframe(child)

            # Determina a textura
            texture_key = MATERIAL_CODE_MAP.get(mat_raw, "studs")
            
            # Se a cor for verde grama clássica (141, 37, 28) e sem material definido, dá textura de grass ou studs
            if color_id in (37, 141) and texture_key == "studs" and size[0] > 10 and size[2] > 10:
                texture_key = "grass"

            # Registra material único
            mat_key = (color_id, texture_key, round(transparency, 2))
            if mat_key not in unique_materials:
                unique_materials[mat_key] = subres_counter
                subres_counter += 1

            pos_x, pos_y, pos_z, rot = cframe
            parts.append({
                "name": name,
                "size": size,
                "pos": (pos_x, pos_y, pos_z),
                "rot": rot,
                "mat_id": unique_materials[mat_key],
            })

    print(f"[+] Total de partes: {len(parts)} | Materiais texturizados unicos: {len(unique_materials)}")
    if len(parts) == 0:
        print("[!] Nenhuma parte encontrada.")
        return

    # Monta o arquivo .tscn
    load_steps = len(TEXTURE_MAP) + len(unique_materials) + 1
    tscn = []
    tscn.append(f'[gd_scene load_steps={load_steps} format=2]')
    tscn.append('')

    # ExtResources (as texturas)
    for tex_key, (tex_path, ext_id) in TEXTURE_MAP.items():
        tscn.append(f'[ext_resource path="{tex_path}" type="Texture" id={ext_id}]')
    tscn.append('')

    # SubResources (os materiais combinando cada cor e textura)
    for (color_id, texture_key, transp), mat_id in unique_materials.items():
        rgb = ROBLOX_BRICKCOLORS.get(color_id, (0.64, 0.64, 0.65))
        _, ext_id = TEXTURE_MAP[texture_key]
        alpha = max(0.0, min(1.0, 1.0 - transp))

        tscn.append(f'[sub_resource type="SpatialMaterial" id={mat_id}]')
        if transp > 0.05:
            tscn.append('flags_transparent = true')
        tscn.append(f'albedo_color = Color( {rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f}, {alpha:.3f} )')
        tscn.append(f'albedo_texture = ExtResource( {ext_id} )')
        tscn.append('uv1_scale = Vector3( 0.5, 0.5, 0.5 )')
        tscn.append('uv1_triplanar = true')
        tscn.append('roughness = 0.75')
        tscn.append('')

    # Estrutura dos Nós
    tscn.append('[node name="RobloxMap" type="Spatial"]')
    tscn.append('')

    for idx, p in enumerate(parts):
        node_name = f"P_{idx}"
        sx, sy, sz = p["size"]
        px, py, pz = p["pos"]
        r = p["rot"]
        mat_id = p["mat_id"]

        tscn.append(f'[node name="{node_name}" type="StaticBody" parent="."]')
        tscn.append(f'transform = Transform( {r[0]:.4f}, {r[1]:.4f}, {r[2]:.4f}, {r[3]:.4f}, {r[4]:.4f}, {r[5]:.4f}, {r[6]:.4f}, {r[7]:.4f}, {r[8]:.4f}, {px:.3f}, {py:.3f}, {pz:.3f} )')
        tscn.append('')
        tscn.append(f'[node name="MeshInstance" type="CSGBox" parent="{node_name}"]')
        tscn.append(f'width = {sx:.3f}')
        tscn.append(f'height = {sy:.3f}')
        tscn.append(f'depth = {sz:.3f}')
        tscn.append('use_collision = true')
        tscn.append(f'material = SubResource( {mat_id} )')
        tscn.append('')

    with open(output_tscn_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tscn))

    print(f"[OK] Mapa texturizado exportado com sucesso para: {output_tscn_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python convert_rbxl.py <arquivo.rbxl> [saida.tscn]")
        sys.exit(1)
        
    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(in_file)[0] + ".tscn"
    convert_rbxl_to_godot(in_file, out_file)
