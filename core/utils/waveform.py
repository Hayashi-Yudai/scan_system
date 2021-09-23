from core.models import TemporalData


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
