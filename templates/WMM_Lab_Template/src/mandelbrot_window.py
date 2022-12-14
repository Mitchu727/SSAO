import moderngl

from base_window import BaseWindowConfig


class MandelbrotWindowConfig(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(MandelbrotWindowConfig, self).__init__(**kwargs)

    def init_shaders_variables(self):
        self.center = self.program['center']
        self.scale = self.program['scale']
        self.ratio = self.program['ratio']
        self.iter = self.program['iter']

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0, 0.0)

        self.center.value = (0.5, 0.0)
        self.iter.value = 1
        self.scale.value = 1.5
        self.ratio.value = self.aspect_ratio
        self.vao.render(moderngl.TRIANGLE_STRIP)
