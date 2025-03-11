from typing import TypedDict

from pygame import Surface
from pygame.font import Font
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

    def show_game_over_screen(self, screen: Surface, font: Font):
        self.next_hole(0)
        score = 0
        for hole in self.past_holes:
            score += hole["shots"] - hole["par"]

        game_over_text = font.render(
            "GAME OVER",
            True,
            (255, 255, 255),
            (0, 0, 0),
        )
        game_over_text_rect = game_over_text.get_rect(center=(1280 / 2, (720 / 2) - 50))
        score_text = font.render(
            f"Score: {score}",
            True,
            (255, 255, 255),
            (0, 0, 0),
        )
        score_text_rect = score_text.get_rect(center=(1280 / 2, (720 / 2) + 50))
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
