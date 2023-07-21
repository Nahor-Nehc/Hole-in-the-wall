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

# == # == # == # == # == #

# sizes
SIZE = round(WIDTH/(11.2))
PADDING = SIZE/3

top = int(HEIGHT/3*2 - SIZE*2)
PLAYER_BOUNDS = {
  "top": top,
  "bottom": top + SIZE*4,
  "left": WIDTH/2 - SIZE*2,
  "right": WIDTH/2 + SIZE*2
}

# == # == # == # == # == #

# control panel measurements
width =  round(HEIGHT - PLAYER_BOUNDS["right"] - PADDING*2)
height = round(PLAYER_BOUNDS["top"] - PADDING*2)

b_width = (width-PADDING*2)/3
b_height = (width-PADDING*2)/3

s_width = width
s_height = b_height

# right control panel
x = PLAYER_BOUNDS["right"] + PADDING
y = PADDING

# buttons on right control panel
FAST_BACKWARD_BUTTON = pygame.Rect(x, y, b_width, b_height)
PLAY_BUTTON = pygame.Rect(x + PADDING + b_width, y, b_width, b_height)
FAST_FORWARD_BUTTON = pygame.Rect(x + PADDING*2 + b_width*2, y, b_width, b_height)

# left control panel
x = PADDING
y = PADDING + SIZE

# buttons/sliders on left control panel

BLOCK_WIDTH_SLIDER = pygame.Rect(x, y, s_width, s_height)
BLOCK_HEIGHT_SLIDER = pygame.Rect(x, y + s_height + PADDING, s_width, s_height)
BLOCK_SPEED_SLIDER = pygame.Rect(x, y + s_height*2 + PADDING*2, s_width, s_height)

#tile_size_slider

# == # == # == # == # == #

# user events
TO_GAME = pygame.USEREVENT + 1
TO_EDITOR = pygame.USEREVENT + 2
EDITOR_PLAY = pygame.USEREVENT + 3
FAST_BACKWARD = pygame.USEREVENT + 4
FAST_FORWARD = pygame.USEREVENT + 5
USEREVENTS = [TO_GAME, TO_EDITOR, EDITOR_PLAY, FAST_BACKWARD, FAST_FORWARD]

# == # == # == # == # == #

# fonts
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)
TITLEFONT = FONT(70)
GAMEOVER_FONT = FONT(50)
SLIDER_FONT = FONT(20)

# == # == # == # == # == #

# file locations
from os import path
PATH_TO_LEVELS = path.join("assets", "levels", "levels") # last levels is the shelve file itself

# == # == # == # == # == #

# unicode characters
FAST_FORWARD_IMAGE = pygame.transform.scale(pygame.image.load(path.join("assets", "images", "forward_button.png")), (b_width, b_height)).convert_alpha()
PLAY_IMAGE = pygame.transform.scale(pygame.image.load(path.join("assets", "images", "play_button.png")), (b_width, b_height)).convert_alpha()
PAUSE_IMAGE = pygame.transform.scale(pygame.image.load(path.join("assets", "images", "pause_button.png")), (b_width, b_height)).convert_alpha()
FAST_BACKWARD_IMAGE = pygame.transform.scale(pygame.image.load(path.join("assets", "images", "back_button.png")), (b_width, b_height)).convert_alpha()

# == # == # == # == # == #

def handle_events(player, mouse, state, blocks, pen, buttons, editor_sliders):
  
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
    
    # CLASS UPDATERS
    editor_sliders.update(pygame.mouse)

    if event.type == pygame.MOUSEBUTTONDOWN:
      if pygame.mouse.get_pressed()[0]:
        buttons.check(mouse)
      
    # GAME MODE
    if state.get_state() == "game":
      if state.get_substate() == "play":
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
            pygame.event.post(pygame.event.Event(TO_EDITOR))
    
    # EDITOR MODE
    elif state.get_state() == "editor":
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_g:
          pygame.event.post(pygame.event.Event(TO_GAME))

      if state.get_substate() == "play":
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            player.move(-1*SIZE, 0)
          elif event.key == pygame.K_RIGHT:
            player.move(SIZE, 0)
          elif event.key == pygame.K_UP:
            player.move(0, -1 * SIZE)
          elif event.key == pygame.K_DOWN:
            player.move(0, SIZE)
      
      if state.get_substate() == "paused":
        if event.type == pygame.MOUSEBUTTONDOWN:
          if pygame.mouse.get_pressed()[0]:
            print()
            print(blocks.blocks)
            print("drew")
            pen.draw(blocks, mouse)
            print(blocks.blocks)
        
        elif event.type == pygame.MOUSEWHEEL:
          blocks.scrolled(event.y)
    
    # USEREVENTS
    if event.type == TO_GAME:
      state.set_state("game")
      state.set_substate("play")
      buttons.toggleVis(PLAY_BUTTON)
      buttons.toggleVis(FAST_BACKWARD_BUTTON)
      buttons.toggleVis(FAST_FORWARD_BUTTON)
      editor_sliders.set_invisible()
    
    elif event.type == TO_EDITOR:
      state.set_state("editor")
      state.set_substate("paused")
      buttons.toggleVis(PLAY_BUTTON)
      buttons.toggleVis(FAST_BACKWARD_BUTTON)
      buttons.toggleVis(FAST_FORWARD_BUTTON)
      editor_sliders.set_visible()
      
    elif event.type == EDITOR_PLAY:
      if state.get_substate() == "paused":
        state.set_substate("play")
        buttons.changeAttr(PLAY_BUTTON, "image", PAUSE_IMAGE)
      else:
        state.set_substate("paused")
        buttons.changeAttr(PLAY_BUTTON, "image", PLAY_IMAGE)
    
    elif event.type == FAST_BACKWARD:
      blocks.fast_forward(-10)
    
    elif event.type == FAST_FORWARD:
      blocks.fast_forward(10)

# == # == # == # == # == #

def process_game(player, blocks, state, pen, editor_sliders):
  if state.get_state() == "game":
    if state.get_substate() == "game over":
      pass
    elif state.get_substate() == "paused":
      pass
    elif state.get_substate() == "play":
      blocks.move()
      player.update()
      if player.collide(blocks.get_rects()):
        state.set_substate("game over")
      blocks.cull(HEIGHT)

  if state.get_state() == "editor":
    slider = editor_sliders.get(BLOCK_WIDTH_SLIDER)
    if slider != None:
      pen.set_width(slider.current)
    slider = editor_sliders.get(BLOCK_HEIGHT_SLIDER)
    if slider != None:
      pen.set_height(slider.current)
    slider = editor_sliders.get(BLOCK_SPEED_SLIDER)
    if slider != None:
      pen.set_speed(slider.current)
      
    if state.get_substate() == "play":
      blocks.move()
      player.update()

# == # == # == # == # == #

def draw(WIN, player, blocks, state, pen, mouse, buttons, editor_sliders):
  WIN.fill(BLACK)
  if state.get_state() == "game":
    
    pygame.draw.rect(WIN, GREY, pygame.Rect(PLAYER_BOUNDS["left"], PLAYER_BOUNDS["top"], SIZE*4, SIZE*4), 1)
    
    player.draw(WIN)
    blocks.draw(WIN)
    if state.get_substate() == "game over":
      text = GAMEOVER_FONT.render("Game Over", 1, WHITE, BLACK)
      WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/3))
    
  if state.get_state() == "editor":
    blocks.draw(WIN)
    buttons.draw(WIN)
    
    if state.get_substate() == "play":
      player.draw(WIN)
    
    if state.get_substate() == "paused":
      pen.draw_grid(WIN)
      pen.preview(mouse, WIN)
      
      for i in range(0, 5):
        pygame.draw.line(WIN, WHITE, (PLAYER_BOUNDS["left"] + SIZE*i, 0), (PLAYER_BOUNDS["left"] + SIZE*i, HEIGHT), 3)
      
      for i in range(0, 5):
        pygame.draw.line(WIN, WHITE, (PLAYER_BOUNDS["left"], PLAYER_BOUNDS["top"] + SIZE*i), (PLAYER_BOUNDS["right"], PLAYER_BOUNDS["top"] + SIZE*i), 3)
  
  editor_sliders.draw(WIN)
  pygame.display.update()

# == # == # == # == # == #

def main():
  clock = pygame.time.Clock()
  
  # remove unnecessary events from event list
  pygame.event.set_blocked(None)
  pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL])
  pygame.event.set_allowed(USEREVENTS)
  
  from components.state import State
  #from components.textures import TextureAtlas
  from components.player import Player
  from components.blocks import Block, Blocks
  from components.drawer import Drawer
  from components.button import Buttons
  from components.slider import Slider, Sliders
  
  # GAME VARIABLES
  state = State("game")
  state.set_substate("play")
  player_surface = pygame.Surface((SIZE, SIZE))
  player_surface.fill(WHITE)
  player = Player(PLAYER_BOUNDS["left"], PLAYER_BOUNDS["top"], player_surface, PLAYER_BOUNDS)
  
  pen = Drawer(SIZE, SIZE, WHITE, 3, 0.7, 10, PLAYER_BOUNDS)
  
  buttons = Buttons()
  
  buttons.create(PLAY_BUTTON, BLACK, EDITOR_PLAY, 1, GREY, False, image = PLAY_IMAGE)
  buttons.create(FAST_FORWARD_BUTTON, BLACK, FAST_FORWARD, 1, GREY, False, image = FAST_FORWARD_IMAGE)
  buttons.create(FAST_BACKWARD_BUTTON, BLACK, FAST_BACKWARD, 1, GREY, False, image = FAST_BACKWARD_IMAGE)
  
  temp_blocks = [
    Block(PLAYER_BOUNDS["left"] + SIZE*i2, -i*3*SIZE, SIZE, SIZE, WHITE, 3, 0.7) for i in range(10) for i2 in range(2)
  ]
  
  blocks = Blocks(*temp_blocks)
  #blocks.toggle_see_collision_box()
  
  block_width = Slider(5, 100, SIZE, 5, BLOCK_WIDTH_SLIDER, top_bar = True, name = "block width:", font = SLIDER_FONT, value_display=True)
  block_height = Slider(5, 100, SIZE, 5, BLOCK_HEIGHT_SLIDER, top_bar = True, name = "block height:", font = SLIDER_FONT, value_display=True)
  block_speed = Slider(1, 10, 3, 1, BLOCK_SPEED_SLIDER, top_bar = True, name = "block speed:", font = SLIDER_FONT, value_display=True)
  editor_sliders = Sliders(block_width, block_height, block_speed)
  editor_sliders.set_invisible()
  
  #texture_atlas = TextureAtlas(PATH_TO_ATLAS_IMAGE)
  
  # DEBUG MODE
  debug_mode = True
  
  #initiates game loop
  run = 1
  while run:
    
    #ticks the clock
    clock.tick(FPS)

    mouse = pygame.mouse.get_pos()
    
    #for everything that the user has inputted ...
    handle_events(player, mouse, state, blocks, pen, buttons, editor_sliders)
    
    process_game(player, blocks, state, pen, editor_sliders)
    
    draw(WIN, player, blocks, state, pen, mouse, buttons, editor_sliders)
    

    print(len(blocks))
    

# == # == # == # == # == #

main()