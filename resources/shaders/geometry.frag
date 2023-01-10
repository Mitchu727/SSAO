#version 330

uniform mat4 camera_matrix;

in vec3 pos;
in vec3 normal;

layout(location=0) out float g_view_z;
layout(location=1) out vec3 g_normal;

void main() {
    // Rotate into view space, and record the z component.
    g_view_z = -(camera_matrix * vec4(pos, 1.0)).z;
    g_normal = normalize(normal);
}