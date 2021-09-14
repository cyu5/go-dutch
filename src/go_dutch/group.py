# Group class
import collections
from typing import Iterator, List


class Group(collections.abc.Collection):

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
        return self.__ledger.copy()

    def get_balances (self) -> dict:
        return self.__balances.copy()

    # remove a single member from the group only if the member is settled
    def remove_settled_member (self, member: str) -> None:
        if member not in self.__balances:
            raise KeyError(f"{member} is not part of group {self}")
        if self.__balances[member] != 0:
            raise ValueError(f"{member} is not settled")
        del self.__balances[member]

    # clears all information from group
    def clear (self) -> None:
        self.__balances.clear()
        self.__ledger.clear()
    
    def add_transaction(self, payer: str, payees: List[str], amount: float, weights: List[int]=None):
        if payer not in self.__balances:
            raise ValueError(f"{payer} is not in group")
        for payee in payees:
            if payee not in self.__balances:
                raise ValueError(f"{payee} is not in group")
        if amount <= 0:
            raise ValueError(f"{amount} has to be greater than 0")

        if weights is None:
            self.__balances[payer] += amount
            split_amount = amount/len(payees)
            for payee in payees:
                self.__balances[payee] -= split_amount
        else:
            if len(weights) != len(payees):
                raise ValueError("payees and weights have different lengths")
            if any(w <= 0 for w in weights):
                raise ValueError("all weights have to be greater than 0")
            self.__balances[payer] += amount
            quantum = amount / sum(weights)
            for payee, weight in zip(payees, weights):
                self.__balances[payee] -= weight * quantum

        Transaction = collections.namedtuple("Transaction", "payer payees amount weights")
        transaction = Transaction(payer, payees, amount, weights)
        self.__ledger.append(transaction)

    def __len__(self) -> int:
        return self.__balances.__len__()
    
    def __iter__(self) -> Iterator:
        return self.__balances.__iter__()

    def __contains__(self, member: str) -> bool:
        return self.__balances.__contains__(member)



