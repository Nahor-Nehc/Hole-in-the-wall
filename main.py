import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

WIDTH, HEIGHT = 960, 560

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
pygame.display.set_caption("Time platformer")

# fonts
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)
TITLEFONT = FONT(70)

# file locations
from os import path
PATH_TO_ATLAS_IMAGE = path.join("assets", "images", "atlas.bmp")
PATH_TO_LEVELS = path.join("assets", "levels", "levels")

def draw():
  pygame.display.update()

def main():
  clock = pygame.time.Clock()
  
  # remove unnecessary events from event list
  pygame.event.set_blocked(None)
  pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
  #pygame.event.set_allowed(USEREVENTS)
  
  from components.state import State
  from components.textures import TextureAtlas
  
  # GAME VARIABLES
  state = State("start")
  
  texture_atlas = TextureAtlas(PATH_TO_ATLAS_IMAGE)
  
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
        if state.get_state() == "start":
          if event.key == pygame.K_e: # temp
            state.set_state("editor mode")
    
    draw()

main()