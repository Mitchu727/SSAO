#version 330

uniform mat4 camera_matrix;
uniform sampler2D texture_diffuse;
//uniform sampler2D texture_specular;
uniform vec3 tex_color;


in vec2 texcoord;
in vec3 pos;
in vec3 normal;

layout(location=0) out float g_view_z;
layout(location=1) out vec3 g_normal;
layout(location=3) out vec4 g_albedo_specular;

void main() {
    // Rotate into view space, and record the z component.
    g_view_z = -(camera_matrix * vec4(pos, 1.0)).z;
    g_normal = normalize(normal);

    vec3 color = tex_color;

    g_albedo_specular.rgb = texture(texture_diffuse, texcoord).rgb;
//    g_albedo_specular.a = texture(texture_specular, texcoord).r;
//    g_albedo_specular.rgb = tex_color;
    g_albedo_specular.a = 1.0;
    g_albedo_specular = vec4(0.5, 0.5, 0.5, 1.0);
}