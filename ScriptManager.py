class Scripter:
  def __init__(self, script: list):
    '''
    The class 'Scripter' interacts with a script, devised from a .txt file. It can splice the
    header off of the script, if applicable. Or it can polish the script into a readable variable.
    '''
    self.script = script  # 'script' is the list that contains the contents of the .txt
    # file. It is bare-bones, still containing even the '\n' characters.


  def dissector(self, section: int = 0):  # *
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
        if (self.script[har] == "---") or (self.script[har] == "---\n"):  # If this line is the 
        # separator...
          break  # leave the while loop.
      except:
        # This sequence will forcefully crash the program if it does not have a header.
        har = int("CRASH")

      har += 1  # if not, increase the counter and go back to the start.

    ''' for Loop: Adds every line of the header to `split`. ''' 
    for iar in range(har):  # For every line in the header...
      split[0].append(self.script[iar])  # add to `split[0]`.
    
    ''' for Loop: Adds every line outside of the header to `split`. '''
    for iar in range(len(self.script)-har-1):  # For every line outside of the header...
      split[1].append(self.script[iar+har+1])  # add to `split[1]`.

    return split[section]  # returns both sides separately, to be placed in two different 
    # variables.


  def polishHead(self):
    '''
    Polishes the header of the script into a readable variable. Returns the polished version of the
    header.
    '''
    header_info = self.dissector()
    traits = []

    for iar in range(len(header_info)):
      header_info[iar] = header_info[iar][:-1]
      header_info[iar] = header_info[iar].split(" ")

      while True:
        traits.append(header_info[iar][0])
        header_info[iar].remove(header_info[iar][0]) 
        
        if header_info[iar] == []:
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
    body_info = self.dissector(1)
    
    for iar in range(len(self.script)-1):
      self.script[i] = self.script[iar][:-1]

    return self.script
