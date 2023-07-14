from pygame import Surface, draw

class Drawer:
  def __init__(self, width, height, colour, speed, collision_rect_decimal, grid_size, bounds):
    self.width = width
    self.height = height
    self.colour = colour
    self.speed = speed
    self.collision_rect_decimal = collision_rect_decimal
    
    self.grid_size = grid_size
    self.view_grid = True
    self.snap_grid = True
    
    self.type = "erase" # out of ["draw", "erase"]
    
    self.bounds = bounds
    top = self.bounds["top"]
    times = 0
    while top > 0:
      top -= self.grid_size
      times += 1
    self.vertical_offset = top
    
    left = self.bounds["left"]
    times = 0
    while left > 0:
      left -= self.grid_size
      times += 1
    self.horizontal_offset = left
    print(left)
  
  def snap_to(self, mouse):
    # find where the 3 difference comes from (for accurate scaling)
    x = self.grid_size * round((mouse[0]-3)/self.grid_size) + self.horizontal_offset
    y = self.grid_size * round(mouse[1]/self.grid_size) + self.vertical_offset
    
    return (x, y)
    
  def draw(self, blocks, mouse):
    if self.type == "draw":
      if self.snap_grid == False:
        blocks.create(mouse[0], mouse[1], self.width, self.height, self.colour, self.speed, self.collision_rect_decimal)
      else:
        snap = self.snap_to(mouse)
        blocks.create(snap[0], snap[1], self.width, self.height, self.colour, self.speed, self.collision_rect_decimal)
    elif self.type == "erase":
      self.erase(blocks, mouse)
  
  def erase(self, blocks, mouse):
    blocks.sort(key = lambda rect: rect.bottom, reverse = True)
    i = 0
    while blocks[i].bottom >= 0:
      if blocks[i].collidepoint(mouse):
        blocks.pop(i)
        return True
      i += 1
      if i >= len(blocks):
        return False
    return False
  
  def preview(self, mouse, window):
    preview = Surface((self.width, self.height))
    preview.fill(self.colour)
    preview.set_alpha(150)
    if self.snap_grid == False:
      window.blit(preview, mouse)
    else:
      window.blit(preview, self.snap_to(mouse))
  
  def draw_grid(self, window):
    """only draws the grid if view_grid is true"""
    if self.view_grid == True:
      left = self.bounds["left"]
      right = self.bounds["right"]
      total_width = int(right - left)
      
      for i in range(0, total_width, self.grid_size):
        draw.line(window, (255, 255, 255), (left + i, 0), (left + i, window.get_height()))
      for i in range(self.vertical_offset, window.get_height(), self.grid_size):
        draw.line(window, (255, 255, 255), (left, i), (right, i))
      
  
  def toggle_grid_view(self):
    self.view_grid = not self.view_grid
  
  def toggle_snap_grid(self):
    self.snap_grid = not self.snap_grid
