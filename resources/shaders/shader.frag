#version 330

#define NR_POINT_LIGHTS 1
#define KERNEL_SIZE 64

float radius = 0.5;
float bias = 0.025;

struct PointLight {
    vec3 color;
    vec3 position;
    float ambient_strength;
    float diffuse_strength;
    float specular_strength;
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

uniform mat4 projection;
uniform vec3 samples[KERNEL_SIZE];

vec3 calculateLight(PointLight light);
vec4 getColor();

void main()
{
    vec4 object_color = getColor();
    vec3 light = vec3(0);

    // get input for SSAO algorithm
//    vec3 fragPos = texture(gPosition, TexCoords).xyz;
//    vec3 normal = normalize(texture(gNormal, TexCoords).rgb);
//    vec3 randomVec = normalize(texture(texNoise, TexCoords * noiseScale).xyz);

    vec3 fragPos = v_vert.xyz;
    vec3 normal = normalize(v_norm.rgb);
    vec3 randomVec = vec3(0);
    // create TBN change-of-basis matrix: from tangent-space to view-space
    vec3 tangent = normalize(randomVec - normal * dot(randomVec, normal));
    vec3 bitangent = cross(normal, tangent);
    mat3 TBN = mat3(tangent, bitangent, normal);

    float occlusion = 0.0;
    for(int i = 0; i < KERNEL_SIZE; ++i)
    {
        // get sample position
        vec3 samplePos = TBN * samples[i]; // from tangent to view-space
        samplePos = fragPos + samplePos * radius;

        // project sample position (to sample texture) (to get position on screen/texture)
        vec4 offset = vec4(samplePos, 1.0);
        offset = projection * offset; // from view to clip-space
        offset.xyz /= offset.w; // perspective divide
        offset.xyz = offset.xyz * 0.5 + 0.5; // transform to range 0.0 - 1.0

        // get sample depth
//        float sampleDepth = texture(v_vert.xyz, offset.xy).z; // get depth value of kernel sample

        vec4 offsetPosition = texture(v_vert, offsetUV.xy);

        // range check & accumulate
        float rangeCheck = smoothstep(0.0, 1.0, radius / abs(fragPos.z - sampleDepth));
        occlusion += (sampleDepth >= samplePos.z + bias ? 1.0 : 0.0) * rangeCheck;
    }
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        light += calculateLight(point_lights[i]);
    f_color = vec4(vec3(0.55) * light, 1.0);
}

vec4 getColor() {
    vec4 color;
    switch (use_texture) {
        case 0:
            color = vec4(object_color, 1.0);
            break;
        case 1:
            color = texture(tex, v_text/texture_scale).rgba;
            break;
        case 2:
            color = texture(texCube, v_text3).rgba;
            break;
    }
    return color;
}

vec3 calculateLight(PointLight light) {
    vec3 light_direction = normalize(light.position - v_vert);
    vec3 reflect_direction = reflect(-light_direction, v_norm);
    vec3 view_direction = normalize(view_position - v_vert);

    float diff = max(dot(v_norm, light_direction), 0.0);
    float spec = max(dot(view_direction, reflect_direction), 0.0);

    vec3 ambient_color = light.color * light.ambient_strength;
    vec3 diffuse_color = diff * light.color * light.diffuse_strength;
    vec3 specular_color = diff <= 0 ? vec3(0) : pow(spec, 64.) * object_shininess * light.color * light.specular_strength;

    return clamp(ambient_color + diffuse_color + specular_color, 0.0, 1.0);
}

