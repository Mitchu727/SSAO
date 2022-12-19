import moderngl
import numpy as np
from pyrr import Matrix44, Vector3, vector, matrix33

from base_window import BaseWindowConfig
from point_light import lights_from_open_gl


class SSAOWindow(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(SSAOWindow, self).__init__(**kwargs)
        self.camera_pos = Vector3([15.0, 0.0, 0.0])
        self.camera_target = Vector3([-1.0, 0, 0.0])
        self.camera_up = Vector3([0.0, 0, 1.0])
        self.camera_moving_speed = 0.1
        self.camera_rotation_speed = 0.1

    def unicode_char_entered(self, char: str):
        forward = self.camera_target
        side = vector.normalize(np.cross(forward, self.camera_up))
        up = vector.normalize(np.cross(side, forward))

        if char.lower() == "w":
            self.camera_pos += forward * self.camera_moving_speed
        if char.lower() == "s":
            self.camera_pos -= forward * self.camera_moving_speed
        if char.lower() == "d":
            self.camera_pos += side * self.camera_moving_speed
        if char.lower() == "a":
            self.camera_pos -= side * self.camera_moving_speed
        if char.lower() == "q":
            self.camera_pos += up * self.camera_moving_speed
        if char.lower() == "z":
            self.camera_pos -= up * self.camera_moving_speed
        print(f"New camera position: {self.camera_pos}")

    def mouse_position_event(self, x, y, dx, dy):
        z_rotation_matrix = matrix33.create_from_z_rotation(np.pi / 180 * self.camera_moving_speed * dx)

        self.camera_target = vector.normalize(matrix33.apply_to_vector(z_rotation_matrix, self.camera_target))
        self.camera_up = vector.normalize(matrix33.apply_to_vector(z_rotation_matrix, self.camera_up))

        side = vector.normalize(np.cross(self.camera_target, self.camera_up))
        side_rotation = matrix33.create_from_axis_rotation(side, -np.pi / 180 * self.camera_moving_speed * dy)

        self.camera_target = vector.normalize(matrix33.apply_to_vector(side_rotation, self.camera_target))
        self.camera_up = vector.normalize(matrix33.apply_to_vector(side_rotation, self.camera_up))
        print(f"New camera vector: {self.camera_target}")

    def model_load(self):
        # wczytanie obiektów do późniejszego renderowania
        self.sphere = self.load_scene("sphere.obj").root_nodes[0].mesh.vao.instance(self.program)
        self.cube = self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        self.teapot = self.load_scene("teapot.obj").root_nodes[0].mesh.vao.instance(self.program)

    def init_shaders_variables(self):
        self.transform_matrix = self.program['transform_matrix']  # przekształcenie obiektu pierwotnego
        # self.model = self.program['model']  # przekształcenie obiektu pierwotnego
        self.projection = self.program['projection']
        self.view = self.program['view']
        self.object_color = self.program['object_color']  # przekazywanie koloru do shadera
        self.object_shininess = self.program['object_shininess']  # przekazywanie koloru do shadera
        self.point_lights = lights_from_open_gl(self.program, 1) # przekazywanie świateł do shadera4
        self.view_position = self.program['view_position']

    def setup_lights(self):
        self.point_lights[0].position.value = (10., 10.0, 0.0)
        self.point_lights[0].color.value = (0.5, 0.5, 0.5)
        self.point_lights[0].strength.value = 0.1
        # self.point_lights[1].position.value = (0., -10.0, 0.0)
        # self.point_lights[1].color.value = (0.5, 0.5, 0.5)
        # self.point_lights[1].strength.value = 0.4

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.setup_lights()
        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)

        lookat = Matrix44.look_at(
            self.camera_pos,
            self.camera_pos + self.camera_target,
            self.camera_up
        )

        self.object_shininess.value = 1.0
        self.view_position.value = self.camera_pos

        # ustawienie kolorów dla danych części ciała
        head_color = (1.0, 229 / 255, 180 / 225)
        body_color = (1.0, 215 / 255, 0.0)
        arm_color = (0.0, 0x2d / 255, 0x6e / 255)
        leg_color = (0.5, 0.0, 0.0)

        self.view.write(lookat.astype('f4'))
        self.projection.write(projection.astype('f4'))

        # wyświetlenie głowy
        translation = Matrix44.from_translation([0.0, 0.0, 5.0])
        self.object_color.value = head_color
        self.transform_matrix.write((translation).astype('f4'))
        self.sphere.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie tułowia
        translation = Matrix44.from_translation([20, 0.0, 2.0])
        scaling = Matrix44.from_scale([1.0, 1.0, 2.0])
        self.object_color.value = body_color
        self.transform_matrix.write((translation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie prawej ręki (po lewej od patrzącego)
        translation = Matrix44.from_translation([0.0, 3.0, 3.0])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.25])
        rotation = Matrix44.from_x_rotation(-np.pi / 4)
        self.object_color.value = arm_color
        self.transform_matrix.write((translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie lewej ręki (po lewej od patrzącego)
        translation = Matrix44.from_translation([0.0, -3.0, 3.0])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.25])
        rotation = Matrix44.from_x_rotation(np.pi / 4)
        self.object_color.value = arm_color
        self.transform_matrix.write((translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie prawej nogi (po lewej od patrzącego)
        translation = Matrix44.from_translation([0.0, 2.0, -1.5])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.75])
        rotation = Matrix44.from_x_rotation(-np.pi / 6)
        self.object_color.value = leg_color
        self.transform_matrix.write((translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie lewej nogi (po prawej od patrzącego)
        translation = Matrix44.from_translation([0.0, -2.0, -1.5])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.75])
        rotation = Matrix44.from_x_rotation(np.pi / 6)
        self.object_color.value = leg_color
        self.transform_matrix.write((translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)
