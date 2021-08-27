from collections import defaultdict

# Group class
class Group():

    # constructor
    def __init__(self, members=None) -> None:
        self.__balances = dict()
        if members is not None:
            # add members to group
            if not isinstance(members, str):
                for member in members:

                    # input validation
                    if not isinstance(member, str):
                        raise TypeError(f'{member} is not a str')
                    else:
                        self.__balances[member] = 0
            else:
                raise TypeError('input should be an iterable, not a string')
            
        self.__ledger = list()

    def extend_members(self, new_members) -> None:
        if not isinstance(new_members, str):
            tmp = dict()
            for member in new_members:

                # input validation
                if not isinstance(member, str):
                    raise TypeError(f'{member} is not a str')
                elif member not in self.__balances:
                    tmp[member] = 0
            self.__balances.update(tmp)
        else:
            raise TypeError('input should be an iterable, not a string')
            
        
    # add a single member to the group
    def add_member (self, member: str) -> None:

        if isinstance(member, str):
            self.__balances.setdefault(member, 0)
        else:
            raise TypeError('Single string argument required for input')
    
    def get_members (self) -> list:
        return list(self.__balances.keys())

    def get_balance (self, member: str) -> int:
        try:
            return self.__balances[member]
        except KeyError:
            raise KeyError(f"{member} is not part of group {self}")

    def has_member (self, member: str) -> int:
        return member in self.__balances

    def get_ledger(self) -> list:
        return self.__ledger

    def get_balances (self) -> dict:
        return self.__balances