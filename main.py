import pygame
import sys
import random


def create_and_scale(path_to_image):
    obj = pygame.image.load(path_to_image)
    obj = pygame.transform.scale2x(obj)
    return obj


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score, welcome
    welcome = False
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            lose_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        lose_sound.play()
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


def score_display(game_state):
    global high_score_ability
    if game_state == 'main_game':
        score_surface = game_font.render(str(score), True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(288 + 4, 100 + 4))
        screen.blit(score_surface, score_rect)
        score_surface = game_font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
        if score > high_score:
            if high_score_ability:
                high_score_ability = False
                high_score_sound.play()

    if game_state == 'game_over':
        score_surface = game_font.render(f"Score: {str(score)}", True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(288+4, 100+4))
        screen.blit(score_surface, score_rect)
        score_surface = game_font.render(f"Score: {str(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(288 + 4, 850 + 4))
        screen.blit(high_score_surface, high_score_rect)
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(actual_score, actual_high_score):
    global high_score_ability
    if actual_score > actual_high_score:
        actual_high_score = actual_score

    return actual_high_score


def set_to_default():
    global bg_surface, floor_surface, pipe_surface, fps, high_score_ability, nyan_ability, cyber_ability, christmas_ability, dorime_ability
    fps = 80
    bg_surface = create_and_scale('assets/background-day.png')
    floor_surface = create_and_scale('assets/base.png')
    pipe_surface = create_and_scale('assets/pipe-green.png')
    high_score_ability = True
    nyan_ability = True
    cyber_ability = True
    christmas_ability = True
    dorime_ability = True


def music_stop():
    cyber_sound.stop()
    nyan_sound.stop()
    christmas_sound.stop()
    dorime_sound.stop()


# Game variables
gravity = 0.25
bird_movement = 0
game_active = False
welcome = True
score = 0
high_score = 0
high_score_ability = True
can_score = True
fps = 80
nyan_ability = True
cyber_ability = True
christmas_ability = True
dorime_ability = True

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/04B_19.ttf', 40)

bg_surface = create_and_scale('assets/background-day.png')

floor_surface = create_and_scale('assets/base.png')
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = create_and_scale('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)
pipe_height = [400, 600, 800]

game_over_surface = create_and_scale('assets/message.png')
game_over_rect = game_over_surface.get_rect(center=(288, 512))

welcome_surface = create_and_scale('assets/hello_screen.png')
welcome_rect = welcome_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('sound/wing.wav')
death_sound = pygame.mixer.Sound('sound/hit.wav')
lose_sound = pygame.mixer.Sound('sound/die.wav')
score_sound = pygame.mixer.Sound('sound/point.wav')
switch1_sound = pygame.mixer.Sound('sound/switch1.wav')
switch2_sound = pygame.mixer.Sound('sound/switch2.wav')
switch3_sound = pygame.mixer.Sound('sound/switch3.wav')
high_score_sound = pygame.mixer.Sound('sound/hooray.wav')
nyan_sound = pygame.mixer.Sound('sound/nyan.wav')
cyber_sound = pygame.mixer.Sound('sound/cyber.wav')
christmas_sound = pygame.mixer.Sound('sound/christmas.wav')
dorime_sound = pygame.mixer.Sound('sound/dorime.mp3')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()

            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

            if event.key == pygame.K_a and welcome:  # choose red bird
                welcome_surface = create_and_scale('assets/hello_screen_a.png')
                bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
                bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
                bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
                bird_frames = [bird_downflap, bird_midflap, bird_upflap]
                switch3_sound.play()

            if event.key == pygame.K_d and welcome:  # choose yellow bird
                welcome_surface = create_and_scale('assets/hello_screen_d.png')
                bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
                bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
                bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
                bird_frames = [bird_downflap, bird_midflap, bird_upflap]
                switch2_sound.play()

            if event.key == pygame.K_s and welcome:  # choose blue bird
                welcome_surface = create_and_scale('assets/hello_screen_s.png')
                bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
                bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
                bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
                bird_frames = [bird_downflap, bird_midflap, bird_upflap]
                switch1_sound.play()

            if event.key == pygame.K_b and not game_active:
                welcome = True
                switch1_sound.play()

        if 15 <= score <= 16 and game_active:
            floor_surface = create_and_scale('assets/base.png')
            pipe_surface = create_and_scale('assets/orange-pipe.png')
            bg_surface = create_and_scale('assets/background-night.png')

        if 30 <= score <= 31 and game_active:
            nyan_sound.stop()
            if cyber_ability:
                cyber_ability = False
                cyber_sound.play()
            floor_surface = create_and_scale('assets/cyber-base.png')
            pipe_surface = create_and_scale('assets/pipe-cyber.png')
            bg_surface = create_and_scale('assets/background-cyber.jpg')

        if 45 <= score <= 46 and game_active:
            cyber_sound.stop()
            if christmas_ability:
                christmas_ability = False
                christmas_sound.play()

            floor_surface = create_and_scale('assets/winter-base.png')
            pipe_surface = create_and_scale('assets/pipe-winter-blue.png')
            bg_surface = create_and_scale('assets/winter.jpg')

        if 60 <= score <= 61 and game_active:
            christmas_sound.stop()
            if nyan_ability:
                nyan_ability = False
                nyan_sound.play()
            floor_surface = create_and_scale('assets/nyan-base.png')
            pipe_surface = create_and_scale('assets/pipe-violet.png')
            bg_surface = create_and_scale('assets/background-nyan.jpg')

        if 75 <= score <= 76 and game_active:
            nyan_sound.stop()
            if dorime_ability:
                dorime_ability = False
                dorime_sound.play(-1)
            floor_surface = create_and_scale('assets/hell-base.png')
            pipe_surface = create_and_scale('assets/pipe-red.png')
            bg_surface = create_and_scale('assets/hell2.jpg')

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()
        score_display('main_game')

    elif welcome and not game_active:  # welcome screen
        screen.blit(welcome_surface, welcome_rect)

    elif not game_active:
        music_stop()
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        set_to_default()

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(fps)
