shader_type spatial;
render_mode cull_back, diffuse_lambert;

uniform vec4 albedo_color : hint_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform sampler2D top_texture : hint_albedo;
uniform sampler2D bottom_texture : hint_albedo;
uniform sampler2D side_texture : hint_albedo;
uniform float uv_scale = 0.5;

void fragment() {
    vec3 world_pos = (CAMERA_MATRIX * vec4(VERTEX, 1.0)).xyz;
    vec3 world_norm = normalize((CAMERA_MATRIX * vec4(NORMAL, 0.0)).xyz);
    
    vec4 tex_sample;
    if (world_norm.y > 0.55) {
        tex_sample = texture(top_texture, world_pos.xz * uv_scale);
    } else if (world_norm.y < -0.55) {
        tex_sample = texture(bottom_texture, world_pos.xz * uv_scale);
    } else {
        if (abs(world_norm.x) > abs(world_norm.z)) {
            tex_sample = texture(side_texture, world_pos.zy * uv_scale);
        } else {
            tex_sample = texture(side_texture, world_pos.xy * uv_scale);
        }
    }
    
    ALBEDO = albedo_color.rgb * tex_sample.rgb;
    ROUGHNESS = 0.6;
    SPECULAR = 0.2;
}
