from script_manager import Scripter

def primary():
  # !!! this is TEMPORARY, so I can determine if the script is being edited correctly.
  x = Scripter("sample_script.txt")
  
  y = x.polishScript()
  
  print(y)

primary()
