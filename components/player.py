from pygame import Surface, sprite
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN, Vector2

class Player:
  def __init__(self, x, y, image:Surface):
    sprite.Sprite.__init__(self)
    self.movement = Vector2()
    self.image = image
    self.rect = image.get_rect()
    self.rect.x = x
    self.rect.y = y
  
  def move(self, x_direction, y_direction):
    self.rect.x += x_direction
    self.rect.y += y_direction
    
  def draw(self, window:Surface):
    window.blit(self.image, (self.rect.x, self.rect.y))