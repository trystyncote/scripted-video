# !!! may just place this in the __init__() function
def dissector(script: list):  # *
  '''
  Dissects the header of the script, separated by the line '---', off of the rest of the script.
  It then returns the header as output A, and the remainder as output B. It does not polish 
  either part.
  '''
  split = [[], []]  # `split` is a variable to separately handle each side of the script to be 
  # returned.
  har = 0  # `har` acts as an interval counter to define which line acts as the separator; the line
  # '---'. After then, it is used to pinpoint that line for the purposes of the split.
  ''' while Loop: Finds the separator line, "---". '''
  while True:
    try:
      if (script[har] == "---") or (script[har] == "---\n"):  # If this line is the 
      # separator...
        break  # leave the while loop.
    except:
      # This sequence will forcefully crash the program if it does not have a header.
      har = int("CRASH")

    har += 1  # if not, increase the counter and go back to the start.

  ''' for Loop: Adds every line of the header to `split`. ''' 
  for iar in range(har):  # For every line in the header...
    split[0].append(script[iar])  # add to `split[0]`.
  
  ''' for Loop: Adds every line outside of the header to `split`. '''
  for iar in range(len(script)-har-1):  # For every line outside of the header...
    split[1].append(script[iar+har+1])  # add to `split[1]`.

  return split[0], split[1]  # returns both sides separately, to be placed in two different 
  # variables.


class Scripter:
  def __init__(self, file: str):
    '''
    The class 'Scripter' interacts with a script, devised from a .txt file. It can splice the
    header off of the script, if applicable. Or it can polish the script into a readable variable.
    '''
    ''' with Statement: Reads the file and inputs it to `self.script`. '''
    with open(self.file, "r") as read:
      self.script = read.readlines()
    
    self.script = script  # 'script' is the list that contains the contents of the .txt
    # file. It is bare-bones, still containing even the '\n' characters.
    
    self.header, self.body = dissector(self.script)


  def polishHead(self):
    '''
    Polishes the header of the script into a readable variable. Returns the polished version of the
    header.
    '''
    traits = []

    for iar in range(len(self.header)):
      self.header[iar] = self.header[iar][:-1]
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
      self.body[i] = self.body[iar][:-1]
      
    self.body = self.body.split("") 
    
    return self.body
