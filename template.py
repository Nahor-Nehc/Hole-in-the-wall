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

# fonts
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)
TITLEFONT = FONT(70)

# file locations
from os import path
PATH_TO_ATLAS_IMAGE = path.join("assets", "images", "atlas.bmp")
PATH_TO_LEVELS = path.join("assets", "levels", "levels")

def handle_events(player, mouse):
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
      
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        player.move(-50, 0)
      elif event.key == pygame.K_RIGHT:
        player.move(50, 0)
      elif event.key == pygame.K_UP:
        player.move(0, -50)
      elif event.key == pygame.K_DOWN:
        player.move(0, 50)

def process_game(blocks):
  blocks.move()

def draw(WIN, player, blocks):
  WIN.fill(BLACK)
  player.draw(WIN)
  blocks.draw(WIN)
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
  state = State("start")
  player_surface = pygame.Surface((50, 50))
  player_surface.fill(WHITE)
  player = Player(200, 200, player_surface)
  
  blocks = Blocks()
  blocks.toggle_see_collision_box()
  
  blocks.create(100, 100, 50, 50, WHITE, 2, 0.7)
  blocks.create(200, 100, 100, 50, WHITE, 2, 0.7)
  
  blocks.create(100, 0, 50, 50, WHITE, 2, 0.7)
  blocks.create(200, 0, 100, 50, WHITE, 2, 0.7)
  
  blocks.create(100, -100, 100, 50, WHITE, 2, 0.7)
  blocks.create(250, -100, 50, 50, WHITE, 2, 0.7)
  
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
    handle_events(player, mouse)
    
    process_game(blocks)
    
    draw(WIN, player, blocks)

main()