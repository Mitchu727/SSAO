#version 330

uniform mat4 camera_matrix;
uniform sampler2D texture_diffuse;
//uniform sampler2D texture_specular;
uniform vec3 tex_color;

// do tekstur
uniform int use_texture;
uniform sampler2D tex;
uniform samplerCube texCube;
uniform float texture_scale;
uniform vec3 object_color;


in vec2 texcoord;
in vec3 pos;
in vec3 normal;

layout(location=0) out float g_view_z;
layout(location=1) out vec3 g_normal;
layout(location=2) out vec4 g_albedo_specular;
//layout(location=3) out vec4 g_albedo_specular;

vec4 getColor();


void main() {
    // Rotate into view space, and record the z component.
    g_view_z = -(camera_matrix * vec4(pos, 1.0)).z;
    g_normal = normalize(normal);

    vec3 color = tex_color;

//    g_albedo_specular.rgb = texture(texture_diffuse, texcoord).rgb;
//    g_albedo_specular.a = texture(texture_specular, texcoord).r;
    g_albedo_specular = getColor();
//    g_albedo_specular.a = 1.0;
//    g_albedo_specular = vec4(1.0, 1.0, 1.0, 0.5);
//    g_albedo_specular = g_view_z;
}

vec4 getColor() {
    vec4 color;
    switch (use_texture) {
        case 0:
            color = vec4(object_color, 1.0);
            break;
        case 1:
            color = texture(tex, texcoord/texture_scale).rgba;
            break;
        case 2:
            color = texture(texCube, pos).rgba;
            break;
    }
    return color;
}