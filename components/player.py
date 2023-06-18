from pygame import Surface, sprite
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN, Vector2
from math import sqrt

class Movable(sprite.Sprite):
  def move(self, movement:Vector2):
    self.rect.x += movement.x
    self.rect.y += movement.y

class Player(Movable):
  def __init__(self, x, y, image:Surface, speed):
    sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
    self.max_speed = speed
    self.speed = speed
    self.movement = Vector2()
    self.image = image
    self.rect = image.get_rect()
    self.gravity = gravity
    self.jump_momentum = Vector2(0, 0)
  
  def normalise_movement(self, movement):
    if movement.x != 0 and movement.y != 0:
      self.speed = self.max_speed / sqrt(2)
    else:
      self.speed = self.max_speed
    return movement

  def add_speed(self, movement):
    print("added speed")
    movement.x = movement.x * self.speed
    movement.y = movement.y * self.speed
    
    return movement
  
  def check_movement(self, keys_pressed, state) -> Vector2:
    """applies the movement vector to the object, generated from key presses"""
    print("movement checked")
    pressing = keys_pressed
    movement = Vector2(0, 0)
    
    if pressing[K_UP]:
      movement.y -= 1
    if pressing[K_DOWN]:
      movement.y += 1
    if pressing[K_LEFT]:
      movement.x -= 1
    if pressing[K_RIGHT]:
      movement.x += 1
    
    movement = self.normalise_movement(movement)

    return movement
  
  def update(self, keys_pressed, state, tile_space):
    # check horizontal movement
    self.movement = self.add_speed(self.check_movement(keys_pressed, state))

    self.move(self.movement)
    
    
  def draw(self, window:Surface):
    window.blit(self.image, (self.rect.x, self.rect.y))