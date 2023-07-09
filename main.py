import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

WIDTH, HEIGHT = 560, 560

FPS = 30

# general colours
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
RED =    (211,   0,   0)
GREEN =  (  0, 150,   0)
DGREEN = (  0, 100,   0)
BLUE =   (  0,   0, 211)
LBLUE =  (137, 207, 240)
GREY =   (201, 201, 201)
LGREY =  (231, 231, 231)
DGREY =  ( 50,  50,  50)
LBROWN = (185, 122,  87)
DBROWN = (159, 100,  64)

# display window that is drawn to
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hole in the wall")

# sizes
SIZE = 50
PLAYER_BOUNDS = {
  "top": HEIGHT/3*2 - SIZE*2,
  "bottom": HEIGHT/3*2 + SIZE*2,
  "left": WIDTH/2 - SIZE*2,
  "right": WIDTH/2 + SIZE*2
}

# fonts
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)
TITLEFONT = FONT(70)

# file locations
from os import path
PATH_TO_ATLAS_IMAGE = path.join("assets", "images", "atlas.bmp")
PATH_TO_LEVELS = path.join("assets", "levels", "levels")

def handle_events(player, mouse, state):
  for event in pygame.event.get():
    #if the "x" button is pressed ...
    if event.type == pygame.QUIT:
      #save game with shelve?
      #
      #ends game loop
      run = False

      #terminates pygame
      pygame.quit()

      #terminates system
      import sys
      sys.exit()
      
    if state.get_state() == "game":
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          player.move(-1*SIZE, 0)
        elif event.key == pygame.K_RIGHT:
          player.move(SIZE, 0)
        elif event.key == pygame.K_UP:
          player.move(0, -1 * SIZE)
        elif event.key == pygame.K_DOWN:
          player.move(0, SIZE)
        
        elif event.key == pygame.K_e:
          state.set_state("editor")
    
    elif state.get_state() == "editor":
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_g:
          state.set_state("game")

def process_game(player, blocks, state):
  if state.get_state() == "game":
    blocks.move()
    player.update()

def draw(WIN, player, blocks, state):
  WIN.fill(BLACK)
  if state.get_state() == "game":
    player.draw(WIN)
    blocks.draw(WIN)
    
  if state.get_state() == "editor":
    blocks.draw(WIN)
    
    for i in range(0, 5):
      pygame.draw.line(
        WIN,
        WHITE,
        (PLAYER_BOUNDS["left"] + SIZE*i, 0),
        (PLAYER_BOUNDS["left"] + SIZE*i, HEIGHT)
        )
    
    for i in range(0, 5):
      pygame.draw.line(
        WIN,
        WHITE,
        (0, PLAYER_BOUNDS["top"] + SIZE*i),
        (WIDTH, PLAYER_BOUNDS["top"] + SIZE*i))
    
  pygame.display.update()

def main():
  clock = pygame.time.Clock()
  
  # remove unnecessary events from event list
  pygame.event.set_blocked(None)
  pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
  #pygame.event.set_allowed(USEREVENTS)
  
  from components.state import State
  #from components.textures import TextureAtlas
  from components.player import Player
  from components.blocks import Block, Blocks
  
  # GAME VARIABLES
  state = State("game")
  player_surface = pygame.Surface((SIZE, SIZE))
  player_surface.fill(WHITE)
  player = Player(PLAYER_BOUNDS["left"], PLAYER_BOUNDS["top"], player_surface, PLAYER_BOUNDS)
  
  blocks = Blocks()
  blocks.toggle_see_collision_box()
  
  #texture_atlas = TextureAtlas(PATH_TO_ATLAS_IMAGE)
  
  # DEBUG MODE
  debug_mode = True
  
  #initiates game loop
  run = 1
  while run:
    
    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()
    
    #for everything that the user has inputted ...
    handle_events(player, mouse, state)
    
    process_game(player, blocks, state)
    
    draw(WIN, player, blocks, state)

main()