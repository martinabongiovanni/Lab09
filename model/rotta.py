from dataclasses import dataclass

from model import airport


@dataclass
class Rotta:
    a1: airport.Airport
    a2: airport.Airport
    totDistance: float
    nVoli: int

    def __post_init__(self):
        self.avgDistance = float(self.totDistance / self.nVoli)
