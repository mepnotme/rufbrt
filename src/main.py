import pygame, sys
from pygame.locals import *
from math import fabs

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
FRAMES_JUMPING = 6
JUMP_HEIGHT = 15    # altura máxima del salto del jugador (en píxeles)

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
    global pyramid, hero
    pyramid = []
    floor_columns = 7
    for floor_number in range(7):
        floor = []
        for column in range(floor_columns):
            floor.append(0)
        pyramid.append(floor)
        floor_columns -= 1
    hero["floor"] = 6
    hero["col"] = 0
    hero["state"] = "idle"

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
    draw_surface.blit(menu_rufus_img, ((0, 0)))
    draw_surface.blit(menu_title_img, ((68, 9)))
    draw_surface.blit(menu_subtitle_1_img, ((195, 160)))
    draw_surface.blit(menu_subtitle_2_img, ((195, 170)))
    draw_surface.blit(menu_subtitle_3_img, ((185, 180)))


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


def draw_hero(hero):
    hero_x, hero_y = coordinates_of_block(hero["floor"], hero["col"])
    if hero["state"] == "jumping":
        hero_dest_x, hero_dest_y = coordinates_of_block(hero["dest_floor"], hero["dest_col"])
        inc_x = (frame_counter - hero["state_init_counter"]) * (hero_dest_x - hero_x) / FRAMES_JUMPING
        inc_y = (frame_counter - hero["state_init_counter"]) * (hero_dest_y - hero_y) / FRAMES_JUMPING
        curve_y_inc = (1 - (1/(FRAMES_JUMPING / 2)) * fabs( frame_counter - hero["state_init_counter"] - 3)) * JUMP_HEIGHT
        #print(curve_y_inc)
    else:
        inc_x = 0
        inc_y = 0
        curve_y_inc = 0
    draw_surface.blit(hero["img"], (hero_x + HERO_IMG_SHIFT_X + inc_x, hero_y + HERO_IMG_SHIFT_Y + inc_y - curve_y_inc))

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
            dest_hero_floor = hero["floor"]
            dest_hero_col = hero["col"]
            if event.key == K_q and hero["state"] == "idle":  # Diagonal arriba-izquierda
                dest_hero_floor = hero["floor"] + 1
                dest_hero_col = hero["col"] - 1
            elif event.key == K_w and hero["state"] == "idle":  # Diagonal arriba-derecha
                dest_hero_floor = hero["floor"] + 1
                dest_hero_col = hero["col"]
            elif event.key == K_a and hero["state"] == "idle":  # Diagonal abajo-izquierda
                dest_hero_floor = hero["floor"] - 1
                dest_hero_col = hero["col"]
            elif event.key == K_s and hero["state"] == "idle":  # Diagonal abajo-derecha
                dest_hero_floor = hero["floor"] - 1
                dest_hero_col = hero["col"] + 1
            if (hero["floor"] != dest_hero_floor or hero["col"] != dest_hero_col) and cell_exists(dest_hero_floor, dest_hero_col):
                hero["dest_floor"] = dest_hero_floor
                hero["dest_col"] = dest_hero_col
                hero["state"] = "jumping"
                hero["state_init_counter"] = frame_counter  # contador para saber cuánto tiempo llevamos en este estado
    if hero["state"] == "jumping":
        if frame_counter - hero["state_init_counter"] > FRAMES_JUMPING:
            hero["floor"] = hero["dest_floor"]
            hero["col"] = hero["dest_col"]
            hero["state"] = "idle"

    draw_surface.fill((0, 0, 0))
    draw_pyramid()
    draw_hero(hero)


pygame.init()

# Definimos el factor inicial de escalado. Se usa para definir el tamaño inicial de la ventana
# del juego y para multiplicar la superficie draw_surface al mostrarla en display_surface
scale_factor = get_new_scale_factor(int(pygame.display.Info().current_w * 0.7), int(pygame.display.Info().current_h))

display_surface = pygame.display.set_mode((WORLD_WIDTH * scale_factor, WORLD_HEIGHT * scale_factor),  HWSURFACE | DOUBLEBUF | RESIZABLE)
draw_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),  HWSURFACE | DOUBLEBUF)

pygame.display.set_caption('rufbrt')
font_title = pygame.font.Font("assets/daydream.ttf", 28)
font_paragraph = pygame.font.Font("assets/daydream.ttf", 8)
menu_title_img = font_title.render("rufbrt", False, (240, 108, 124))
menu_rufus_img = pygame.image.load("assets/start_menu.png")
menu_subtitle_1_img = font_paragraph.render("press", False, (116, 220, 188))
menu_subtitle_2_img = font_paragraph.render("space", False, (116, 220, 188))
menu_subtitle_3_img = font_paragraph.render("to start", False, (116, 220, 188))


block_img = pygame.image.load('assets/block_1.png')

pyramid = []    # matriz que contiene información sobre todos los bloques del juego
hero = {
    "floor": 0,         # piso en el que se encuentra el héroe
    "col": 0,           # columna en la que se encuentra el héroe
    "state": "idle",    # estado en el que se encuentra el héroe ("idle", "jumping"...)
    "img": pygame.image.load('assets/hero_1.png'),
}

frame_counter = 0
screen = "menu"
clock = pygame.time.Clock()
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
    clock.tick(30)
    frame_counter += 1