from typing import TypedDict
from utils.singleton import singleton

PastHoleType = TypedDict("PastHoleType", {"shots": int, "par": int})


@singleton
class ParTracker:
    def __init__(self) -> None:
        self.shots = 0
        self.par = 0
        self.past_holes: list[PastHoleType] = []

    def next_hole(self, new_par: int) -> None:
        self.past_holes.append({"shots": self.shots, "par": self.par})
        self.par = new_par
        self.shots = 0
