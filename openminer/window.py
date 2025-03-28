from __future__ import annotations

import glfw
import OpenGL.GL as gl
import glm

class Window():
    def __init__(self: Window) -> None:
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW!")

    def Create(self: Window) -> None:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        window = glfw.create_window(800, 450, "OpenMiner", None, None)
        if not window:
            raise RuntimeError("Failed to create GLFW window!")

        monitor_size = glfw.get_monitor_workarea(glfw.get_primary_monitor())[2:4]
        glfw.set_window_pos(window, *(glm.ivec2(monitor_size) / 2 - glm.ivec2(800, 450) / 2))

        glfw.set_framebuffer_size_callback(window, self._onResize)

        glfw.make_context_current(window)
        glfw.swap_interval(1)

        gl.glClearColor(0.20, 0.3, 0.25, 1.0)
        gl.glViewport(0, 0, 800, 450)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

        self.window = window
        self.resolution = glm.vec2(800, 450)

    def _onResize(self: Window, window, new_x: int, new_y: int) -> None:
        gl.glViewport(0, 0, new_x, new_y)
        self.resolution = glm.vec2(glfw.get_window_size(window))

    def Tick(self: Window) -> bool:
        if glfw.window_should_close(self.window):
            return False

        glfw.poll_events()
        glfw.swap_buffers(self.window)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        return True

    def Destroy(self: Window) -> None:
        # I'm unsure if this is actually required, due to pythons garbage
        # collection, however I put it anyway just in case.

        glfw.destroy_window(self.window)
        glfw.terminate()
