import pygame

pygame.init()

WIDTH = 950
HEIGHT = 650
SEGMENT_SIZE = 25

CAPTION = 'Snake Game'
GOAL = 30
START_X = 0
START_Y = 50
START_LIFES = 5
START_FPS = 60
MOVE_DELAY = 10
COLLISION_DELAY = 1000
TEXT_OFFCET = 10
FREE = 0
BRICKS = 1
HORIZONTAL_PIPE = 3
VERTICAL_PIPE = 4

WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 200, 0)
DARK_GREEN = (0, 180, 0)

APPLE_PATHS = ['./images/red-apple.png', './images/green-apple.png', './images/apple-worm.png', './images/yellow-apple.png']
APPLE_SIZE = 30
APPLE_OVERFLOW = APPLE_SIZE - SEGMENT_SIZE
HEAD_SIZE = 40
HEAD_OVERFLOW = HEAD_SIZE - SEGMENT_SIZE

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

MOVES = {
    RIGHT: (SEGMENT_SIZE, 0),
    LEFT: (-SEGMENT_SIZE, 0),
    UP: (0, -SEGMENT_SIZE),
    DOWN: (0, SEGMENT_SIZE),
    None: (0, 0)
}

HEAD_IMAGE_DOWN = pygame.transform.scale(pygame.image.load('./images/head.png'), (HEAD_SIZE, HEAD_SIZE))
HEAD_IMAGE_LEFT = pygame.transform.rotate(HEAD_IMAGE_DOWN, -90)
HEAD_IMAGE_RIGHT = pygame.transform.rotate(HEAD_IMAGE_DOWN, 90)
HEAD_IMAGE_UP = pygame.transform.rotate(HEAD_IMAGE_DOWN, 180)

HEAD_IMAGES = {
    LEFT: HEAD_IMAGE_LEFT,
    RIGHT: HEAD_IMAGE_RIGHT,
    UP: HEAD_IMAGE_UP,
    DOWN: HEAD_IMAGE_DOWN,
    None: HEAD_IMAGE_RIGHT
}

BODY_IMAGE = pygame.transform.scale(pygame.image.load('./images/body.png'), (SEGMENT_SIZE, SEGMENT_SIZE))
BRICKS_IMG = pygame.transform.scale(pygame.image.load('./images/bricks.png'), (SEGMENT_SIZE * 2, SEGMENT_SIZE * 2))

PIPE_IMG_1 = pygame.transform.scale(pygame.image.load('./images/pipe_no_ends.png'), (SEGMENT_SIZE * 2 + HEAD_OVERFLOW, SEGMENT_SIZE * 2 + HEAD_OVERFLOW))
PIPE_IMG_2 = pygame.transform.rotate(PIPE_IMG_1, 90)

PIPE_IMAGES = {
    HORIZONTAL_PIPE: PIPE_IMG_1,
    VERTICAL_PIPE: PIPE_IMG_2,
}

HEART_IMAGE = pygame.transform.scale(pygame.image.load('./images/heart.png'), (33, 33))

STARS_IMAGE_2 = pygame.transform.scale(pygame.image.load('./images/stars.png'), (HEAD_SIZE * 2 - HEAD_OVERFLOW, HEAD_SIZE * 2 - HEAD_OVERFLOW))
STARS_RECT_2 = STARS_IMAGE_2.get_rect()

STARS_IMAGE_1 = pygame.transform.scale(STARS_IMAGE_2, (SEGMENT_SIZE * 2, SEGMENT_SIZE * 2))
STARS_IMAGE_1 = pygame.transform.rotate(STARS_IMAGE_1, 30)
STARS_RECT_1 = STARS_IMAGE_1.get_rect()

#FONT = pygame.font.Font('freesansbold.ttf', 32)
FONT = pygame.font.SysFont('Comic Sans MS', 32, bold=True, italic=False)

SCORE_TXT = 'Score:'
score_text = FONT.render(f'{SCORE_TXT} 00', True, (WHITE))
SCORE_RECT = score_text.get_rect()
SCORE_RECT.x, SCORE_RECT.y = TEXT_OFFCET, TEXT_OFFCET // 4

HEARTS_OFFCET_X = SCORE_RECT.width + TEXT_OFFCET * 2
HEARTS_OFFCET_Y = 7

LEVEL_TXT = 'Level'
level_text = FONT.render(f'{LEVEL_TXT} 55', True, (WHITE))
LEVEL_RECT = level_text.get_rect()
LEVEL_RECT.x = WIDTH / 2 - LEVEL_RECT.width / 2
LEVEL_RECT.y = TEXT_OFFCET // 4

GOAL_TEXT = FONT.render(f'Goal: {GOAL}', True, (WHITE))
GOAL_RECT = GOAL_TEXT.get_rect()
GOAL_RECT.x = WIDTH - TEXT_OFFCET - GOAL_RECT.width
GOAL_RECT.y = TEXT_OFFCET // 4

NEXT_LEVEL_TEXT = FONT.render('GOAL REACHED!  NEXT LEVEL LOADING...', True, WHITE, DARK_GREEN)
NEXT_LEVEL_RECT = NEXT_LEVEL_TEXT.get_rect()
NEXT_LEVEL_RECT.x = WIDTH / 2 - NEXT_LEVEL_RECT.width / 2
NEXT_LEVEL_RECT.y = HEIGHT / 2 - NEXT_LEVEL_RECT.height / 2

YOU_LOSE_TEXT = FONT.render('YOU LOSE!  RELOADING LEVEL...', True, WHITE)
YOU_LOSE_RECT = YOU_LOSE_TEXT.get_rect()
YOU_LOSE_RECT.x = WIDTH / 2 - YOU_LOSE_RECT.width / 2
YOU_LOSE_RECT.y = HEIGHT / 2 - YOU_LOSE_RECT.height / 2

CONGRATULATIONS_TEXT = FONT.render('CONGRATULATIONS!  ALL LEVELS COMPLETED!', True, WHITE, DARK_GREEN)
CONGRATULATIONS_RECT = CONGRATULATIONS_TEXT.get_rect()
CONGRATULATIONS_RECT.x = WIDTH / 2 - CONGRATULATIONS_RECT.width / 2
CONGRATULATIONS_RECT.y = HEIGHT / 2 - CONGRATULATIONS_RECT.height / 2

SAVE_SURFACE_WIDTH = 650
SAVE_SURFACE_HEIGHT = 200
SAVE_SURFACE = pygame.Surface((SAVE_SURFACE_WIDTH, SAVE_SURFACE_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
SAVE_SURFACE.fill((*DARK_GREEN, 240))

SAVE_TEXT_1 = FONT.render('Do you want to save your progress?', True, WHITE)
SAVE_RECT_1 = SAVE_TEXT_1.get_rect()
SAVE_RECT_1.x = WIDTH / 2 - SAVE_RECT_1.width / 2
SAVE_RECT_1.y = 260

SAVE_TEXT_2 = FONT.render('Y for Yess, any key for No', True, WHITE)
SAVE_RECT_2 = SAVE_TEXT_2.get_rect()
SAVE_RECT_2.x = WIDTH / 2 - SAVE_RECT_2.width / 2
SAVE_RECT_2.y = 340

try:
    CRUNCHY_SOUND = pygame.mixer.Sound('./sound_effects/crunchy_sound.mp3')
    LOSE_SOUND = pygame.mixer.Sound('./sound_effects/lose_sound.wav')
    LEVEL_COMPLETED_SOUND = pygame.mixer.Sound('./sound_effects/completed_level_sound.wav')
    GAME_COMPLETED_SOUND = pygame.mixer.Sound('./sound_effects/final_sound.wav')
except:
    pass

SAVE_FILE = 'save_level.txt'
