from pygame import Rect, Surface, draw

class Sliders:
  def __init__(self, *sliders):
    self.sliders = sliders
    
  def draw(self, window):
    for slider in self.sliders:
      slider.draw(window)
    
  def update(self, mouse):
    """call if mouse clicked"""
    for slider in self.sliders:
      slider.update(mouse)

class Slider:
  def __init__(self, min:int, max:int, step:float, rect:Rect, show_buttons = True, draggable_slider = True):
    """rect is the size and place where all the components of the slider will go"""
    self.min = min
    self.max = max
    self.range = max-min
    self.step = step
    
    self.show_buttons = show_buttons
    self.draggable_slider = draggable_slider
    
    self.rect = rect
    self.surface = Surface((self.rect.width, self.rect.height))
    self.surface.fill((0, 0, 0))
    
    self.current = self.min
    
    # slider buttons
    self.buttons_size = self.rect.height
    self.button_right = Surface((self.buttons_size, self.buttons_size))
    self.button_left = Surface((self.buttons_size, self.buttons_size))
    
    self.button_right_rect = self.button_right.get_rect()
    self.button_right_rect.x = self.rect.x + self.surface.get_width() - self.buttons_size
    self.button_right_rect.y = self.rect.y
    
    self.button_left_rect = self.button_left.get_rect()
    self.button_left_rect.x = self.rect.x
    self.button_left_rect.y = self.rect.y
    
    draw.line(self.button_right, (255, 255, 255), (self.buttons_size//2, 0), (self.buttons_size//2, self.buttons_size), 3)
    draw.line(self.button_right, (255, 255, 255), (0, self.buttons_size//2), (self.buttons_size, self.buttons_size//2), 3)
    draw.line(self.button_left, (255, 255, 255), (0, self.buttons_size//2), (self.buttons_size, self.buttons_size//2), 3)

  def increment(self):
    self.current += self.step
    self.current = min(self.current, self.max)
  
  def decrement(self):
    self.current -= self.step
    self.current = max(self.current, self.min)
  
  def draw(self, window):
    self.surface.fill((0, 0, 0))
    x = self.rect.x
    y = self.rect.y
    
    # draw slider buttons
    self.surface.blit(self.button_left, (0, 0))
    self.surface.blit(self.button_right, (self.surface.get_width() - self.buttons_size, 0))
    
    # draw slider line
    start_x = self.buttons_size*3//2
    end_x = self.surface.get_width() - (self.buttons_size*3//2)
    draw.line(self.surface, (111, 111, 111), (start_x, self.buttons_size//2), (end_x, self.buttons_size//2), 3)
    
    # draw slider dot
    x_offset = round(((self.current - self.min) / self.range) * (end_x - start_x))
    draw.circle(self.surface, (255, 255, 255), (start_x + x_offset, self.buttons_size//2 + 1), 4, 1)
    
    # draw slider to window
    window.blit(self.surface, (x, y))
  
  def update(self, mouse):
    if self.button_right_rect.collidepoint(mouse):
      self.increment()
    elif self.button_left_rect.collidepoint(mouse):
      self.decrement()