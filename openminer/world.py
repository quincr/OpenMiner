from __future__ import annotations

import time
import numpy as np
import math

from mesh import Mesh
from shader import Shader
from material import Material

CHUNK_SIZE = 8

BLOCKS = {}
MODELS = {}

class Chunk():
    def __init__(self: Chunk, chunk_shader: Shader, chunk_material: Material) -> None:
        self.shader = chunk_shader
        self.material = chunk_material

        self.mesh = Mesh(self.shader, self.material)

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

        return math.sin(x / 3.21 + y / 2.21 + z / 5.21) < 0

    def BuildMesh(self: Chunk) -> None:
        a = time.time()
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

        print("Chunk build time: ", time.time() - a)
        self.mesh.Create(np.array(mesh_data, np.float32))

    def Render(self: Chunk) -> None:
        self.mesh.Render()
