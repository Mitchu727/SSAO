#version 330

#define NR_POINT_LIGHTS 2

struct PointLight {
//    vec3 color;
    vec3 position;
//    float ambient_strength;
//    float diffuse_strength;
//    float specular_strength;
};

uniform vec3 light_pos;
uniform vec3 camera_pos;
uniform vec3 base_color;
uniform vec4 material_properties;
uniform int render_mode;

uniform sampler2D g_view_z;
uniform sampler2D g_normal;
uniform sampler2D g_albedo_specular;
uniform sampler2D ssao_occlusion;

// do świateł
uniform PointLight point_lights[NR_POINT_LIGHTS];

float calculateLight(PointLight light, vec4 material_properties, float occlusion, vec3 position, vec3 normal);

in vec3 view_ray;
in vec2 texcoord;

layout(location=0) out vec4 frag_color;

void main() {
    // Ignore background fragments
    float view_z = texture(g_view_z, texcoord).x;
    if (view_z == 0.0) {
        discard;
    }

    // Load/compute the position and normal vectors (in world space)
    vec3 position = camera_pos + view_z * view_ray;
    vec3 normal = texture(g_normal, texcoord).xyz;
    vec3 albedo = texture(g_albedo_specular, texcoord).xyz;

    float occlusion = texture(ssao_occlusion, texcoord).x;
    // Compute lighting
    //    float ambient_magnitude = material_properties.x;
    //    float diffuse_magnitude = material_properties.y;
    //    float specular_magnitude = material_properties.z;
    //    float specular_exponent = material_properties.w;
    //
//    vec3 light_dir = normalize(light_pos - position);
//    vec3 reflection_dir = reflect(-light_dir, normal);
//
//    float ambient = ambient_magnitude * occlusion;
//    float diffuse = diffuse_magnitude * max(dot(light_dir, normal), 0.0);
//    float specular = specular_magnitude * pow(max(dot(light_dir, normal), 0.0), specular_exponent);

    float luminosity = 0;
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        luminosity += calculateLight(point_lights[i], material_properties, occlusion, position, normal)/NR_POINT_LIGHTS;
    vec3 color = luminosity * albedo;
    frag_color = vec4(color, 1.0);
}

float calculateLight(PointLight light, vec4 material_properties, float occlusion, vec3 position, vec3 normal) {
    float ambient_magnitude = material_properties.x;
    float diffuse_magnitude = material_properties.y;
    float specular_magnitude = material_properties.z;
    float specular_exponent = material_properties.w;

    vec3 light_dir = normalize(light.position - position);
    vec3 reflection_dir = reflect(-light_dir, normal);

    float ambient = ambient_magnitude * occlusion;
    float diffuse = diffuse_magnitude * max(dot(light_dir, normal), 0.0);
    float specular = specular_magnitude * pow(max(dot(light_dir, normal), 0.0), specular_exponent);
    return ambient + diffuse + specular;
}