"""
A class to provide a circular list structure that maintains its length as elements are added to it.
"""
class CircularList(list):

  def __init__(self, data, maxlen=0):
    assert isinstance(data, list), "Invalid data. It must be a list."

    # zero-pad or trim data from the left to fit to maximum length
    maxlen = len(data) if(maxlen == 0) else maxlen
    delta = maxlen - len(data)
    if(delta > 0):
      data = [0]*delta + data # prepend zeros
    else:
      data[:-maxlen] = []     # trim the leftmost portion

    # initialize the parent list constructor with the data
    super().__init__(data)

  def add(self, data):
    assert isinstance(data, (float,int,list)), "Must be number or list."

    # convert to iterable (list) if just a single number
    data = data if isinstance(data, list) else [data]

    # shift the array if the shift is less than array length
    shift = len(data)
    maxlen = len(self)
    if(shift < maxlen):
      self[:-shift] = self[shift:] # shift the existing data left
      self[-shift:] = data         # append the new data to the end
    else:
      self[:] = data[-maxlen:]     # only copy the rightmost portion

  def clear(self):
    self.add([0]*len(self))
