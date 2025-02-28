# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
CLOCK = pygame.time.Clock()
RUNNING = True
DELTA_TIME = 0

PLAYER_POS = pygame.Vector2(SCREEN.get_width() / 2, SCREEN.get_height() / 2)
BALL_SPEED = 600
BALL_SIZE = 40


def check_bounds():
    if PLAYER_POS.x < BALL_SIZE:
        PLAYER_POS.x = BALL_SIZE
    elif PLAYER_POS.x > SCREEN.get_width() - BALL_SIZE:
        PLAYER_POS.x = SCREEN.get_width() - BALL_SIZE

    if PLAYER_POS.y < BALL_SIZE:
        PLAYER_POS.y = BALL_SIZE
    elif PLAYER_POS.y > SCREEN.get_height() - BALL_SIZE:
        PLAYER_POS.y = SCREEN.get_height() - BALL_SIZE


def move_ball():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
        PLAYER_POS.y -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_k]:
        PLAYER_POS.y += BALL_SPEED * DELTA_TIME
    if keys[pygame.K_j]:
        PLAYER_POS.x -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_l]:
        PLAYER_POS.x += BALL_SPEED * DELTA_TIME


while RUNNING:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill("green")
    pygame.draw.circle(SCREEN, "white", PLAYER_POS, BALL_SIZE)

    move_ball()
    check_bounds()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # delta time in seconds since last frame, used for framerate-independent physics.
    DELTA_TIME = CLOCK.tick(60) / 1000

pygame.quit()
