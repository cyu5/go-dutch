from user import User
from typing import List

class Transaction:
    def __init__(self, payer: User, amount: float, payees: List[User]):
      self.payer = payer
      self.amount = amount
      self.payees = payees
