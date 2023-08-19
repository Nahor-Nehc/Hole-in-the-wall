from pygame import display

class Loader:
  def __init__(self, total_steps, font):
    self.total_steps = total_steps
    self.current = 0
    self.font = font
  
  def draw(self, window):
    window.fill((0, 0, 0))
    string = str(self.current+1) + "/" + str(self.total_steps)
    text = self.font.render(string, 1, (255, 255, 255))
    window.blit(text, (0, 0))
    
    display.update()
  
  def next_step(self, window, increment = 1):
    self.current += increment
    self.draw(window)