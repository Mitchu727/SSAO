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

vec3 calculateLight(PointLight light);
vec3 getColor();

void main()
{
    vec3 color = getColor();
    vec3 light = vec3(0);
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        light += calculateLight(point_lights[i]);
    vec3 result = color*light;
    f_color = vec4(result, 1.0);
}

vec3 GetColor() {
    vec3 color;
    switch (use_texture) {
        case 0:
            color = vec3(object_color);
            break;
        case 1:
            vec2 tex_coord = vec2(v_text/texture_scale);
            color = vec3(texture(tex, tex_coord).rgb);
            break;
        case 2:
            color = vec3(texture(texCube, v_text3).rgb);
            break;
    }
    return color;
}

vec3 CalculateLight(PointLight light) {
    vec3 light_direction = normalize(light.position - v_vert);
    vec3 reflect_direction = reflect(-light_direction, v_norm);
    vec3 view_direction = normalize(view_position - v_vert);

    float diff = max(dot(v_norm, light_direction), 0.0);
    float spec = max(dot(view_direction, reflect_direction), 0.0);

    vec3 ambient_color = light.color * light.strength;
    vec3 diffuse_color = diff * light.color;
    vec3 specular_color = pow(spec, 32.) * object_shininess * light.color;

    return ambient_color + diffuse_color;
}

