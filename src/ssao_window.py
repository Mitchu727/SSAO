from abc import ABC

import numpy as np
from moderngl_window.context.base import WindowConfig
from pyrr import vector, matrix33, Vector3


class SSAOWindow(WindowConfig, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_position = Vector3([10.0, 0.0, 0])
        self.camera_target = Vector3([-1.0, 0, 0.0])
        self.camera_up = Vector3([0.0, 0, 1.0])
        self.camera_moving_speed = 0.1
        self.camera_rotation_speed = 0.1

        self.wnd.mouse_exclusivity = True

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
            forward_rotation = matrix33.create_from_axis_rotation(forward, 2 * -np.pi / 45 * self.camera_rotation_speed)
            self.rotate_camera(forward_rotation)
        if char.lower() == "e":
            forward_rotation = matrix33.create_from_axis_rotation(forward, 2 * np.pi / 45 * self.camera_rotation_speed)
            self.rotate_camera(forward_rotation)

        self.check_implementation_specific_characters(char)

    def check_implementation_specific_characters(self, char: str):
        raise "Not implemented"

    def move_camera(self, moving_vector):
        self.camera_position += moving_vector
        # print(f"New camera position: {self.camera_position}")

    def rotate_camera(self, rotation_matrix):
        self.camera_target = vector.normalize(matrix33.apply_to_vector(rotation_matrix, self.camera_target))
        self.camera_up = vector.normalize(matrix33.apply_to_vector(rotation_matrix, self.camera_up))
        # print(f"New camera vector: {self.camera_target}")
        # print(f"New camera up: {self.camera_up}")

    def mouse_position_event(self, x, y, dx, dy):
        side = vector.normalize(np.cross(self.camera_target, self.camera_up))

        z_rotation_matrix = matrix33.create_from_z_rotation(np.pi / 180 * self.camera_rotation_speed * dx)
        self.rotate_camera(z_rotation_matrix)

        side_rotation = matrix33.create_from_axis_rotation(side, -np.pi / 180 * self.camera_rotation_speed * dy)
        self.rotate_camera(side_rotation)
