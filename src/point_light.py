class PointLight:
    def __init__(self, position):
        self.position = position


def lights_from_open_gl(program, nr_point_light):
    point_lights = []
    for i in range(nr_point_light):
        point_lights.append(PointLight(program[f"point_lights[{i}].position"]))
    return point_lights
