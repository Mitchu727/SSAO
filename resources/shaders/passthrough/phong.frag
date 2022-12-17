#version 330

#define NR_POINT_LIGHTS 1

struct PointLight {
    vec3 color;
    vec3 position;
    float strength;
};

out vec4 f_color;

in vec3 v_vert;
in vec3 v_norm;
in vec2 v_text;
in vec3 v_text3;

// do tekstur
uniform int use_texture;
uniform sampler2D tex;
uniform samplerCube texCube;
uniform float texture_scale;
// do świateł
uniform PointLight point_lights[NR_POINT_LIGHTS];
uniform vec3 view_position;
uniform vec3 object_color;
uniform float object_shininess;

vec3 CalculateLight(PointLight light, vec3 normal, vec3 view);

void main()
{
    vec3 color;
    switch (use_texture) {
        case 0:
            color = vec3(object_color);
            break;
        case 1:
            vec2 tex_coord = vec2(v_text[0]/texture_scale, v_text[1]/texture_scale);
            color = vec3(texture(tex, tex_coord).rgb);
            break;
        case 2:
            color = vec3(texture(texCube, v_text3).rgb);
            break;
    }

    vec3 light = vec3(0);
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        light += CalculateLight(point_lights[i], v_norm, view_position);
    vec3 result = color*light;
    f_color = vec4(result, 1.0);
}

vec3 CalculateLight(PointLight light, vec3 normal, vec3 view) {
    //ambient
    vec3 ambient = light.color * light.strength;
    //diff
    vec3 light_directory = normalize(light.position - v_vert);
    vec3 normal_vector = normalize(normal);
    float diff = max(dot(normal_vector, light_directory), 0.0);
    vec3 diffuse = diff * light.color;
    //specular
    vec3 view_directory = normalize(v_vert-view_position);
    vec3 reflect_directory = reflect(light_directory, normal_vector);
    float spec = pow(max(dot(view_directory, reflect_directory), 0.0), 32);
    vec3 specular = object_shininess * spec * light.color;
    return (diffuse);
}

