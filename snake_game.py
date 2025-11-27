from levels import level_dict
from constants import *
import random
import sys
import os
import pygame

pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)


def set_initial_values():
    level = 1
    lifes = START_LIFES

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            str_level = f.readline()

            if str_level:
                try:
                    saved_level = int(str_level)
                    if saved_level in level_dict:
                        level = saved_level
                    
                    saved_lifes = int(f.readline())
                    if 1 <= saved_lifes <= START_LIFES:
                        lifes = saved_lifes
                except ValueError:
                    pass

    return level, lifes


def append_level_coords(level_matrix):
    wall_rects = []
    free_positions = []
    pipe_coords = {num: [] for num in PIPE_IMAGES}
    pipe_collision_points = {num: [] for num in PIPE_IMAGES}

    for row in range(len(level_matrix)):
        for col in range(len(level_matrix[row])):
            current_element = level_matrix[row][col]
            x = col * SEGMENT_SIZE
            y = row * SEGMENT_SIZE

            if current_element == FREE:
                free_positions.append((x, y))

            elif current_element == BRICKS:
                wall_rect = pygame.Rect(x, y, BRICKS_IMG.get_rect().width, BRICKS_IMG.get_rect().height)
                wall_rects.append(wall_rect)

            elif current_element == HORIZONTAL_PIPE:
                pipe_coords[current_element].append((x, y))
                pipe_collision_points[HORIZONTAL_PIPE].extend(((x, y), (x + SEGMENT_SIZE, y),(x, y + 2 * SEGMENT_SIZE), (x + SEGMENT_SIZE, y + 2 * SEGMENT_SIZE)))
                               
            elif current_element == VERTICAL_PIPE:
                pipe_coords[current_element].append((x, y))
                pipe_collision_points[VERTICAL_PIPE].extend(((x, y), (x, y + SEGMENT_SIZE), (x + 2 * SEGMENT_SIZE, y), (x + 2 * SEGMENT_SIZE, y + SEGMENT_SIZE)))
   
    return free_positions, wall_rects, pipe_coords, pipe_collision_points


def get_random_apple():
    rand_img_path = random.choice(APPLE_PATHS)
    apple_img = pygame.image.load(rand_img_path)
    apple_img = pygame.transform.scale(apple_img, (APPLE_SIZE, APPLE_SIZE))
    return apple_img
    #return pygame.transform.scale(pygame.image.load(random.choice(APPLE_PATHS)), (APPLE_SIZE, APPLE_SIZE))


def check_for_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if level > 1:
                WINDOW.blit(SAVE_SURFACE, (WIDTH / 2 - SAVE_SURFACE_WIDTH / 2, HEIGHT / 2 - SAVE_SURFACE_HEIGHT / 2))
                WINDOW.blit(SAVE_TEXT_1, SAVE_RECT_1)
                WINDOW.blit(SAVE_TEXT_2, SAVE_RECT_2)
                pygame.display.update()              

                loop = 1
                while loop:
                    for save_event in pygame.event.get():
                        if save_event.type == pygame.KEYDOWN:
                            loop = 0
                            with open(SAVE_FILE, 'w') as f:
                                if save_event.key == pygame.K_y:
                                    f.write(str(level) + '\n')
                                    f.write(str(lifes))
                                else:
                                    f.write('')
            else:
                with open(SAVE_FILE, 'w') as f:
                    f.write('')
                    
            pygame.quit()
            sys.exit()


def check_for_pause(pressed_keys):    
    if pressed_keys[pygame.K_SPACE]:
        game_paused = 1
        while game_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    game_paused = 0


def get_direction(keys, direction):
    if keys[pygame.K_LEFT] and direction != RIGHT and direction is not None:
        direction = LEFT
    elif keys[pygame.K_RIGHT] and direction != LEFT:
        direction = RIGHT
    elif keys[pygame.K_UP] and direction != DOWN:
        direction = UP
    elif keys[pygame.K_DOWN] and direction != UP:
        direction = DOWN
        
    return direction


def set_if_out_of_screen(x, y):
    if x >= WIDTH:
        x = 0
    elif x < 0:
        x = WIDTH - SEGMENT_SIZE

    if y >= HEIGHT:
        y = 0
    elif y < 0:
        y = HEIGHT - SEGMENT_SIZE

    return x, y


def check_pipe_collision(pipe_collision_points, x, y, prev_x, prev_y):
    for pipe_type in pipe_collision_points:
        for point_x, point_y in pipe_collision_points[pipe_type]:
            if pipe_type == HORIZONTAL_PIPE and (point_x == prev_x == x):
                if (y == point_y and prev_y < point_y) or (prev_y == point_y and y < point_y):
                    return True
            elif pipe_type == VERTICAL_PIPE and (point_y == prev_y == y):
                if (x == point_x and prev_x < point_x) or (prev_x == point_x and x < point_x):
                    return True
    return False


def draw_grid():
    WINDOW.fill(LIGHT_GREEN)
    for row in range(HEIGHT // SEGMENT_SIZE):
        for col in range(row % 2, WIDTH // SEGMENT_SIZE, 2):
            pygame.draw.rect(WINDOW, DARK_GREEN, (col * SEGMENT_SIZE, row * SEGMENT_SIZE, SEGMENT_SIZE, SEGMENT_SIZE))


def draw_walls(wall_rects):
    for wall_rect in wall_rects:
        WINDOW.blit(BRICKS_IMG, wall_rect)


def draw_score(score):
    score_text = FONT.render(f'{SCORE_TXT} {score}', True, WHITE)
    WINDOW.blit(score_text, SCORE_RECT)


def draw_level_text(level):
    level_text = FONT.render(f'{LEVEL_TXT} {level}', True, WHITE)
    WINDOW.blit(level_text, LEVEL_RECT)


def draw_hearts(lifes):
    for index in range(lifes):
        WINDOW.blit(HEART_IMAGE, (HEARTS_OFFCET_X + index * HEART_IMAGE.get_rect().width, HEARTS_OFFCET_Y))


def draw_body(snake_segments):
    for seg_x, seg_y in snake_segments:
        WINDOW.blit(BODY_IMAGE, (seg_x, seg_y, SEGMENT_SIZE, SEGMENT_SIZE))


def draw_food(apple_img, food_rect):
    blit_rect = apple_img.get_rect()
    blit_rect.center = food_rect.center
    WINDOW.blit(apple_img, (blit_rect))


def draw_head(x, y, direction):
    head_image = HEAD_IMAGES[direction]
    head_rect = head_image.get_rect()
    head_rect.center = (x + SEGMENT_SIZE / 2, y + SEGMENT_SIZE / 2)
    WINDOW.blit(HEAD_IMAGES[direction], head_rect)


def draw_pipes(pipe_coords): 
    for num in pipe_coords:
        for x, y in pipe_coords[num]:
            WINDOW.blit(PIPE_IMAGES[num], (x - HEAD_OVERFLOW / 2, y - HEAD_OVERFLOW / 2, PIPE_IMG_1.get_width(), PIPE_IMG_1.get_height()))


def redraw_sreen(wall_rects, score, snake_segments, apple_img, food_rect, x, y, direction, pipe_coords):
    draw_grid()
    draw_walls(wall_rects)
    draw_score(score)
    draw_level_text(level)
    WINDOW.blit(GOAL_TEXT, GOAL_RECT)
    draw_hearts(lifes)
    draw_body(snake_segments)
    draw_food(apple_img, food_rect)
    draw_head(x, y, direction)
    draw_pipes(pipe_coords)
    pygame.display.update()


def play_sound(sound):
    try:
        sound.play()
    except:
        pass


def draw_stars(x, y):
    STARS_RECT_1.center = (x + SEGMENT_SIZE / 2, y + SEGMENT_SIZE / 2)
    WINDOW.blit(STARS_IMAGE_1, STARS_RECT_1)
    pygame.display.update(STARS_RECT_1)
    pygame.time.delay(COLLISION_DELAY // 2)

    STARS_RECT_2.center = (STARS_RECT_1.center)
    WINDOW.blit(STARS_IMAGE_2, STARS_RECT_2)
    pygame.display.update(STARS_RECT_2)
    pygame.time.delay(COLLISION_DELAY)


def reset_lifes_and_level(lifes, level):
    if lifes > 0:
        return lifes, level
    return START_LIFES, 1


def draw_goal_reached_message(level_dict):
    if level < len(level_dict):
        WINDOW.blit(NEXT_LEVEL_TEXT, NEXT_LEVEL_RECT)
        pygame.display.update(NEXT_LEVEL_RECT)
        pygame.time.delay(COLLISION_DELAY)
    else:
        WINDOW.blit(CONGRATULATIONS_TEXT, CONGRATULATIONS_RECT)
        pygame.display.update(CONGRATULATIONS_RECT)
        while 1:
            check_for_quit()

    
def play_level():
    global lifes, level
    score = 0
    counter = 0
    
    level_matrix = level_dict[level]
    free_positions, wall_rects, pipe_coords, pipe_collision_points = append_level_coords(level_matrix)

    food_x, food_y = random.choice(free_positions)
    food_rect = pygame.Rect(food_x, food_y, SEGMENT_SIZE, SEGMENT_SIZE)
    apple_img = get_random_apple()

    x, y = START_X, START_Y
    prev_head_position = (x, y)

    snake_segments = []
    snake_segments.append(prev_head_position)
    snake_segments.append(prev_head_position)

    direction = None

    CLOCK = pygame.time.Clock()
    fps = START_FPS

    while 1:
        check_for_quit()
        keys = pygame.key.get_pressed()
        check_for_pause(keys)
        
        direction = get_direction(keys, direction)
        x_move, y_move = MOVES[direction]

        if counter < MOVE_DELAY:
            counter += 1
        else:
            counter = 0

            prev_head_position = (x, y)        
            x += x_move
            y += y_move            
            x, y = set_if_out_of_screen(x, y)

            collide_rect = pygame.Rect(x, y, SEGMENT_SIZE, SEGMENT_SIZE)            
            pipe_collision = check_pipe_collision(pipe_collision_points, x, y, *prev_head_position)
                 
            if collide_rect.collidelist(wall_rects) >= 0 or pipe_collision:
                lifes -= 1
                x -= x_move
                y -= y_move

                redraw_sreen(wall_rects, score, snake_segments, apple_img, food_rect, x, y, direction, pipe_coords)
                pygame.time.delay(COLLISION_DELAY // 3)   

                play_sound(LOSE_SOUND)
                pygame.time.delay(COLLISION_DELAY // 2)

                draw_stars(x, y)
                WINDOW.fill(DARK_GREEN)
                WINDOW.blit(YOU_LOSE_TEXT, YOU_LOSE_RECT)
                pygame.display.update()
                pygame.time.delay(COLLISION_DELAY)                            
                
                lifes, level = reset_lifes_and_level(lifes, level)
                play_level()

            if not collide_rect.collidepoint(food_rect.center):
                snake_segments.pop()

            else:
                play_sound(CRUNCHY_SOUND)

                score += 1
                if score == GOAL:
                    snake_segments.insert(0, prev_head_position)

                    redraw_sreen(wall_rects, score, snake_segments, apple_img, food_rect, x, y, direction, pipe_coords)                    
                    pygame.time.delay(COLLISION_DELAY)

                    play_sound(LEVEL_COMPLETED_SOUND)
                    pygame.time.delay(COLLISION_DELAY)

                    if level == len(level_dict):
                        play_sound(GAME_COMPLETED_SOUND)
                    pygame.time.delay(COLLISION_DELAY)

                    draw_goal_reached_message(level_dict)
                    pygame.time.delay(COLLISION_DELAY // 2)

                    level += 1
                    play_level()

                food_rect.x, food_rect.y = random.choice(free_positions)
                apple_img = get_random_apple()            

            snake_segments.insert(0, prev_head_position)    
            redraw_sreen(wall_rects, score, snake_segments, apple_img, food_rect, x, y, direction, pipe_coords)                  
               
        CLOCK.tick(fps)


if __name__ == '__main__' :
    level, lifes = set_initial_values()
    play_level()
