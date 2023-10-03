# from pygmtls
from pygame import draw, Rect, Surface
from pygame import mouse as py_mouse

class Scroll:
  def __init__(self, x, y, width, height, maxHeight, scrollbarWidth, colour):
    self.buffer = 2
    
    self.currentY = 0
    
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.total = maxHeight
    self.rect = Rect(self.x, self.y, self.width, self.height)
    self.surface = Surface((self.width, self.height))
    self.scrollbarWidth = scrollbarWidth
    self.colour = colour
    
    self.surface.fill(self.colour)
    
    self.scrollClickY = 0
    
    self.scrollBar = [self.width - scrollbarWidth - self.buffer, self.height*(self.currentY/self.total) + self.buffer, scrollbarWidth, (self.height/self.total)*self.height - self.buffer*2]
    self.scrollBarRect = Rect(*self.scrollBar)
    self.down = False
    
    self.items = []
    
  def draw(self, window) -> None:
    window.blit(self.surface, (self.x, self.y))
    draw.rect(self.surface, self.colour, Rect(0, 0, self.width, self.height))
    for item in self.items:
      if item["shape"] == "rect":
        draw.rect(self.surface, item["colour"], Rect(item["x"], item["y"]-self.currentY, item["width"], item["height"]))
        if item["borderWidth"] != None and item["borderColour"] != None:
          draw.rect(self.surface, item["borderColour"], Rect(item["x"], item["y"]-self.currentY, item["width"], item["height"]), item["borderWidth"])
          
      elif item["shape"] == "line":
        draw.aaline(self.surface, item["colour"], (item["start"][0], item["start"][1]-self.currentY), (item["end"][0], item["end"][1]-self.currentY), item["width"])
        
      elif item["shape"] == "circle":
        draw.circle(self.surface, item["colour"], (item["centerx"], item["centery"] - self.currentY), item["radius"])
        if item["borderWidth"] != None and item["borderColour"] != None:
          draw.circle(self.surface, item["borderColour"], (item["centerx"], item["centery"] - self.currentY), item["radius"], item["borderWidth"])
          
      elif item["shape"] == "surface":
        pass
    
    draw.rect(self.surface, (211, 211, 211), self.scrollBarRect)
    
    self.items = []

  def draw_rect(self, rect_name, colour, x, y, width, height, borderWidth=None, borderColour=None) -> None:
    dictionary = {
      "shape" : "rect",
      "name" : rect_name,
      "colour" : colour,
      "x" : x,
      "y" : y,
      "width" : width,
      "height" : height,
      "borderWidth" : borderWidth,
      "borderColour" : borderColour
    }
    self.items.append(dictionary)
    
  def draw_line(self, line_name, colour, start, end, width) -> None:
    dictionary = {
      "shape" : "line",
      "name" : line_name,
      "colour" : colour,
      "start" : start,
      "end" : end,
      "width" : width
    }
    self.items.append(dictionary)
    
  def draw_circle(self, line_name, colour, centerx, centery, radius, borderWidth = None, borderColour = None) -> None:
    dictionary = {
      "shape" : "circle",
      "name" : line_name,
      "colour" : colour,
      "centerx" : centerx,
      "centery" : centery,
      "radius" : radius,
      "borderWidth" : borderWidth,
      "borderColour" : borderColour
    }
    self.items.append(dictionary)

  def blit(self, surface, destination):
    dictionary = {
      "shape" : "surface",
      
    }
    
    self.items.append(dictionary)
  
  def checkMouseDown(self, mouse) -> None:
    rect = Rect(self.scrollBarRect.left + self.x, self.scrollBarRect.top + self.y, self.scrollBarRect.width, self.scrollBarRect.height)
    print(rect, mouse)
    if rect.collidepoint(mouse):
      print("2")
      self.scrollClickY = mouse[1]
      self.down = True
      self.origin = self.scrollBarRect[1]
      
  def checkMouseMotion(self, mouse) -> None:
    if py_mouse.get_pressed()[0] and self.down == True:
      print(4)
      self.currentY = self.origin + mouse[1] - self.scrollClickY
      
      if self.currentY < self.buffer:
        self.currentY = self.buffer
        
      elif self.currentY > self.height - self.scrollBarRect.height - self.buffer:
        self.currentY = self.height - self.scrollBarRect.height - self.buffer
      self.scrollBar[1] = self.currentY
      self.scrollBarRect = Rect(*self.scrollBar)
        
  def checkMouseUp(self, mouse) -> None:
    self.scrollClickY = 0
    self.down = False

  def checkScroll(self, event, sensitivity=5) -> None:
    
    self.currentY -= sensitivity*event.y
    if self.currentY < self.buffer:
      self.currentY = self.buffer

    elif self.currentY > self.height - self.scrollBarRect.height - self.buffer:
      self.currentY = self.height - self.scrollBarRect.height - self.buffer
      
    self.scrollBar[1] = self.currentY
    self.scrollBarRect = Rect(*self.scrollBar)

  def extend_surface(self, x_increase, y_increase):
    items = self.items
    currentY = self.currentY
    self.__init__(self.x, self.y, self.width + x_increase, self.height, self.total + y_increase, self.scrollbarWidth, self.colour)
    self.items = items
    self.currentY = currentY