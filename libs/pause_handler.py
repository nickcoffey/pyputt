from typing import Callable, Optional


class PauseHandler:
    def __init__(self):
        self.seconds_to_pause = 0
        self.is_paused = False
        self.resume_cb: Optional[Callable]
        self.pause_cb: Optional[Callable]

    def start_pause(
        self,
        seconds: int,
        resume_cb: Optional[Callable] = None,
        pause_cb: Optional[Callable] = None,
    ):
        self.seconds_to_pause = seconds
        self.is_paused = True
        self.resume_cb = resume_cb
        self.pause_cb = pause_cb

    def decrement_frames(self, amount):
        if self.pause_cb is not None:
            self.pause_cb()

        self.seconds_to_pause = self.seconds_to_pause - amount
        if self.seconds_to_pause == 0 or self.seconds_to_pause < 0:
            if self.resume_cb is not None:
                self.resume_cb()
            self.is_paused = False
            self.seconds_to_pause = 0
            self.resume_cb = None
