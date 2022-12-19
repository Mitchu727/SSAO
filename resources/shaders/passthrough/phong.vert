#version 330

in vec3 in_position;
in vec3 in_normal;

out vec3 frag_position;
out vec3 frag_normal;

uniform mat4 transform_matrix;
uniform mat4 view;
uniform mat4 projection;

void main() {
    // przekazanie pozycji do
    frag_position = vec3(transform_matrix * vec4(in_position, 1.0));
    frag_normal = mat3(transpose(inverse(transform_matrix))) * in_normal;

    gl_Position = projection*view*vec4(frag_position, 1.0);
}