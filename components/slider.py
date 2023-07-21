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
  
  def set_visible(self):
    for slider in self.sliders:
      slider.visible = True
    
  def set_invisible(self):
    for slider in self.sliders:
      slider.visible = False
  
  def toggle_visibility(self):
    for slider in self.sliders:
      slider.visible = not self.visible
  
  def get(self, rect):
    for slider in self.sliders:
      if slider.rect == rect:
        return slider
    return None

class Slider:
  def __init__(self, min:int, max:int, default:int, step:float, rect:Rect, show_buttons = True, draggable_slider = True, top_bar = False, name = "", font = None, value_display = False):
    """rect is the size and place where all the components of the slider will go
    
    top_bar is where name and value display will go"""
    
    if top_bar == False and (name != "" or value_display == False):
      raise ValueError("top_bar not enabled for name and value display")
    
    self.min = min
    self.max = max
    self.default = default
    self.range = max-min
    self.step = step
    
    self.show_buttons = show_buttons
    self.draggable_slider = draggable_slider
    self.name = name
    self.font = font
    self.value_display = value_display
    
    self.rect = rect
    self.surface = Surface((self.rect.width, self.rect.height))
    self.surface.fill((0, 0, 0))
    
    self.current = self.default
    self.visible = True
    
    # slider buttons
    if top_bar == False:
      self.slider_rect = self.rect
      
    else:
      height = self.rect.height // 2
      self.slider_rect = Rect(self.rect.x, self.rect.y + height, self.rect.width, height)
    
    self.slider_surface = Surface((self.slider_rect.width, self.slider_rect.height))
    
    self.buttons_size = self.slider_rect.height
    self.button_right = Surface((self.buttons_size, self.buttons_size))
    self.button_left = Surface((self.buttons_size, self.buttons_size))
    
    self.button_right_rect = self.button_right.get_rect()
    self.button_right_rect.x = self.slider_rect.x + self.slider_surface.get_width() - self.buttons_size
    self.button_right_rect.y = self.slider_rect.y
    
    self.button_left_rect = self.button_left.get_rect()
    self.button_left_rect.x = self.slider_rect.x
    self.button_left_rect.y = self.slider_rect.y
    
    draw.line(self.button_right, (255, 255, 255), (self.buttons_size//2, 0), (self.buttons_size//2, self.buttons_size), 3)
    draw.line(self.button_right, (255, 255, 255), (0, self.buttons_size//2), (self.buttons_size, self.buttons_size//2), 3)
    draw.line(self.button_left, (255, 255, 255), (0, self.buttons_size//2), (self.buttons_size, self.buttons_size//2), 3)

  def set_visible(self):
    self.visible = True
    
  def set_invisible(self):
    self.visible = False
  
  def toggle_visibility(self):
    self.visible = not self.visible

  def increment(self):
    self.current += self.step
    self.current = min(self.current, self.max)
  
  def decrement(self):
    self.current -= self.step
    self.current = max(self.current, self.min)
  
  def draw(self, window):
    if self.visible == True:
      self.surface.fill((0, 0, 0))
      self.slider_surface.fill((0, 0, 0))
      
      # draw other sections
      if self.name != "":
        text = self.font.render(self.name, 1, (255, 255, 255))
        self.surface.blit(text, (0, 0))
      
      if self.value_display == True:
        text = self.font.render(str(self.current), 1, (255, 255, 255))
        self.surface.blit(text, (self.button_right_rect.x - text.get_width(), 0))
      
      # draw slider section
      if self.show_buttons == True:
        # draw slider buttons
        self.slider_surface.blit(self.button_left, (0, 0))
        self.slider_surface.blit(self.button_right, (self.slider_surface.get_width() - self.buttons_size, 0))
      
      # draw slider line
      start_x = self.buttons_size*3//2
      end_x = self.slider_surface.get_width() - (self.buttons_size*3//2)
      draw.line(self.slider_surface, (111, 111, 111), (start_x, self.buttons_size//2), (end_x, self.buttons_size//2), 3)
      
      # draw slider dot
      x_offset = round(((self.current - self.min) / self.range) * (end_x - start_x))
      draw.circle(self.slider_surface, (255, 255, 255), (start_x + x_offset, self.buttons_size//2 + 1), 4, 1)
      
      self.surface.blit(self.slider_surface, (0, self.surface.get_height()//2))
      
      # draw slider to window
      window.blit(self.surface, (self.rect.x, self.rect.y))
  
  def update(self, mouse):
    pos = mouse.get_pos()
    if mouse.get_pressed()[0]:
      if self.button_right_rect.collidepoint(pos):
        self.increment()
      elif self.button_left_rect.collidepoint(pos):
        self.decrement()
    
  def get_value(self):
    return self.current