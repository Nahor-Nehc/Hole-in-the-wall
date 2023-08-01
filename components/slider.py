from pygame import Rect, Surface, draw

class Sliders:
  def __init__(self, *sliders):
    self.sliders = sliders
    
  def draw(self, window):
    for slider in self.sliders:
      slider.draw(window)
    
  def update(self, mouse):
    """call if mouse clicked"""
    drag_available = not self.check_dragging()
    for slider in self.sliders:
      slider.update(mouse, drag_available)
  
  def set_visible(self):
    for slider in self.sliders:
      slider.visible = True
    
  def set_invisible(self):
    for slider in self.sliders:
      slider.visible = False
  
  def toggle_visibility(self):
    for slider in self.sliders:
      slider.visible = not self.visible
  
  def check_dragging(self):
    if sum([1 for slider in self.sliders if slider.dragging == True]) >= 1:
      return True
    else:
      return False
  
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
    
    if top_bar == False:
      self.slider_rect = self.rect
      
    else:
      height = self.rect.height // 2
      self.slider_rect = Rect(self.rect.x, self.rect.y + height, self.rect.width, height)
    
    self.slider_surface = Surface((self.slider_rect.width, self.slider_rect.height))
    
    # slider buttons
    # general dimensions
    self.buttons_size = self.slider_rect.height
    self.button_right = Surface((self.buttons_size, self.buttons_size))
    self.button_left = Surface((self.buttons_size, self.buttons_size))
    
    # right side
    self.button_right_rect = self.button_right.get_rect()
    self.button_right_rect.x = self.slider_rect.x + self.slider_surface.get_width() - self.buttons_size
    self.button_right_rect.y = self.slider_rect.y
    
    # left side
    self.button_left_rect = self.button_left.get_rect()
    self.button_left_rect.x = self.slider_rect.x
    self.button_left_rect.y = self.slider_rect.y
    
    self.slider_bar_start_x = self.buttons_size*3//2
    self.slider_bar_end_x = self.slider_surface.get_width() - (self.buttons_size*3//2)
    self.set_slider_dot_pos()
    
    draw.line(self.button_right, (255, 255, 255), (self.buttons_size//2, 0), (self.buttons_size//2, self.buttons_size), 3)
    draw.line(self.button_right, (255, 255, 255), (0, self.buttons_size//2), (self.buttons_size, self.buttons_size//2), 3)
    draw.line(self.button_left, (255, 255, 255), (0, self.buttons_size//2), (self.buttons_size, self.buttons_size//2), 3)
    
    # controls draggables
    self.dragging = False

  def set_slider_dot_pos(self):
    x_offset = round(
      ((self.current - self.min) / self.range) * 
      (self.slider_bar_end_x - self.slider_bar_start_x)
    )
    
    self.slider_dot_rect = draw.circle(
      self.slider_surface,
      (255, 255, 255),
      (
        self.slider_bar_start_x + x_offset,
        self.buttons_size//2 + 1
        ),
      4,
      1)
    self.calculate_absolute_dot_rect()

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
      self.slider_dot_rect = draw.circle(self.slider_surface, (255, 255, 255), (start_x + x_offset, self.buttons_size//2 + 1), 4, 1)
      self.calculate_absolute_dot_rect()
      
      self.surface.blit(self.slider_surface, (0, self.surface.get_height()//2))
      
      # draw slider to window
      window.blit(self.surface, (self.rect.x, self.rect.y))
      
  def calculate_absolute_dot_rect(self):
    self.absolute_slider_dot_rect = self.slider_dot_rect
    self.absolute_slider_dot_rect.x = self.slider_dot_rect.x + self.slider_rect.x
    self.absolute_slider_dot_rect.y = self.slider_dot_rect.y + self.slider_rect.y
    
  
  def update(self, mouse, drag_available):
    pos = mouse.get_pos()
    if mouse.get_pressed()[0]:
      if self.button_right_rect.collidepoint(pos):
        self.increment()
      elif self.button_left_rect.collidepoint(pos):
        self.decrement()
        
      if self.absolute_slider_dot_rect.collidepoint(pos) and drag_available == True:
        self.dragging = True
    
    else:
      self.dragging = False

    if self.dragging == True:
      start_pos =self.slider_bar_start_x + self.rect.x
      end_pos = self.slider_bar_end_x + self.rect.x
      a = pos[0] - start_pos
      b = end_pos - pos[0]
      percentage = a/(end_pos - start_pos)
      if percentage < 0:
        percentage = 0
      if percentage > 1:
        percentage = 1
      self.current = round(percentage*self.range) + self.min
      self.set_slider_dot_pos()
      print(percentage, self.current, a, b, start_pos, end_pos)
    
  def get_value(self):
    return self.current