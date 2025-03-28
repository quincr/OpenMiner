from __future__ import annotations

import OpenGL.GL as gl

from texture import Texture
from shader import Shader

class Material():
    def __init__(self: Material, diffuse_texture_path: str) -> None:
        self.diffuse = Texture(diffuse_texture_path)

    def Apply(self: Material, shader_program: Shader) -> None:
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.diffuse._id)

        shader_program.SetInt('material.diffuse', 0)
