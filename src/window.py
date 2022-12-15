import moderngl
import numpy as np
from pyrr import Matrix44, Vector3, vector, matrix33

from base_window import BaseWindowConfig


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
        self.plane = self.load_scene("plane.obj").root_nodes[0].mesh.vao.instance(self.program)

        # tekstury
        self.wood_texture = self.load_texture_2d("../textures/laminate_floor_02_diff_4k.jpg")

    def init_shaders_variables(self):
        self.transform_matrix = self.program['transform_matrix']  # przekształcenie obiektu pierwotnego
        self.color = self.program['color']  # przekazywanie koloru do shadera
        self.use_texture = self.program['useTexture']

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)

        lookat = Matrix44.look_at(
            self.camera_pos,
            self.camera_pos + self.camera_target,
            self.camera_up
        )

        # ustawienie kolorów dla danych części ciała
        head_color = (1.0, 229 / 255, 180 / 225)
        body_color = (1.0, 215 / 255, 0.0)
        arm_color = (0.0, 0x2d / 255, 0x6e / 255)
        leg_color = (0.5, 0.0, 0.0)

        scaling = Matrix44.from_scale([10, 10, 0.1])
        translation = Matrix44.from_translation([0.0, 0.0, -5.0])
        self.use_texture.value = True
        self.wood_texture.use()
        self.transform_matrix.write((projection * lookat * translation * scaling).astype('f4'))
        self.cube.render(moderngl.TRIANGLE_STRIP)

        self.use_texture.value = False

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
