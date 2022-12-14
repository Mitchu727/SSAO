#version 330

in vec3 in_position;
uniform mat4 transform_matrix;

void main() {
    gl_Position = transform_matrix*vec4(in_position, 1.0);
}