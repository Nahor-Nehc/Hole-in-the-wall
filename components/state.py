
class State:
  def __init__(self, initial_state):
    self.state = initial_state
    
    self.substates = {
      "start":[],
      "menu":["level select"],
      "game":["paused", "game over"],
      "editor":[],
    }
    
    self.substate = None
  
  def set_state(self, state):
    self.state = state
    self.substate = None
    
  def get_state(self):
    return self.state
  
  def set_substate(self, substate):
    if substate in self.substates[self.state]:
      self.substate = substate
    
  def get_substate(self):
    return self.substate
  
  def get_possible_substates(self):
    return self.substates[self.state]