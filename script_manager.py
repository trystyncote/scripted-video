def split(array: list, index):
  new_array = []
  har = 0
  brake = False

  while True:
    try:
      har = array.index(index)
    except:
      har = len(array)
      brake = True

    new_array.append([])
    for i in range(har):
      new_array[-1].append(array[i])
    del array[:har+1]

    if brake == True:
      break

  return(new_array)


class Scripter:
  def __init__(self, file: str):
    '''
    The class 'Scripter' interacts with a script, devised from a .txt file. It can splice the
    header off of the script, if applicable. Or it can polish the script into a readable variable.
    '''
    ''' with Statement: Reads the file and inputs it to `self.script`. '''
    with open(file, "r") as read:
      self.script = read.readlines()
    
    for iar in range(len(self.script)):
      self.script[iar] = self.script[iar][:-1]

    self.script = split(self.script, "---")
    self.header, self.body = self.script[0], self.script[1]


  def polishHead(self):
    '''
    Polishes the header of the script into a readable variable. Returns the polished version of the
    header.
    '''
    traits = []

    for iar in range(len(self.header)):
      self.header[iar] = self.header[iar].split(" ")

      while True:
        traits.append(self.header[iar][0])
        self.header[iar].remove(self.header[iar][0]) 
        
        if self.header[iar] == []:
          break
    
    for iar in range(len(traits)):
      try:
        traits[iar] = int(traits[iar])
      except:
        pass 
    
    # est. sequence of traits: window width, window height, framerate,
    # scene number, take number [edits every time program is run*]
    return tuple(traits)


  def polishBody(self):
    '''
    Polishes the body of the script into usable chunks. Returns the polished version of the script.
    '''
    for iar in range(len(self.body)-1):
      self.body[iar] = self.body[iar][:-1]
      
    self.body = split(self.body, "") 
    
    return self.body
