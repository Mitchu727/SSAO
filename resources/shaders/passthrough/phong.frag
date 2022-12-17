#version 330

#define NR_POINT_LIGHTS 2

struct PointLight {
    vec3 color;
    vec3 position;
    float strength;
};

out vec4 f_color;
in vec3 frag_position;
in vec3 frag_normal;
uniform PointLight point_lights[NR_POINT_LIGHTS];
uniform vec3 view_position;
uniform vec3 object_color;
uniform float object_shininess;

vec3 CalculateLight(PointLight light, vec3 normal, vec3 view);

void main()
{
    vec3 result = vec3(0);
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        result += CalculateLight(point_lights[i], frag_normal, view_position);
    result *= object_color;
    f_color = vec4(result, 1.0);
}

vec3 CalculateLight(PointLight light, vec3 normal, vec3 view) {
    //ambient
    vec3 ambient = light.color * light.strength;
    //diff
    vec3 light_directory = normalize(light.position - frag_position);
    vec3 normal_vector = normalize(frag_normal);
    float diff = max(dot(normal_vector, light_directory), 0.0);
    vec3 diffuse = diff * light.color;
    //specular
    vec3 view_directory = normalize(frag_position-view_position);
    vec3 reflect_directory = reflect(light_directory, normal_vector);
    float spec = pow(max(dot(view_directory, reflect_directory), 0.0), 32);
    vec3 specular = object_shininess * spec * light.color;
    return (ambient + diffuse + specular);
}

