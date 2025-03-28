from __future__ import annotations

import glm
import OpenGL.GL as gl

class Shader():
    def __init__(self: Shader, vertex_path: str, fragment_path: str) -> None:
        with open(vertex_path, 'r') as v_file:
            v_source = v_file.read()
        
        v_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(v_shader, v_source)
        gl.glCompileShader(v_shader)

        result = gl.glGetShaderiv(v_shader, gl.GL_COMPILE_STATUS)
        if result != 1:
            raise RuntimeError(f"Failed to compile shader! log: {gl.glGetShaderInfoLog(v_shader).decode()}")

        with open(fragment_path, 'r') as f_file:
            f_source = f_file.read()
        
        f_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(f_shader, f_source)
        gl.glCompileShader(f_shader)

        result = gl.glGetShaderiv(f_shader, gl.GL_COMPILE_STATUS)
        if result != 1:
            raise RuntimeError(f"Failed to compile shader! log: {gl.glGetShaderInfoLog(f_shader).decode()}")

        program = gl.glCreateProgram()
        gl.glAttachShader(program, v_shader)
        gl.glAttachShader(program, f_shader)
        gl.glLinkProgram(program)

        link_status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
        if link_status != 1:
            raise RuntimeError("Failed to link shader program!")

        gl.glDetachShader(program, v_shader)
        gl.glDetachShader(program, f_shader)
        gl.glDeleteShader(v_shader)
        gl.glDeleteShader(f_shader)

        self.id = program

    def Use(self: Shader) -> None:
        gl.glUseProgram(self.id)

    def SetMat4x4(self: Shader, name: str, value: glm.mat4) -> None:
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.id, name), 1, gl.GL_FALSE, glm.value_ptr(value))

    def SetFloat(self: Shader, name: str, value: float) -> None:
        gl.glUniform1f(gl.glGetUniformLocation(self.id, name), value)

    def SetInt(self: Shader, name: str, value: int) -> None:
        gl.glUniform1i(gl.glGetUniformLocation(self.id, name), value)

    def SetVec3(self: Shader, name: str, value: glm.vec3) -> None:
        gl.glUniform3fv(gl.glGetUniformLocation(self.id, name), 1, glm.value_ptr(value))

    def SetVec2(self: Shader, name: str, value: glm.vec2) -> None:
        gl.glUniform2fv(gl.glGetUniformLocation(self.id, name), 1, glm.value_ptr(value))

    def Destroy(self: Shader) -> None:
        gl.glDeleteProgram(self.id)
