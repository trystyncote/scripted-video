class File:  # *
  def __init__(self, name: str):
    '''
    The class 'File' interacts with a file. It can either read a file, or write over it.
    '''
    self.name = name  # `self.name` is the name of the file that's being used.

  def read(self):
    '''
    Takes the file and reads its contents. It then returns the file's contents.
    '''
    # !!! does not currently work with img files; allow for more rotund programming later.
    ''' with Statement: Reads the file and inputs it to `file_read`. '''
    with open(self.name, "r") as file_read:
      file_read = file_read.readlines()  # Reads the contents of the file.

    return file_read
  
  # This is where a 'write' function would go, later. It would be used to change the 'take number'
  # within the header of the script file.