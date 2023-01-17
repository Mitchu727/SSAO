#version 330

uniform vec3 light_pos;
uniform vec3 camera_pos;
uniform vec3 base_color;
uniform vec4 material_properties;
uniform int render_mode;

uniform sampler2D g_view_z;
uniform sampler2D g_normal;
uniform sampler2D ssao_occlusion;
uniform sampler2D g_albedo_specular;

in vec3 view_ray;
in vec2 texcoord;

layout(location=0) out vec4 frag_color;

void main() {
    // Ignore background fragments.
    float view_z = texture(g_view_z, texcoord).x;
    if (view_z == 0.0) {
        discard;
    }

    // Load/compute the position and normal vectors (in world space).
    vec3 position = camera_pos + view_z * view_ray;
    vec3 normal = texture(g_normal, texcoord).xyz;
    vec3 Albedo = texture(g_albedo_specular, texcoord).xyz;

//    Albedo = vec3(0.5, 0.5, 0.5);
//    float Specular = texture(g_albedo_specular, TexCoords).a;

    // Compute lighting.
    float ambient_magnitude = material_properties.x;
    float diffuse_magnitude = material_properties.y;
    float specular_magnitude = material_properties.z;
    float specular_exponent = material_properties.w;

    float occlusion = texture(ssao_occlusion, texcoord).x;
    vec3 light_dir = normalize(light_pos - position);
    vec3 reflection_dir = reflect(-light_dir, normal);

    float ambient = ambient_magnitude * occlusion;
    float diffuse = diffuse_magnitude * max(dot(light_dir, normal), 0.0);
    float specular = specular_magnitude * pow(max(dot(light_dir, normal), 0.0), specular_exponent);

    float luminosity = ambient + diffuse + specular;
//    vec3 color = luminosity * base_color;
    vec3 color = luminosity * Albedo;
//    vec3 color = Albedo;
    frag_color = vec4(color, 1.0);
}
