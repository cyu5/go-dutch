from collections import defaultdict

# Group class
class Group:

    # constructor
    def __init__(self, members=None) -> None:
        self.members = set()
        if members is not None:
            # add members to group
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
        self.balances = defaultdict(int)

    def extend_members(self, new_members) -> None:
        if not isinstance(new_members, str):
            tmp = set()
            for member in new_members:

                # input validation
                if not isinstance(member, str):
                    raise TypeError(f'{member} is not a str')
                else:
                    tmp.add(member)
            self.members.update(tmp)
        else:
            raise TypeError('input should be an iterable, not a string')
            
        
    # add a single member to the group
    def add_member (self, member: str) -> None:

        if isinstance(member, str):
            self.members.add(member)
        else:
            raise TypeError('Single string argument required for input')
    
