from __future__ import annotations

import glm
import numpy as np
import math

from mesh import Mesh
from shader import Shader
from material import Material

CHUNK_SIZE = 8
WORLD_SIZE = 3

BLOCKS = {}
MODELS = {}

class World():
    def __init__(self: World, chunk_shader: Shader, chunk_material: Material) -> None:
        self.chunks = []

        self.chunk_shader = chunk_shader
        self.chunk_material = chunk_material

    def Generate(self: World) -> None:
        for x in range(-WORLD_SIZE, WORLD_SIZE + 1):
            for y in range(-WORLD_SIZE, WORLD_SIZE + 1):
                for z in range(-WORLD_SIZE, WORLD_SIZE + 1):
                    next_chunk = Chunk(self.chunk_shader, self.chunk_material, x, y, z)
                    next_chunk.BuildMesh()

                    self.chunks.append(next_chunk)

    def Render(self: World) -> None:
        for c in self.chunks:
            c.Render()

class Chunk():
    def __init__(self: Chunk, chunk_shader: Shader, chunk_material: Material, x: int, y: int, z: int) -> None:
        self.shader = chunk_shader
        self.material = chunk_material

        self.mesh = Mesh(self.shader, self.material)
        self.mesh.position.xyz = (x * CHUNK_SIZE // 4, y * CHUNK_SIZE // 4, z * CHUNK_SIZE // 4)
        self.position = glm.vec3(x, y, z) * CHUNK_SIZE

    def _testIsBlockAir(self: Chunk, x: int, y: int, z: int) -> bool:
        if any((
            x < 0,
            y < 0,
            z < 0,
            x > CHUNK_SIZE - 1,
            y > CHUNK_SIZE - 1,
            z > CHUNK_SIZE - 1
        )):
            return True

        return math.sin((x + self.position.x) / 3.21 + (y + self.position.y) / 2.21 + (z + self.position.z) / 5.21) < 0

    def BuildMesh(self: Chunk) -> None:
        mesh_data = []

        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    if self._testIsBlockAir(x, y, z):
                        continue

                    if self._testIsBlockAir(x + 1, y, z):
                        mesh_data.extend([
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,

                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                        ])

                    if self._testIsBlockAir(x - 1, y, z):
                        mesh_data.extend([
                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,

                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,
                        ])

                    if self._testIsBlockAir(x, y + 1, z):
                        mesh_data.extend([
                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,

                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                        ])

                    if self._testIsBlockAir(x, y - 1, z):
                        mesh_data.extend([
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,

                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                        ])

                    if self._testIsBlockAir(x, y, z + 1):
                        mesh_data.extend([
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 1, 0, 0, 0, 0,

                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 + 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 0, 0, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 + 0.125, 1, 0, 0, 0, 0,
                        ])

                    if self._testIsBlockAir(x, y, z - 1):
                        mesh_data.extend([
                            x * 0.25 + 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 1, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 0, 1, 0, 0, 0,

                            x * 0.25 - 0.125, y * 0.25 + 0.125, z * 0.25 - 0.125, 0, 1, 0, 0, 0,
                            x * 0.25 + 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 1, 0, 0, 0, 0,
                            x * 0.25 - 0.125, y * 0.25 - 0.125, z * 0.25 - 0.125, 0, 0, 0, 0, 0,
                        ])

        self.mesh.Create(np.array(mesh_data, np.float32))

    def Render(self: Chunk) -> None:
        self.mesh.Render()
