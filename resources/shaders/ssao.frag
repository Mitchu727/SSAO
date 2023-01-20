#version 330

const int MAX_SSAO_SAMPLES_QUANTITY = 100;

uniform vec3 f_camera_pos;
uniform mat4 mvp;
uniform int n_samples;
uniform vec3 samples[MAX_SSAO_SAMPLES_QUANTITY];
uniform float z_offset;

uniform sampler2D g_view_z;
uniform sampler2D g_norm;
uniform sampler2D noise;

in vec3 view_ray;
in vec2 texcoord;

layout(location=0) out float occlusion;

void main() {
    // Ignore background fragments.
    float f_view_z = texture(g_view_z, texcoord).x;
    if (f_view_z == 0.0) {
        discard;
    }

    // Load/compute the position and normal vectors (in world coordinates).
    vec3 f_pos = f_camera_pos + f_view_z * view_ray;
    vec3 f_norm = texture(g_norm, texcoord).xyz;
    // Compute the rotation matrix that takes us from tangent space to world space.
    // Note that the x and y axes in tangent space aren't aligned with the texture coordinates or
    // anything -- they are intentionally randomized to decorrelate our samples in nearby pixels.
    const int noise_size = 32;
    vec2 noise_pos = (1.0 / float(noise_size)) * vec2(
        float(mod(gl_FragCoord.x, noise_size)),
        float(mod(gl_FragCoord.y, noise_size))
    );
    vec3 random_vec = normalize(texture(noise, noise_pos).xyz);
    vec3 tangent_x = normalize(random_vec - f_norm * dot(random_vec, f_norm));
    vec3 tangent_y = cross(f_norm, tangent_x);
    mat3 tan_to_world = mat3(tangent_x, tangent_y, f_norm);

    // Measure occlusion.
    occlusion = 0.0;
    for (int i = 0; i < n_samples; ++i) {
        // Compute the sample position in world coordinates.
        vec3 sample_offset = tan_to_world * samples[i];
        vec4 sample_pos = vec4(f_pos + sample_offset, 1.0);

        // Convert to clip space, then scale the relevant coordinates to the range [0, 1].
        sample_pos = mvp * sample_pos;
        sample_pos.xyz /= sample_pos.w;
        sample_pos.xy = 0.5 * sample_pos.xy + 0.5;

        // Read the actual depth at the sample point.
        float actual_view_z = texture(g_view_z, sample_pos.xy).x;

        // If the actual depth is less than the depth of the sample point, the sample is occluded.
        occlusion += (actual_view_z != 0.0 && actual_view_z + z_offset < f_view_z) ? 1.0 : 0.0;
    }
    occlusion = 1.0 - (1.0 / float(n_samples)) * occlusion;
}