#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec3 v_position;
out vec3 v_norm;
out vec2 v_text;
out vec3 v_text3;

uniform mat4 transform_matrix;
uniform mat4 view;
uniform mat4 projection;

void main() {
    v_position = vec3(transform_matrix * vec4(in_position, 1.0));
    v_norm = mat3(transpose(inverse(transform_matrix))) * in_normal;
    v_text = in_texcoord_0;
    v_text3 = in_position;
    gl_Position = projection * view * transform_matrix * vec4(v_position, 1.0);
}