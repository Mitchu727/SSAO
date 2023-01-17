#version 330

uniform mat4 camera_matrix;
uniform mat4 projection_matrix;
uniform mat4 transform_matrix;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 texcoord;
out vec3 pos;
out vec3 normal;

void main() {
    gl_Position = projection_matrix * camera_matrix * transform_matrix * vec4(in_position,1.0);
    pos = vec3(transform_matrix * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(transform_matrix))) * in_normal;
    texcoord = in_texcoord_0;
}
