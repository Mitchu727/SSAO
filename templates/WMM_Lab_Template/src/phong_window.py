import moderngl
from pyrr import Matrix44

from base_window import BaseWindowConfig


class PhongWindow(BaseWindowConfig):

    def __init__(self, **kwargs):
        super(PhongWindow, self).__init__(**kwargs)

    def init_shaders_variables(self):
        self.transform_matrix = self.program['transform_matrix']
        self.light_color = self.program['light_color']
        self.light_position = self.program['light_position']
        self.object_color = self.program['object_color']
        self.object_shininess = self.program['object_shininess']
        self.light_strength = self.program['light_strength']


    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (3.0, 1.0, -5.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
        )
        # TODO: Write variables to shader
        self.transform_matrix.write((proj * lookat).astype('f4'))
        self.light_color.value = (0.5, 0.5, 0.5)
        self.light_position.value = (-0.5, 2.0, -1.5)
        self.light_strength.value = 0.2
        self.object_color.value = (1.0, 1.0, 0.0)
        self.object_shininess.value = 0.5
        self.vao.render()
