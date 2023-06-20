from pygame import Rect
from pygame.draw import rect as draw_rect
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
    
    collision_rect_left = int(self.left + self.width*((1-collision_rect_percentage)/2))
    collision_rect_top = int(self.top + self.height*((1-collision_rect_percentage)/2))
    collision_rect_width = int(self.width * collision_rect_percentage)
    collision_rect_height = int(self.height * collision_rect_percentage)
    
    self.collision_rect =Rect(collision_rect_left,
                              collision_rect_top,
                              collision_rect_width,
                              collision_rect_height)
    
    print(self.collision_rect)
  
  def draw(self, WIN, see_collision_box):
    draw_rect(WIN, self.colour, self)
    if see_collision_box == True:
      draw_rect(WIN, (255, 255, 0), self.collision_rect, 1)

  
  def move_generic(self, x_direction, y_direction):
    self.x += x_direction
    self.y += y_direction
    self.collision_rect.x += x_direction
    self.collision_rect.y += y_direction
  
  def move(self):
    self.move_generic(0, self.speed)

class Blocks(MutableSequence):
  def __init__(self):
    self.blocks = []
    self.see_collision_box = False
  
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

  def toggle_see_collision_box(self):
    self.see_collision_box = not self.see_collision_box
  
  def draw(self, WIN):
    for block in self.blocks:
      block.draw(WIN, self.see_collision_box)
      
  def move(self):
    for block in self.blocks:
      block.move()
  
  def create(self, left, top, width, height, colour, speed, collision_rect_percentage:float):
    new_block = Block(left, top, width, height, colour, speed, collision_rect_percentage, self)
