class PointLight:
    def __init__(self, color, position, ambient_strength, diffuse_strength, specular_strength):
        self.color = color
        self.position = position
        self.ambient_strength = ambient_strength
        self.diffuse_strength = diffuse_strength
        self.specular_strength = specular_strength


def lights_from_open_gl(program, nr_point_light):
    point_lights = []
    for i in range(nr_point_light):
        point_lights.append(
            PointLight(
                program[f"point_lights[{i}].color"],
                program[f"point_lights[{i}].position"],
                program[f"point_lights[{i}].ambient_strength"],
                program[f"point_lights[{i}].diffuse_strength"],
                program[f"point_lights[{i}].specular_strength"]
            )
        )
    return point_lights
