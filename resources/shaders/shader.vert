#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec3 v_vert;
out vec3 v_norm;
out vec2 v_text;
out vec3 v_text3;

uniform mat4 lookat;
uniform mat4 projection;
uniform mat4 transform_matrix;

void main() {
    gl_Position = projection * lookat * transform_matrix * vec4(in_position,1.0);
    v_vert = vec3(transform_matrix * vec4(in_position, 1.0));
    v_norm = mat3(transpose(inverse(transform_matrix))) * in_normal;
    v_text = in_texcoord_0;
    v_text3 = in_position;
}