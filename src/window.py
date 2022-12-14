import moderngl
import numpy as np
from pyrr import Matrix44, Vector3, Matrix33

from base_window import BaseWindowConfig


class SSAOWindow(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(SSAOWindow, self).__init__(**kwargs)
        self.camera_position = [15.0, 0.0, 1.0]
        self.camera_target = [0.0, 0, 1.0]
        self.camera_speed = 0.1

    def unicode_char_entered(self, char: str):
        if char.lower() == "s":
            self.camera_position[0] += self.camera_speed
            self.camera_target[0] += self.camera_speed
        if char.lower() == "w":
            self.camera_position[0] -= self.camera_speed
            self.camera_target[0] -= self.camera_speed
        if char.lower() == "d":
            self.camera_position[1] += self.camera_speed
            self.camera_target[1] += self.camera_speed
        if char.lower() == "a":
            self.camera_position[1] -= self.camera_speed
            self.camera_target[1] -= self.camera_speed
        if char.lower() == "q":
            self.camera_position[2] += self.camera_speed
            self.camera_target[2] += self.camera_speed
        if char.lower() == "e":
            self.camera_position[2] -= self.camera_speed
            self.camera_target[2] -= self.camera_speed
        print(f"New camera position: {self.camera_position}")

    # def mouse_position_event(self, x, y, dx, dy):
    #     x_rotation = Matrix33.from_x_rotation(dx)
    #     vec = Vector3(self.camera_position) - Vector3(self.camera_target)
    #     self.camera_target = self.camera_target + vec * x_rotation
    #     print(f"New camera target: {self.camera_target}, {self.window_size[0] * self.aspect_ratio}, {y}")

    def model_load(self):
        # wczytanie obiektów do późniejszego renderowania
        self.sphere = self.load_scene("sphere.obj").root_nodes[0].mesh.vao.instance(self.program)
        self.cube = self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        self.teapot = self.load_scene("teapot.obj").root_nodes[0].mesh.vao.instance(self.program)

    def init_shaders_variables(self):
        self.transform_matrix = self.program['transform_matrix']  # przekształcenie obiektu pierwotnego
        self.color = self.program['color']  # przekazywanie koloru do shadera

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            self.camera_position,
            self.camera_target,
            (0.0, 0.0, 1.0),
        )

        # ustawienie kolorów dla danych części ciała
        head_color = (1.0, 229 / 255, 180 / 225)
        body_color = (1.0, 215 / 255, 0.0)
        arm_color = (0.0, 0x2d / 255, 0x6e / 255)
        leg_color = (0.5, 0.0, 0.0)

        # wyświetlenie głowy
        translation = Matrix44.from_translation([0.0, 0.0, 5.0])
        self.color.value = head_color
        self.transform_matrix.write((projection * lookat * translation).astype('f4'))
        self.sphere.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie tułowia
        translation = Matrix44.from_translation([0.0, 0.0, 2.0])
        scaling = Matrix44.from_scale([1.0, 1.0, 2.0])
        self.color.value = body_color
        self.transform_matrix.write((projection * lookat * translation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie prawej ręki (po lewej od patrzącego)
        translation = Matrix44.from_translation([0.0, 3.0, 3.0])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.25])
        rotation = Matrix44.from_x_rotation(-np.pi / 4)
        self.color.value = arm_color
        self.transform_matrix.write((projection * lookat * translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie lewej ręki (po lewej od patrzącego)
        translation = Matrix44.from_translation([0.0, -3.0, 3.0])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.25])
        rotation = Matrix44.from_x_rotation(np.pi / 4)
        self.color.value = arm_color
        self.transform_matrix.write((projection * lookat * translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie prawej nogi (po lewej od patrzącego)
        translation = Matrix44.from_translation([0.0, 2.0, -1.5])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.75])
        rotation = Matrix44.from_x_rotation(-np.pi / 6)
        self.color.value = leg_color
        self.transform_matrix.write((projection * lookat * translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        # wyświetlenie lewej nogi (po prawej od patrzącego)
        translation = Matrix44.from_translation([0.0, -2.0, -1.5])
        scaling = Matrix44.from_scale([0.5, 0.5, 1.75])
        rotation = Matrix44.from_x_rotation(np.pi / 6)
        self.color.value = leg_color
        self.transform_matrix.write((projection * lookat * translation * rotation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)
