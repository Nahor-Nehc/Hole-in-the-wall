from collections.abc import MutableSequence

class Loader:
  def __init__(self):
    pass
  
  def load_level(self, path_to_levels_folder, level_name):
    from shelve import open as open_shelf
    level_loader = open_shelf(path_to_levels_folder)
    blocks = level_loader[level_name]
    
    level_loader.close()
    return blocks
    
  def save_level(self, path_to_levels_file, level_name, blocks):
    from shelve import open as open_shelf
    level_loader = open_shelf(path_to_levels_file)
    
    try:
      _ = level_loader[level_name]
      from pyautogui import confirm # type:ignore
      check = confirm(text='WARNING: There is already a file saved here. Do you want to replace it?', title='WARNING: OVERWRITE ERROR', buttons=['Yes', 'No'])
      if check == "Yes":
        level_loader[level_name] = blocks
      elif check == "No":
        pass
        
    except KeyError:
      level_loader[level_name] = blocks

    level_loader.close()