from pygame import Rect
from pygame.draw import rect
from collections.abc import MutableSequence

class Block(Rect):
  def __init__(self, left, top, width, height, colour, speed, collision_rect_percentage:float, blocks_group):
    super().__init__(left, top, width, height)
    self.colour = colour
    self.set_collision_rect_precentage(collision_rect_percentage)
    self.speed = speed
    blocks_group.add(self)
  
  def set_collision_rect_precentage(self, collision_rect_percentage:float):
    
    if 0 <= collision_rect_percentage <= 1:
      pass
    else:
      raise ValueError("Collision rect percentage not between 0 and 1")
    
    self.collision_rect =Rect(self.left + self.width*(collision_rect_percentage/2),
                              self.top + self.height*(collision_rect_percentage/2),
                              self.width * collision_rect_percentage,
                              self.height * collision_rect_percentage)
  
  def draw(self, WIN):
    rect(WIN, self.colour, self)
  
  def move(self, x_direction, y_direction):
    self.x += x_direction
    self.y += y_direction
  

class Blocks(MutableSequence):
  def __init__(self):
    self.blocks = []
  
  # def __call__(self):
  #   return self.blocks

  def __getitem__(self, i):
    return self.blocks[i]
  
  def __len__(self):
    return len(self.blocks)
  
  def __setitem__(self, index, value):
    self.blocks[index] = value
    
  def __delitem__(self, key):
    self.blocks.remove(key)
    
  def insert(self, index, object):
    self.blocks.insert(index, object)

  def add(self, block:Block):
    self.blocks.append(block)
  
  def remove(self, block:Block):
    self.blocks.remove(block)
  
  def draw(self, WIN):
    for block in self.blocks:
      block.draw(WIN)