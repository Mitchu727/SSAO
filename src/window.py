import os

import moderngl
import numpy as np
from PIL import Image
from moderngl import Texture, VertexArray, TextureCube
from pyglet.gl import glBindTexture, GL_TEXTURE_2D, glTexParameteri, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_WRAP_S
from pyrr import Matrix44, Vector3, vector, matrix33

from base_window import BaseWindowConfig


class SSAOWindow(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(SSAOWindow, self).__init__(**kwargs)
        self.camera_pos = Vector3([10.0, 0.0, 0.0])
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

        # tekstury
        self.wood_texture = self.load_texture_2d("../textures/wood.jpg")
        self.football_texture = self.load_texture_2d("../textures/football.jpg")
        self.stone_texture = self.load_texture_2d("../textures/stone.jpg")
        self.metal_texture = self.load_texture_2d("../textures/metal.jpg")
        companion_cube_path = ["../textures/companion_cube.jpg"] * 6
        self.companion_cube = self.load_texture_cube(*companion_cube_path)

    def init_shaders_variables(self):
        self.transform_matrix = self.program['transform_matrix']  # przekształcenie obiektu pierwotnego
        self.color = self.program['color']  # przekazywanie koloru do shadera
        self.use_texture = self.program['use_texture']
        self.texture_size = self.program['texture_scale']

    def render_vbo(self,
                   vertex_object: VertexArray,
                   projection=Matrix44.identity(),
                   lookat=Matrix44.identity(),
                   translation=Matrix44.identity(),
                   rotation=Matrix44.identity(),
                   scale=Matrix44.identity(),
                   color=(0., 0., 0.),
                   texture: Texture = None,
                   texture_cube: TextureCube = None,
                   texture_scale=1.):
        self.transform_matrix.write((projection * lookat * translation * rotation * scale).astype('f4'))
        self.texture_size.write(np.array(texture_scale).astype("f4"))
        self.color.value = color

        if texture is not None and texture_cube is not None:
            raise Exception("You cannot apply texture_2d and texture_cube at the same time.")

        if texture_cube is not None:
            self.use_texture.value = 2
            texture_cube.use()
        elif texture is not None:
            self.use_texture.value = 1
            texture.use()
        else:
            self.use_texture.value = 0
        vertex_object.render()

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            self.camera_pos,
            self.camera_pos + self.camera_target,
            self.camera_up
        )

        # Tło
        self.render_vbo(self.cube,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([0.0, 0.0, -5.0]),
                        scale=Matrix44.from_scale([10, 10, 0.1]),
                        texture=self.wood_texture)

        self.render_vbo(self.cube,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([-10.0, 0.0, 5.0]),
                        scale=Matrix44.from_scale([10, 10, 0.1]),
                        rotation=Matrix44.from_y_rotation(-np.pi / 2),
                        texture=self.stone_texture,
                        texture_scale=0.1)

        # Piłka
        self.render_vbo(self.sphere,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([-9.0, 0.0, -4.0]),
                        texture=self.football_texture)

        # Dzban
        self.render_vbo(self.teapot,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([-6.0, 3.0, -3.5]),
                        rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
                        scale=Matrix44.from_scale([0.2, 0.2, 0.2]),
                        texture=self.metal_texture)

        # Kostka
        self.render_vbo(self.cube,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([-6.0, -3.0, -3.5]),
                        rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
                        texture_cube=self.companion_cube)
