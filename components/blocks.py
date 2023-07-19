from pygame import Rect
from pygame.draw import rect as draw_rect
from collections.abc import MutableSequence

class Block(Rect):
  def __init__(self, left, top, width, height, colour, speed, collision_rect_decimal:float, blocks_group=None):
    super().__init__(left, top, width, height)
    self.colour = colour
    self.set_collision_rect_precentage(collision_rect_decimal)
    self.speed = speed
    if blocks_group != None:
      blocks_group.add(self)
  
  def set_collision_rect_precentage(self, collision_rect_decimal:float):
    
    if 0 <= collision_rect_decimal <= 1:
      pass
    else:
      raise ValueError("Collision rect decimal not between 0 and 1")
    
    collision_rect_left = int(self.left + self.width*((1-collision_rect_decimal)/2))
    collision_rect_top = int(self.top + self.height*((1-collision_rect_decimal)/2))
    collision_rect_width = int(self.width * collision_rect_decimal)
    collision_rect_height = int(self.height * collision_rect_decimal)
    
    self.collision_rect =Rect(
      collision_rect_left,
      collision_rect_top,
      collision_rect_width,
      collision_rect_height
      )
  
  def draw(self, WIN, see_collision_box):
    draw_rect(WIN, self.colour, self)
    if see_collision_box == True:
      draw_rect(WIN, (255, 0, 255), self.collision_rect, 1)
  
  def move_generic(self, x_direction, y_direction):
    self.x += x_direction
    self.y += y_direction
    self.collision_rect.x += x_direction
    self.collision_rect.y += y_direction
  
  def move(self):
    self.move_generic(0, self.speed)
  
  def get_initial_rect(self, times):
    newtop = self.top - times*self.speed
    return Block(self.left, newtop, self.width, self.height, self.colour, self.speed, self.collision_rect)

class Blocks(MutableSequence):
  def __init__(self, *blocks):
    self.blocks = list(blocks)
    self.see_collision_box = False
    self.sort()
    self.times = 0
  
  def sort(self):
    self.blocks.sort(key = lambda block: block.bottom, reverse=True)

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
    self.sort()

  def add(self, block:Block):
    self.blocks.append(block)
    self.sort()
  
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
    
    self.times += 1
  
  def get_start_position_blocks(self):
    starting_blocks = Blocks()
    for block in self.blocks:
      starting_blocks.add(block.get_initial_rect(self.times))
    
    return starting_blocks
  
  def fast_forward(self, increment):
    self.times += increment
    for block in self.blocks:
      block.move_generic(0, increment * block.speed)
  
  def create(self, left, top, width, height, colour, speed, collision_rect_decimal:float):
    new_block = Block(left, top, width, height, colour, speed, collision_rect_decimal, self)
    self.append(new_block)
    self.sort()
  
  def get_rects(self):
    return [block.collision_rect for block in self.blocks]

  def cull(self, height):
    remove = []
    for block in self.blocks:
      if block.y > height:
        remove.append(block)
    
    for item in remove:
      self.blocks.remove(item)    
  
  def scrolled(self, y):
    self.fast_forward(y)