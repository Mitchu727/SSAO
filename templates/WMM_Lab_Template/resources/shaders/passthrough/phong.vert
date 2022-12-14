#version 330

in vec3 in_position;
in vec3 in_normal;
out vec3 frag_position;
out vec3 frag_normal;
uniform mat4 transform_matrix;

void main() {
    gl_Position = transform_matrix*vec4(in_position, 1.0);
    // przekazanie pozycji do
    frag_position = in_position;
    frag_normal = in_normal;
}