#version 330

out vec4 f_color;
in vec3 frag_position;
in vec3 frag_normal;
uniform vec3 light_color;
uniform vec3 light_position;
uniform vec3 object_color;
uniform float object_shininess;
uniform float light_strength;

void main()
{
    // oświetlenie ambient
    vec3 ambient = light_color * light_strength;
    //diffuse
    vec3 light_directory = normalize(light_position - frag_position);
    vec3 normal_vector = normalize(frag_normal);
    // obliczenie iloczynu skalarnego pomiędzy padającym promieniem, a wektorem prostopadłym do płaszczyzny
    float diff = max(dot(light_directory, normal_vector), 0.0);
    vec3 diffuse = diff * light_color;

    //specular
    //   UWAGA  zakładam, że view_position to 0,0,0
    vec3 view_directory = normalize(-frag_position);
    vec3 reflect_directory = reflect(light_directory, normal_vector);
    //obliczenie iloczynu skalarnego pomiędzy promieniem dochodzącym do obserwatora, a prominiem odbitym
    float spec = pow(max(dot(view_directory, reflect_directory), 0.0), 32);
    vec3 specular = object_shininess * spec * light_color;

    //dodanie oświetleń do siebie
    vec3 result = (ambient + diffuse) * object_color + specular;
    f_color = vec4(result, 1.0);
}



