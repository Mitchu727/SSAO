#version 330

#define NR_POINT_LIGHTS 1

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

// SSAO
uniform float samples[192];

in vec2 var_UV;

uniform sampler2D uni_texture0;  // gPosition
uniform sampler2D uni_texture1;  // gNormal
uniform sampler2D uni_texture2;  // texNoise
uniform int kernelSize;
uniform float radius;
uniform float bias;
const vec2 noiseScale = vec2(1280.0/4.0, 720.0/4.0);
uniform mat4 uni_P;

// Functions
float rand(vec2 co){
  return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

vec3 calculateLight(PointLight light);
vec4 getColor();
float calculateSSAO();

void main()
{
    vec4 object_color = getColor();
    vec3 light = vec3(0);
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        light += calculateLight(point_lights[i]);
    f_color = vec4(object_color.xyz * light, object_color.a);
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

    vec3 ambient_color = light.color * light.ambient_strength * calculateSSAO();
    vec3 diffuse_color = diff * light.color * light.diffuse_strength;
    vec3 specular_color = diff <= 0 ? vec3(0) : pow(spec, 64.) * object_shininess * light.color * light.specular_strength;

    return clamp(ambient_color + diffuse_color + specular_color, 0.0, 1.0);
}

float calculateSSAO() {
    vec3 fragPos = v_vert;
    vec3 normal = v_norm;
    vec3 randomVec = texture(uni_texture2, var_UV * noiseScale).xyz;

    vec3 tangent = normalize(randomVec - normal * dot(randomVec, normal));
    vec3 bitangent = cross(normal, tangent);
    mat3 TBN = mat3(tangent, bitangent, normal);

    float occlusion = 0.0;

	for(int i = 0; i < kernelSize * 3; i += 3) {
		vec3 x = vec3(samples[i], samples[i + 1], samples[i + 2]);
		x = TBN * x;
		x = fragPos + x * radius;

		vec4 offset = vec4(x, 1.0);
		offset = uni_P * offset;
		offset.xyz /= offset.w;
		offset.xyz  = offset.xyz * 0.5 + 0.5;

		float sampleDepth = texture(uni_texture0, offset.xy).z;

		float rangeCheck = smoothstep(0.0, 1.0, radius / abs(fragPos.z - sampleDepth));

		occlusion += (sampleDepth >= x.z + bias ? 1.0 : 0.0) * rangeCheck;
	}
    occlusion = 1.0 - (occlusion / kernelSize);

    return occlusion;
}