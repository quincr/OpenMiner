from __future__ import annotations

import glm
import typing
import ctypes
import numpy as np
import OpenGL.GL as gl

from shader import Shader
from material import Material

class Mesh():
    def __init__(self: Mesh, shader: Shader, material: Material) -> None:
        self.shader = shader
        self.material = material

        self.position = glm.vec3(0)
        self.rotation = glm.vec3(0)
        self.scale = glm.vec3(1)
    
    def Create(self: Mesh, vertices: np.ndarray[typing.Any, np.dtype[np.float32]]) -> None:
        vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(vao)

        vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        gl.glEnableVertexAttribArray(1)

        gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(5 * ctypes.sizeof(ctypes.c_float)))
        gl.glEnableVertexAttribArray(2)

        gl.glBindVertexArray(0)

        self._num_vertices = len(vertices) // 8
        self._vao = vao
        self._vbo = vbo

    def Render(self: Mesh) -> None:
        self.shader.Use()
        self.material.Apply(self.shader)

        model_mat = glm.mat4(1)
        model_mat = glm.translate(model_mat, self.position)
        model_mat = glm.rotate(model_mat, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        model_mat = glm.rotate(model_mat, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        model_mat = glm.rotate(model_mat, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        model_mat = glm.scale(model_mat, self.scale)

        self.shader.SetMat4x4("model", model_mat)
        gl.glBindVertexArray(self._vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self._num_vertices)

    def Destroy(self: Mesh) -> None:
        gl.glDeleteVertexArrays(1, (self._vao,))
        gl.glDeleteBuffers(1, (self._vbo,))
