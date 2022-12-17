#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;
out vec3 v_vert;
out vec3 v_norm;
out vec2 v_text;
out vec3 v_text3;
uniform mat4 transform_matrix;

void main() {
    gl_Position = transform_matrix*vec4(in_position, 1.0);
    // przekazanie pozycji do
    v_vert = in_position;
    v_norm = in_normal;
    v_text = in_texcoord_0;
    v_text3 = in_position;
}