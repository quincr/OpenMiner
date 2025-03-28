from __future__ import annotations

import numpy as np

from window import Window
from shader import Shader
from camera import Camera
from mesh import Mesh
from material import Material
from world import Chunk, World

class OpenMiner:
    def __init__(self: OpenMiner) -> None:
        self.window = Window()

    def Init(self: OpenMiner) -> None:
        self.window.Create()

        self.default_shader = Shader("./openminer/shaders/vertex.glsl", "./openminer/shaders/fragment.glsl")
        self.default_camera = Camera()
        self.texture_atlas = Material("./assets/atlas.png")

        self.testing_mesh = Mesh(self.default_shader, self.texture_atlas)
        self.testing_mesh.Create(np.array((
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 0,
            1, 1, 0, 1, 1, 0, 0, 0
        ), np.float32))

        self.world = World(self.default_shader, self.texture_atlas)

        self.default_camera.position.z = -5

    def Start(self: OpenMiner) -> None:
        self.world.Generate()

        while self.window.Tick():
            self.default_camera.Tick(self.window.resolution, self.window.window, 1 / 60)

            self.default_shader.Use()
            self.default_shader.SetMat4x4("view", self.default_camera.m_view)
            self.default_shader.SetMat4x4("projection", self.default_camera.m_projection)

            self.world.Render()

        self.default_shader.Destroy()
        self.window.Destroy()

if __name__ == '__main__':
    game = OpenMiner()
    game.Init()

    game.Start()
