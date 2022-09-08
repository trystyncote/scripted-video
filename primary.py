from script_manager import Scripter

def primary():
  # !!! this is TEMPORARY, so I can determine if the script is being edited correctly.
  x = Scripter("sample_script.txt")
  
  y1 = x.polishHeader()
  y2 = x.polishBody()
  
  print(y1)
  print(y2)

primary()
