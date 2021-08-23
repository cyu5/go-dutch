# Group class

class Group:

    # constructor
    def __init__(self, members=None) -> None:
        self.members = set()
        # add members to self.members set
        if members is not None:
            if not isinstance(members, str):
                for member in members:
                    # input validation
                    if not isinstance(member, str):
                        raise TypeError(f'{member} is not a str')
                    else:
                        self.members.add(member)
            else:
                raise TypeError('input should be an iterable, not a string')
            

        self.ledger = list()
        self.balances = dict()

        
        
    