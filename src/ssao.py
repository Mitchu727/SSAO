import moderngl
import numpy as np
from moderngl import Texture, TextureCube, VertexArray
from moderngl_window import geometry
from pyrr import Matrix44

import config
from src.ssao_window import SSAOWindow
from utils import get_shaders

MAX_SSAO_SAMPLES_QUANTITY = 100


class SSAODemo(SSAOWindow):
    gl_version = config.GL_VERSION
    title = config.WINDOW_TITLE
    resource_dir = config.RESOURCE_DIR

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.material_properties = [0.5, 0.5, 0.25, 25.0]
        self.ssao_z_offset = 0.0
        self.ssao_blur = False

        # Create the geometry frame-buffer
        self.g_view_z = self.ctx.texture(self.wnd.buffer_size, 1, dtype="f2")
        self.g_normal = self.ctx.texture(self.wnd.buffer_size, 3, dtype="f2")
        self.g_albedo_specular = self.ctx.texture(self.wnd.buffer_size, 4, dtype="f2")
        self.g_depth = self.ctx.depth_texture(self.wnd.buffer_size)
        self.g_buffer = self.ctx.framebuffer(
            color_attachments=[self.g_view_z, self.g_normal, self.g_albedo_specular],
            depth_attachment=self.g_depth
        )

        # Generate the SSAO frame-buffer
        self.ssao_occlusion = self.ctx.texture(self.wnd.buffer_size, 1, dtype="f1")
        self.ssao_buffer = self.ctx.framebuffer(color_attachments=[self.ssao_occlusion])

        shaders = get_shaders(f"{config.RESOURCE_DIR}/shaders")
        self.init_shaders(shaders)
        self.init_models_textures()

        self.quad_fs = geometry.quad_fs()

        # Generate SSAO samples
        self.current_ssao_samples_qty = 64
        self.ssao_program["n_samples"].value = self.current_ssao_samples_qty
        self.ssao_std_dev = 0.1
        self.ssao_samples = np.random.normal(0.0, self.ssao_std_dev, (MAX_SSAO_SAMPLES_QUANTITY, 3))
        self.ssao_samples[:, 2] = np.abs(self.ssao_samples[:, 2])
        self.ssao_program["samples"].write(self.ssao_samples.ravel().astype('f4'))

        # Create random vectors
        rand_texture_size = 32
        rand_texture_data = np.random.bytes(3 * rand_texture_size * rand_texture_size)
        self.random_texture = self.ctx.texture(
            (rand_texture_size, rand_texture_size),
            3,
            dtype="f1",
            data=rand_texture_data
        )
        self.random_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.random_texture.repeat_x = True
        self.random_texture.repeat_y = True

    def change_ssao_samples_quantity(self, sample_delta: int):
        new_samples_qty = self.current_ssao_samples_qty + sample_delta
        if 0 < new_samples_qty <= MAX_SSAO_SAMPLES_QUANTITY:
            print(f"New samples quantity: {new_samples_qty}")
            self.current_ssao_samples_qty = new_samples_qty
            self.ssao_program["n_samples"].value = self.current_ssao_samples_qty

    def render_object(self,
                      color,
                      obj: VertexArray,
                      translation=Matrix44.identity(),
                      rotation=Matrix44.identity(),
                      scale=Matrix44.identity(),
                      texture: Texture = None,
                      texture_cube: TextureCube = None,
                      texture_scale=1.):
        self.geometry_program["transform_matrix"].write((translation * rotation * scale).astype('f4'))
        self.texture_scale.write(np.array(texture_scale).astype("f4"))

        if texture is not None and texture_cube is not None:
            raise Exception("You cannot apply texture_2d and texture_cube at the same time.")

        if texture_cube is not None:
            self.use_texture.value = 2
            texture_cube.use(location=1)
        elif texture is not None:
            self.use_texture.value = 1
            texture.use(location=0)
        else:
            self.use_texture.value = 0
        obj.render()

    def init_shaders(self, shaders):
        self.geometry_program = self.ctx.program(
            vertex_shader=shaders["geometry"].vertex_shader,
            fragment_shader=shaders["geometry"].fragment_shader)
        self.geometry_program['tex'] = 0
        self.geometry_program['texCube'] = 1

        self.ssao_program = self.ctx.program(
            vertex_shader=shaders["ssao"].vertex_shader,
            fragment_shader=shaders["ssao"].fragment_shader)
        self.ssao_program["g_view_z"].value = 0
        self.ssao_program["g_norm"].value = 1
        self.ssao_program["noise"].value = 3

        self.shading_program = self.ctx.program(
            vertex_shader=shaders["shading"].vertex_shader,
            fragment_shader=shaders["shading"].fragment_shader)
        self.shading_program["g_view_z"].value = 0
        self.shading_program["g_normal"].value = 1
        self.shading_program["g_albedo_specular"].value = 2
        self.shading_program["ssao_occlusion"].value = 3

    def init_models_textures(self):
        # Scene objects
        self.sphere = self.load_scene("models/sphere.obj").root_nodes[0].mesh.vao.instance(self.geometry_program)
        self.cube = self.load_scene("models/cube.obj").root_nodes[0].mesh.vao.instance(self.geometry_program)
        self.teapot = self.load_scene("models/teapot.obj").root_nodes[0].mesh.vao.instance(self.geometry_program)
        # self.dragon = self.load_scene('models/stanford_dragon.obj').root_nodes[0].mesh.vao.instance(self.geometry_program)

        # Textures
        self.wood_texture = self.load_texture_2d("textures/wood.jpg")
        self.football_texture = self.load_texture_2d("textures/football.jpg")
        self.stone_texture = self.load_texture_2d("textures/stone.jpg")
        self.metal_texture = self.load_texture_2d("textures/metal.jpg")
        self.companion_cube = self.load_texture_cube(*["textures/companion_cube.jpg"] * 6)

        self.color = self.geometry_program['object_color']
        self.texture_scale = self.geometry_program['texture_scale']
        self.use_texture = self.geometry_program['use_texture']

    def render(self, time: float, frame_time: float):
        projection_matrix = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        camera_matrix = Matrix44.look_at(
            self.camera_position,
            self.camera_position + self.camera_target,
            self.camera_up)
        mvp = projection_matrix * camera_matrix
        self.geometry_program["camera_matrix"].write(camera_matrix.astype('f4'))
        self.geometry_program["projection_matrix"].write(projection_matrix.astype('f4'))
        self.ssao_program["m_camera_inverse"].write(camera_matrix.inverse.astype('f4'))
        self.ssao_program["m_projection_inverse"].write(projection_matrix.inverse.astype('f4'))
        self.ssao_program["mvp"].write(mvp.astype('f4'))
        self.shading_program["m_camera_inverse"].write(camera_matrix.inverse.astype('f4'))
        self.shading_program["m_projection_inverse"].write(projection_matrix.inverse.astype('f4'))

        # Geometry pass
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.g_buffer.clear(0.0, 0.0, 0.0)
        self.g_buffer.use()

        self.render_object(obj=self.cube,
                           color=(0, 0.7, 0.1),
                           translation=Matrix44.from_translation([0.0, 0.0, -5.0]),
                           scale=Matrix44.from_scale([10, 10, 0.1]),
                           texture=self.wood_texture)

        # Background
        self.render_object(obj=self.cube,
                           color=(255, 255, 255),
                           translation=Matrix44.from_translation([-10.0, 0.0, 5.0]),
                           scale=Matrix44.from_scale([10, 10, 0.1]),
                           rotation=Matrix44.from_y_rotation(-np.pi / 2),
                           texture=self.stone_texture,
                           texture_scale=0.1)

        # Ball
        self.render_object(obj=self.sphere,
                           color=(10, 1000, 0),
                           translation=Matrix44.from_translation([-5.0, 0.0, -4.0]),
                           texture=self.football_texture)

        # # Dragon
        # self.render_object(obj=self.dragon,
        #                    color=(255, 255, 0),
        #                    translation=Matrix44.from_translation([0.0, -5.0, -3.0]),
        #                    scale=Matrix44.from_scale([2, 2, 2]),
        #                    rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
        #                    texture=self.football_texture)

        # Teapot
        self.render_object(obj=self.teapot,
                           color=(0.6, 0, 1),
                           translation=Matrix44.from_translation([-6.0, 3.0, -3.5]),
                           # rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
                           scale=Matrix44.from_scale([0.2, 0.2, 0.2]),
                           texture=self.metal_texture)

        # Companion cube
        self.render_object(obj=self.cube,
                           color=(0, 255, 0),
                           translation=Matrix44.from_translation([-6.0, -3.0, -4]),
                           rotation=Matrix44.from_x_rotation(-np.pi / 2) * Matrix44.from_y_rotation(np.pi / 4),
                           texture_cube=self.companion_cube)

        # Calculate occlusion
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ssao_buffer.clear(0.0)
        self.ssao_buffer.use()
        self.ssao_program["v_camera_pos"].value = self.camera_position
        self.ssao_program["f_camera_pos"].value = self.camera_position
        self.ssao_program["z_offset"].value = self.ssao_z_offset
        self.g_view_z.use(location=0)
        self.g_normal.use(location=1)
        self.g_albedo_specular.use(location=2)
        self.random_texture.use(location=3)
        self.quad_fs.render(self.ssao_program)

        # Shading pass
        self.ctx.screen.clear(1.0, 1.0, 1.0)
        self.ctx.screen.use()
        self.shading_program["v_camera_pos"].value = self.camera_position
        self.shading_program["camera_pos"].value = self.camera_position
        self.shading_program["light_pos"].value = self.camera_position
        self.shading_program["material_properties"].value = tuple(self.material_properties)
        self.g_view_z.use(location=0)
        self.g_normal.use(location=1)
        self.g_albedo_specular.use(location=2)
        self.ssao_occlusion.use(location=3)
        self.quad_fs.render(self.shading_program)

    def check_implementation_specific_characters(self, char: str):
        if char.lower() == ",":
            self.change_ssao_samples_quantity(-1)
        if char.lower() == ".":
            self.change_ssao_samples_quantity(1)


if __name__ == '__main__':
    SSAODemo.run()
