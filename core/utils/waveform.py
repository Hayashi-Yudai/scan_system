from core.models import TemporalData

import numpy as np


class WaveForm:
    def __init__(self, x: list[float] = [], y: list[float] = []):
        self.x = x
        self.y = y

    def set(self, x: list[float], y: list[float]) -> None:
        self.x = x
        self.y = y

    def push(self, x: list[float], y: list[float]) -> None:
        self.x += x
        self.y += y

    def clear(self) -> None:
        self.x = []
        self.y = []

    @classmethod
    def new(cls, entry: TemporalData):
        if entry.position_data == "":
            x = []
            y = []
        else:
            x = list(map(float, entry.position_data.split(",")))
            y = list(map(float, entry.intensity_data.split(",")))

        return WaveForm(x=x, y=y)

    def transform(self):
        position = np.array(self.x) * 3500 / 10
        interval = abs(position[0] - position[-1]) / len(position)
        intensity = self.moving_average(self.y, int(6.0 // interval))

        self.x = position[:: int(6.0 // interval)].tolist()
        self.y = intensity[:: int(6.0 // interval)].tolist()

    def moving_average(self, x: np.ndarray, w: int) -> np.ndarray:
        return np.convolve(x, np.ones(w), "same") / w
