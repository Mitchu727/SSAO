#version 330

uniform vec3 color;
uniform bool useTexture;
uniform sampler2D Texture;

in vec3 v_vert;
in vec3 v_norm;
in vec2 v_text;

out vec4 f_color;

void main() {
    if (useTexture) {
        f_color = vec4(texture(Texture, v_text).rgb, 1.0);
    } else {
        f_color = vec4(color, 1.0);
    }
}


