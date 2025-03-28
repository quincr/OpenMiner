from __future__ import annotations

from PIL import Image
import numpy as np
import OpenGL.GL as gl

class Texture():
    def __init__(self: Texture, image: str | Image.Image, raw: bool = False, repeat: bool = True) -> None:
        texture = gl.glGenTextures(1)
        if not raw:
            img = Image.open(image).convert("RGBA")
        else:
            img = image
        img_data = np.array(img, dtype=np.uint8)

        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        if repeat:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        else:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST_MIPMAP_LINEAR)

        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width, img.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        self._id = texture

    def Use(self: Texture) -> None:
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._id)

    def Destroy(self: Texture) -> None:
        gl.glDeleteTextures(1, [self._id])
