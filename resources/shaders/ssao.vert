#version 330

uniform mat4 m_camera_inverse;
uniform mat4 m_projection_inverse;
uniform vec3 v_camera_pos;

in vec3 in_position;
in vec2 in_texcoord_0;

out vec3 view_ray;
out vec2 texcoord;

void main() {
    gl_Position = vec4(in_position, 1.0);

    // Convert in_position from clip space to view space.
    vec4 pos = m_projection_inverse * vec4(in_position, 1.0);
    // Normalize its z value.
    pos.xy /= -pos.z;
    pos.z = -1.0;
    pos.w = 1.0;
    // Convert to world space.
    pos = m_camera_inverse * pos;
    view_ray = pos.xyz - v_camera_pos;

    texcoord = in_texcoord_0;
}
