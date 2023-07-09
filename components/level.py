from collections.abc import MutableSequence

class Level(MutableSequence):
  def __init__(self):
    self.blocks = []

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


class Loader:
  def __init__(self):
    pass
  
  def load_level(self, path_to_levels_folder, level_name):
    from shelve import open as open_shelf
    level_loader = open_shelf(path_to_levels_folder)
    level = level_loader[level_name]
    
    #
    
    level_loader.close()
    
  def save_level(self, path_to_levels_folder, level_name):
    from shelve import open as open_shelf
    level_loader = open_shelf(path_to_levels_folder)
    
    try:
      _ = level_loader[level_name]
      from pyautogui import confirm
      check = confirm(text='WARNING: There is already a file saved here. Do you want to replace it?', title='WARNING: OVERWRITE ERROR', buttons=['Yes', 'No'])
      if check == "Yes":
        level_loader[level_name] = "" # <--   get the level
      elif check == "No":
        pass
        
    except KeyError:
      level_loader[level_name] = "" # <--   get the level

    level_loader.close()