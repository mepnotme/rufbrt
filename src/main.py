import pygame, sys
from pygame.locals import *

WORLD_WIDTH = 256
WORLD_HEIGHT = 256
COL_WIDTH = 32
FLOOR_HEIGHT = 24
PYRAMID_ORIGIN_X = 16   # coordenada x de la esquina superior izquierda donde se dibujará la pirámide
PYRAMID_ORIGIN_Y = 32   # coordenada y de la esquina superior izquierda donde se dibujará la pirámide
HERO_IMG_SHIFT_X = -105
HERO_IMG_SHIFT_Y = -112
BLOCK_IMG_SHIFT_X = -105
BLOCK_IMG_SHIFT_Y = -112

pyramid = [] # matriz que contiene información sobre todos los bloques del juego
hero_floor = 0
hero_col = 0

def mi_error(mensaje):
    print(f"ERROR: {mensaje}")
    pygame.quit()
    sys.exit()

def get_new_scale_factor(display_x_resolution, display_y_resolution):
    max_x_scale_factor = int(display_x_resolution / WORLD_WIDTH)
    max_y_scale_factor = int(display_y_resolution / WORLD_HEIGHT)
    new_scale_factor = min(max_x_scale_factor, max_y_scale_factor)
    new_scale_factor = max(1, new_scale_factor) # el factor de escala mínimo es 1
    return new_scale_factor

def init_game():
    global pyramid, hero_floor, hero_col
    pyramid = []
    floor_columns = 7
    for floor_number in range(7):
        floor = []
        for column in range(floor_columns):
            floor.append(0)
        pyramid.append(floor)
        floor_columns -= 1
    hero_floor = 6
    hero_col = 0

def screen_menu():
    global screen, scale_factor
    # lectura cola de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            new_x_resolution, new_y_resolution = event.dict['size']
            scale_factor = get_new_scale_factor(new_x_resolution, new_y_resolution)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                init_game()
                screen = "match"

    draw_surface.fill((0, 0, 0))
    draw_surface.blit(menu_title_img, ((WORLD_WIDTH - menu_title_img.get_width()) / 2, 100))
    draw_surface.blit(menu_subtitle_img, ((WORLD_WIDTH - menu_subtitle_img.get_width()) / 2, 150))


def coordinates_of_block(floor_number, col_number):
    x = PYRAMID_ORIGIN_X + COL_WIDTH * col_number + floor_number * COL_WIDTH / 2
    y = PYRAMID_ORIGIN_Y + (6 - floor_number) * FLOOR_HEIGHT
    return x, y


def draw_block(x, y):
    draw_surface.blit(block_img, (x + BLOCK_IMG_SHIFT_X, y + BLOCK_IMG_SHIFT_Y))


def draw_pyramid():
    for floor_number, blocks in enumerate(pyramid):
        for col_number in range(len(blocks)):
            x_block, y_block = coordinates_of_block(floor_number, col_number)
            #if floor_number == 6 and col_number == 0:
            #    print(f"Para floor_number {floor_number} y columna {col_number} -> x={x_block}, y={y_block}")
            draw_block(x_block, y_block)


def cell_exists(row, col):
    return 0 <= row <= 6 and 0 <= col <= 6 - row


def draw_hero(hero_floor, hero_col):
    hero_x, hero_y = coordinates_of_block(hero_floor, hero_col)
    draw_surface.blit(hero_img, (hero_x + HERO_IMG_SHIFT_X, hero_y + HERO_IMG_SHIFT_Y))


def screen_match():
    global scale_factor, hero_floor, hero_col

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            new_x_resolution, new_y_resolution = event.dict['size']
            scale_factor = get_new_scale_factor(new_x_resolution, new_y_resolution)
        elif event.type == pygame.KEYDOWN:
            dest_hero_row = hero_floor
            dest_hero_col = hero_col
            if event.key == K_q:  # Diagonal arriba-izquierda
                dest_hero_row = hero_floor + 1
                dest_hero_col = hero_col - 1
            elif event.key == K_w:  # Diagonal arriba-derecha
                dest_hero_row = hero_floor + 1
                dest_hero_col = hero_col
            elif event.key == K_a:  # Diagonal abajo-izquierda
                dest_hero_row = hero_floor - 1
                dest_hero_col = hero_col
            elif event.key == K_s:    # Diagonal abajo-derecha
                dest_hero_row = hero_floor - 1
                dest_hero_col = hero_col + 1
            if cell_exists(dest_hero_row, dest_hero_col):
                hero_floor = dest_hero_row
                hero_col = dest_hero_col

    draw_surface.fill((0, 0, 0))
    draw_pyramid()
    draw_hero(hero_floor, hero_col)


pygame.init()

# Definimos el factor inicial de escalado. Se usa para definir el tamaño inicial de la ventana
# del juego y para multiplicar la superficie draw_surface al mostrarla en display_surface
scale_factor = get_new_scale_factor(int(pygame.display.Info().current_w * 0.7), int(pygame.display.Info().current_h))

display_surface = pygame.display.set_mode((WORLD_WIDTH * scale_factor, WORLD_HEIGHT * scale_factor),  HWSURFACE | DOUBLEBUF | RESIZABLE)
draw_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),  HWSURFACE | DOUBLEBUF)

pygame.display.set_caption('rubrt')
font_title = pygame.font.Font("assets/daydream.ttf", 28)
font_paragraph = pygame.font.Font("assets/daydream.ttf", 11)
menu_title_img = font_title.render("rufbrt", False, (204, 96, 120))
menu_subtitle_img = font_paragraph.render("press space to start", False, (116, 220, 188))
block_img = pygame.image.load('assets/block_1.png')

hero_img = pygame.image.load('assets/hero_1.png')
screen = "menu"
while True:  # main game loop
    if screen == "menu":
        screen_menu()
    elif screen == "match":
        screen_match()
    else:
        mi_error("Pantalla no válida")

    scaled_draw_surface = pygame.transform.scale(draw_surface, (WORLD_WIDTH * scale_factor, WORLD_HEIGHT * scale_factor))
    display_surface.fill((0, 0, 0))
    display_surface.blit(scaled_draw_surface, ((display_surface.get_width() - scaled_draw_surface.get_width()) / 2, (display_surface.get_height() - scaled_draw_surface.get_height()) / 2))
    pygame.display.update()
