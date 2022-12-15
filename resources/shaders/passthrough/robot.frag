#version 330

uniform vec3 color;
uniform int use_texture;
uniform sampler2D tex;
uniform samplerCube texCube;
uniform float texture_scale;

in vec3 v_vert;
in vec3 v_norm;
in vec2 v_text;
in vec3 v_text3;

out vec4 f_color;

void main() {
    switch (use_texture) {
        case 0:
            f_color = vec4(color, 1.0);
            break;
        case 1:
            vec2 tex_coord = vec2(v_text[0]/texture_scale, v_text[1]/texture_scale);
            f_color = vec4(texture(tex, tex_coord).rgb, 1.0);
            break;
        case 2:
            f_color = vec4(texture(texCube, v_text3).rgb, 1.0);
            break;
    }
}


