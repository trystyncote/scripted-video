from FileManager    import File
from ScriptManager  import Scripter

def primary():
  # !!! temp trait!
  x = "game_script_sample.txt" # Will be inputted manually in final ver.
  
  address = "address.txt"
  classA = File(x)

  y = classA.read()
  classB = Scripter(y)

  print(y)
  for i in range(2):
    print("")

  z1, z2 = classB.dissector()
  Scripter(z2).polishBody()
  pass

primary()