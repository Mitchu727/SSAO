from pathlib import Path

import moderngl
from moderngl_window import WindowConfig
from moderngl_window import geometry

import config
from utils import get_shaders


class BaseWindowConfig(WindowConfig):
    gl_version = config.GL_VERSION
    title = config.WINDOW_TITLE
    resource_dir = (Path(__file__).parent.parent / 'resources' / 'models').resolve()

    def __init__(self, **kwargs):
        super(BaseWindowConfig, self).__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        shaders = get_shaders(self.argv.shader_path)
        self.program = self.ctx.program(vertex_shader=shaders[self.argv.shader_name].vertex_shader,
                                        fragment_shader=shaders[self.argv.shader_name].fragment_shader)

        self.model_load()
        self.init_shaders_variables()

    def model_load(self):
        if self.argv.model_name:
            self.obj = self.load_scene(self.argv.model_name)
            self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.program)
        else:
            self.vao = geometry.quad_2d().instance(self.program)

    def init_shaders_variables(self):
        pass

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument('--shader_path', type=str, required=True, help='Path to the directory with shaders')
        parser.add_argument('--shader_name', type=str, required=True,
                            help='Name of the shader to look for in the shader_path directory')
        parser.add_argument('--model_name', type=str, required=False, help='Name of the model to load')

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0, 0.0)
        self.vao.render(moderngl.TRIANGLE_STRIP)
