class PointLight:
    def __init__(self, color, position, value):
        self.color = color
        self.position = position
        self.strength = value


def lights_from_open_gl(program, NR_POINT_LIGHTS):
    point_lights = []
    for i in range(NR_POINT_LIGHTS):
        point_lights.append(
            PointLight(
                program[f"point_lights[{i}].color"],
                program[f"point_lights[{i}].position"],
                program[f"point_lights[{i}].strength"]
            )
        )
    return point_lights
