extends KinematicBody

# BloxRS - Classic Roblox Character Controller for R35S
export var speed: float = 16.0
export var jump_force: float = 22.0
export var gravity: float = 55.0
export var stick_look_speed: float = 3.5
export var mouse_sensitivity: float = 0.003

var velocity: Vector3 = Vector3.ZERO
var spawn_position: Vector3 = Vector3(0, 5, 0)
var anim_time: float = 0.0

onready var camera_pivot = $CameraPivot
onready var camera = $CameraPivot/SpringArm/Camera
onready var model = $CharacterModel
onready var left_arm = $CharacterModel/LeftArmPivot
onready var right_arm = $CharacterModel/RightArmPivot
onready var left_leg = $CharacterModel/LeftLegPivot
onready var right_leg = $CharacterModel/RightLegPivot

func _ready():
    spawn_position = global_transform.origin

func _input(event):
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
        camera_pivot.rotate_x(-event.relative.y * mouse_sensitivity)
        camera_pivot.rotation.x = clamp(camera_pivot.rotation.x, deg2rad(-75), deg2rad(75))

func _physics_process(delta):
    # Respawn if falling into void
    if global_transform.origin.y < -30.0 or Input.is_action_just_pressed("reset_player"):
        global_transform.origin = spawn_position
        velocity = Vector3.ZERO
        return

    # --- 1. Movement Input (Left Stick / D-Pad / WASD) ---
    var move_x = Input.get_action_strength("move_right") - Input.get_action_strength("move_left")
    var move_z = Input.get_action_strength("move_back") - Input.get_action_strength("move_forward")
    var raw_input = Vector2(move_x, move_z)
    if raw_input.length() > 1.0:
        raw_input = raw_input.normalized()

    # --- 2. Camera Input (Right Stick / Arrow Keys) ---
    var look_x = Input.get_action_strength("look_right") - Input.get_action_strength("look_left")
    var look_y = Input.get_action_strength("look_down") - Input.get_action_strength("look_up")
    
    if abs(look_x) > 0.15:
        rotate_y(-look_x * stick_look_speed * delta)
    if abs(look_y) > 0.15:
        camera_pivot.rotate_x(-look_y * stick_look_speed * delta)
        camera_pivot.rotation.x = clamp(camera_pivot.rotation.x, deg2rad(-75), deg2rad(75))

    # --- 3. Velocity Calculation ---
    var move_dir = (transform.basis.x * raw_input.x + transform.basis.z * raw_input.y)
    velocity.x = move_dir.x * speed
    velocity.z = move_dir.z * speed

    # Gravity
    if not is_on_floor():
        velocity.y -= gravity * delta
    else:
        velocity.y = -0.5
        if Input.is_action_just_pressed("jump"):
            velocity.y = jump_force

    velocity = move_and_slide(velocity, Vector3.UP, true)

    # --- 4. Authentic Procedural Limb Swing Animation ---
    var horizontal_speed = Vector2(velocity.x, velocity.z).length()
    var is_moving = horizontal_speed > 1.0 and is_on_floor()

    if is_moving:
        anim_time += delta * 12.0
        var swing = sin(anim_time) * 0.75
        left_arm.rotation.x = swing
        right_arm.rotation.x = -swing
        left_leg.rotation.x = -swing
        right_leg.rotation.x = swing
    else:
        # Return smoothly to neutral standing pose
        anim_time = 0.0
        left_arm.rotation.x = lerp(left_arm.rotation.x, 0.0, delta * 10.0)
        right_arm.rotation.x = lerp(right_arm.rotation.x, 0.0, delta * 10.0)
        left_leg.rotation.x = lerp(left_leg.rotation.x, 0.0, delta * 10.0)
        right_leg.rotation.x = lerp(right_leg.rotation.x, 0.0, delta * 10.0)
