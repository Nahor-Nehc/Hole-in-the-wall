# from pygmtls w edits
from pygame import draw, event, Surface

class Buttons:
  """
  This class holds every button instance created by the create function
  """
  def __init__(self):
    self.buttons = []
    self.visible = []
    self.hidden = []
    
    self.attrs = {
      "rect" : 0,
      "colour" : 1,
      "event" : 2,
      "outlineWidth" : 3,
      "outlineColour" : 4,
      "text" : 5,
      "font" : 6,
      "textColour" : 7,
      "image": 8
    }
    
  def create(self, rect, colour, event, outlineWidth = 0, outlineColour = (0, 0, 0), visible = True, text = "", font = None, textColour = (0, 0, 0), image = None) -> None:
    """
    This function creates a button
    
    :param rect: the rectangle of the button
    :type rect: pygame.Rect
    
    :param colour: the colour of the rectangle
    :type colour: (R, G, B)
    
    :param event: event called by clicking on the button
    :type event: pygame.USEREVENT
    
    :param outlineWidth: the width of the outline
    :type int: integer
    
    :param outlineColour: the colour of the border
    :type outlineColour: (R, G, B)
    """
    temp = [rect, colour, event, outlineWidth, outlineColour, text, font, textColour, image]
    if visible == True:
      self.visible.append(temp)
    else:
      self.hidden.append(temp)
    self.buttons.append(temp)

  def draw(self, window) -> None:
    for button in self.visible:
      
      # draws the rect of the button
      draw.rect(window, button[self.attrs["colour"]], button[self.attrs["rect"]])
      
      # draws the optional border of button
      if button[self.attrs["outlineWidth"]] != 0:
        draw.rect(
          window,
          button[self.attrs["outlineColour"]],
          button[self.attrs["rect"]],
          button[self.attrs["outlineWidth"]]
          )
        
      # draws the text of the button
      if button[self.attrs["font"]] != None:
        # gets the surface containing the text
        txt = button[self.attrs["font"]].render(
          button[self.attrs["text"]],
          1,
          button[self.attrs["textColour"]]
          )
        
        # draws over the button
        window.blit(
          txt,
          (
            button[self.attrs["rect"]].centerx - txt.get_width()/2,
            button[self.attrs["rect"]].centery - txt.get_height()/2
            )
          )
      
      # draws the image of the button over the button
      if button[self.attrs["image"]] != None:
        image = button[self.attrs["image"]]
        window.blit(
          image,
          (
            button[self.attrs["rect"]].centerx - image.get_width()/2,
            button[self.attrs["rect"]].centery - image.get_height()/2
            )
          )
      
  def check(self, mouse) -> None:
    for button in self.visible:
      if button[self.attrs["rect"]].collidepoint(mouse):
        event.post(event.Event(button[self.attrs["event"]]))
        
  def toggleVis(self, rect) -> None:
    edited = False
    for button in self.visible:
      if button[self.attrs["rect"]] == rect:
        self.visible.remove(button)
        self.hidden.append(button)
        edited = True
        
    if edited == False:
      for button in self.hidden:
        if button[self.attrs["rect"]] == rect:
          self.hidden.remove(button)
          self.visible.append(button)
      
  def changeAttr(self, rect, attr, newVal) -> None:
    if attr in self.attrs.keys():
      for button in self.buttons:
        if button[self.attrs["rect"]] == rect:
          button[self.attrs[attr]] = newVal
    else:
      raise ValueError("Attribute does not exist: " + str(attr))
    
  def remove(self, rect) -> None:
    for button in self.buttons:
      if button[self.attrs["rect"]] == rect:
        self.buttons.remove(button)
        try:
          self.hidden.remove(button)
        except:
          self.visible.remove(button)