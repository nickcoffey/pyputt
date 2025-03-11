from utils.singleton import singleton


@singleton
class ParTracker:
    def __init__(self) -> None:
        self.shots = 0
        self.par = 0
