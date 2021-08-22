# Group class

class Group:

  # constructor
  def __init__(self, members=set()) -> None:
    
    self.members = members
    self.ledger = list()
    self.balances = dict()

    # validation
    