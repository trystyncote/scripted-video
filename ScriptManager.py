class Scripter:
  def __init__(self, script: list):
    '''
    The class 'Scripter' interacts with a script, devised from a .txt file. It can splice the
    header off of the script, if applicable. Or it can polish the script into a readable variable.
    '''
    self.script = script  # 'script' is the list that contains the contents of the .txt
    # file. It is bare-bones, still containing even the '\n' characters.
  
  def dissector(self):  # *
    '''
    Dissects the header of the script, separated by the line '---', off of the rest of the script.
    It then returns the header as output A, and the remainder as output B. It does not polish 
    either part.
    '''
    split = [[], []]  # `split` is a variable to separately handle each side of the script to be 
    # returned.
    h = 0  # `h` acts as an interval counter to define which line acts as the separator; the line
    # '---'. After then, it is used to pinpoint that line for the purposes of the split.
    ''' while Loop: Finds the separator line, "---". '''
    while True:
      try:
        if (self.script[h] == "---") or (self.script[h] == "---\n"):  # If this line is the 
        # separator...
          break  # leave the while loop.
      except:
        # This sequence will forcefully crash the program if it does not have a header.
        h = int("CRASH")

      h += 1  # if not, increase the counter and go back to the start.

    ''' for Loop: Adds every line of the header to `split`. ''' 
    for i in range(h):  # For every line in the header...
      split[0].append(self.script[i])  # add to `split[0]`.
    
    ''' for Loop: Adds every line outside of the header to `split`. '''
    for i in range(len(self.script)-h-1):  # For every line outside of the header...
      split[1].append(self.script[i+h+1])  # add to `split[1]`.

    return split[0], split[1]  # returns both sides separately, to be placed in two different 
    # variables.

  def polishHead(self):
    '''
    Polishes the header of the script into a readable variable. Returns the polished version of the
    header.
    '''
    pass

  def polishBody(self):
    '''
    Polishes the body of the script into usable chunks. Returns the polished version of the script.
    '''
    for i in range(len(self.script)-1):
      self.script[i] = self.script[i][:-1]

    return self.script
