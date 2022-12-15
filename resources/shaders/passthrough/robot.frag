#version 330

uniform vec3 color;
uniform bool use_texture;
uniform sampler2D tex;

in vec3 v_vert;
in vec3 v_norm;
in vec2 v_text;

out vec4 f_color;

void main() {
    if (use_texture) {
        f_color = vec4(texture(tex, v_text).rgb, 1.0);
    } else {
        f_color = vec4(color, 1.0);
    }
}


