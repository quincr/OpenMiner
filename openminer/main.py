from __future__ import annotations

from window import Window

class OpenMiner:
    def __init__(self: OpenMiner) -> None:
        self.window = Window()

    def Init(self: OpenMiner) -> None:
        self.window.Create()

    def Start(self: OpenMiner) -> None:
        while self.window.Tick():
            pass

        self.window.Destroy()

if __name__ == '__main__':
    game = OpenMiner()
    game.Init()

    game.Start()
