from FileManager    import File
from ScriptManager  import Scripter

def primary():
  # !!! temp trait; This whole sequence is so I can see if the script is being edited correctly.
  
  x = "game_script_sample.txt"  # A variable that has the name of the file with the example script.
  # This will have a file collecting class in the final ver.
  
  y = File(x).read()
  print(y)
  
  z1, z2 = Scripter(y).dissector()
  Scripter(z2).polishBody()
  print(z1)
  print(z2)
  
  # !!! /temp trait

primary()
