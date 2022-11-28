import moderngl_window

from base_window import BaseWindowConfig
from mandelbrot_window import MandelbrotWindowConfig
from robot_window import RobotWindow
from phong_window import PhongWindow

if __name__ == '__main__':
    # moderngl_window.run_window_config(BaseWindowConfig)
    # moderngl_window.run_window_config(MandelbrotWindowConfig)
    # moderngl_window.run_window_config(RobotWindow)
    moderngl_window.run_window_config(PhongWindow)