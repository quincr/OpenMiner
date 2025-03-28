from __future__ import annotations

import glm

class Camera():
    def __init__(self: Camera) -> None:
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec2(-90, 0)
        self.fov = 70

        self.front = glm.vec3()
        self.right = glm.vec3()
        self.up = glm.vec3()

        self.m_view = None
        self.m_projection = None

    def Tick(self: Camera, resolution: glm.vec2) -> None:
        direction = glm.vec3()

        self.rotation.y = max(min(self.rotation.y, 89.99), -89.99)

        direction.x = glm.cos(glm.radians(self.rotation.x)) * glm.cos(glm.radians(self.rotation.y))
        direction.y = glm.sin(glm.radians(self.rotation.y))
        direction.z = glm.sin(glm.radians(self.rotation.x)) * glm.cos(glm.radians(self.rotation.y))

        camera_front = -glm.normalize(direction)
        camera_right = glm.normalize(glm.cross(glm.vec3(0, 1, 0), camera_front))
        camera_up = glm.cross(camera_front, camera_right)

        self.m_view = glm.lookAt(self.position, self.position + camera_front, camera_up)
        self.m_projection = glm.perspective(glm.radians(self.fov), resolution.x / resolution.y, 0.01, 16384)

        self.right = -camera_right
        self.up = camera_up
        self.front = camera_front
