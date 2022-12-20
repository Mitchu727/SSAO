import moderngl
import numpy as np
from moderngl import Texture, VertexArray, TextureCube
from pyrr import Matrix44, Vector3, vector, matrix33

from base_window import BaseWindowConfig
from point_light import lights_from_open_gl


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
        up = self.camera_up

        if char.lower() == "w":
            self.move_camera(forward * self.camera_moving_speed)
        if char.lower() == "s":
            self.move_camera(-forward * self.camera_moving_speed)
        if char.lower() == "d":
            self.move_camera(side * self.camera_moving_speed)
        if char.lower() == "a":
            self.move_camera(-side * self.camera_moving_speed)
        if char.lower() == " ":
            self.move_camera(up * self.camera_moving_speed)
        if char.lower() == "c":
            self.move_camera(-up * self.camera_moving_speed)
        if char.lower() == "q":
            forward_rotation = matrix33.create_from_axis_rotation(forward, -np.pi / 45 * self.camera_rotation_speed)
            self.rotate_camera(forward_rotation)
        if char.lower() == "e":
            forward_rotation = matrix33.create_from_axis_rotation(forward, np.pi / 45 * self.camera_rotation_speed)
            self.rotate_camera(forward_rotation)

    def move_camera(self, moving_vector):
        self.camera_pos += moving_vector
        print(f"New camera position: {self.camera_pos}")

    def rotate_camera(self, rotation_matrix):
        self.camera_target = vector.normalize(matrix33.apply_to_vector(rotation_matrix, self.camera_target))
        self.camera_up = vector.normalize(matrix33.apply_to_vector(rotation_matrix, self.camera_up))
        print(f"New camera vector: {self.camera_target}")

    def mouse_position_event(self, x, y, dx, dy):
        side = vector.normalize(np.cross(self.camera_target, self.camera_up))

        z_rotation_matrix = matrix33.create_from_z_rotation(np.pi / 180 * self.camera_rotation_speed * dx)
        self.rotate_camera(z_rotation_matrix)

        side_rotation = matrix33.create_from_axis_rotation(side, -np.pi / 180 * self.camera_rotation_speed * dy)
        self.rotate_camera(side_rotation)

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
        self.companion_cube = self.load_texture_cube(*["../textures/companion_cube.jpg"] * 6)

    def init_shaders_variables(self):
        self.transform_matrix = self.program['transform_matrix']  # przekształcenie obiektu pierwotnego
        self.lookat = self.program['lookat']
        self.projection = self.program['projection']
        self.object_color = self.program['object_color']  # przekazywanie koloru do shadera
        self.object_shininess = self.program['object_shininess']  # przekazywanie koloru do shadera
        self.point_lights = lights_from_open_gl(self.program, 1)  # przekazywanie świateł do shadera4
        self.view_position = self.program['view_position']
        self.color = self.program['object_color']  # przekazywanie koloru do shadera
        self.use_texture = self.program['use_texture']
        self.texture_size = self.program['texture_scale']

    def setup_lights(self):
        self.point_lights[0].position.value = (5., 0., 0.)
        self.point_lights[0].color.value = (1., 1., 1.)
        self.point_lights[0].ambient_strength.value = 0.25
        self.point_lights[0].diffuse_strength.value = 0.5
        self.point_lights[0].specular_strength.value = 1

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
        self.projection.write(projection.astype('f4'))
        self.lookat.write(lookat.astype('f4'))
        self.transform_matrix.write((translation * rotation * scale).astype('f4'))
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
        self.setup_lights()
        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            self.camera_pos,
            self.camera_pos + self.camera_target,
            self.camera_up
        )
        self.object_shininess.value = 1.0
        self.view_position.value = self.camera_pos

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
                        translation=Matrix44.from_translation([-5.0, 0.0, -4.0]),
                        texture=self.football_texture)

        # Dzban
        self.render_vbo(self.teapot,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([-6.0, 3.0, -3.5]),
                        # rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
                        scale=Matrix44.from_scale([0.2, 0.2, 0.2]),
                        texture=self.metal_texture)

        # Kostka
        self.render_vbo(self.cube,
                        projection=projection,
                        lookat=lookat,
                        translation=Matrix44.from_translation([-6.0, -3.0, -4]),
                        rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
                        texture_cube=self.companion_cube)
