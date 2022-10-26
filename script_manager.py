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
    
    ''' for Loop: Clears the '\n' off the end of each line exclusing the last line. '''
    for iar in range(len(self.script)):  # For each line in the self.script variable...
      self.script[iar] = self.script[iar][:-1]  # Cut off the '\n' to that line.


  def polishScript(self):
    '''
    Polishes the body of the script into usable chunks. Returns the polished version of the script.
    '''
    for iar in range(len(self.script)-1):
      self.script[iar] = self.script[iar][:-1]
      
    self.script = split(self.script, "") 
    
    return self.body
