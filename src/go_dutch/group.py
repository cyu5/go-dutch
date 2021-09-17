# Group class
import collections
from heapq import heappop, heappush
from typing import Iterator, List, Set
from itertools import chain, combinations, islice


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
        self.__Transaction = collections.namedtuple("Transaction", "payer payees amount weights")
        self.__Payment = collections.namedtuple("Payment", "payer payee amount")

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

        
        transaction = self.__Transaction(payer, payees, amount, weights)
        self.__ledger.append(transaction)


    # return minimum transaction path to settle up all members
    def show_settle_min_flow(self) -> List[collections.namedtuple]:
        return self.__min_flow_helper(self.__balances.items())

    def __min_flow_helper(self, balances) -> List[collections.namedtuple]:
        negatives, positives = [], []
        transactions = []

        for m, b in balances:
            if b > 0:
                heappush(positives, (-b, m))
            elif b < 0:
                heappush(negatives, (b, m))

        while negatives:
            payee_amount, payee = heappop(positives)
            payer_amount, payer = heappop(negatives)
            remains = payer_amount - payee_amount
            amount = min(abs(payee_amount), abs(payer_amount))
            if remains > 0:
                heappush(positives, (-remains, payee))
            elif remains < 0:
                heappush(negatives, (remains, payer))

            transactions.append(self.__Payment(payer, payee, amount))

        return transactions
        

    # settle up all members
    def settle_min_flow (self):
        transactions = self.show_settle_min_flow()
        for t in transactions:
            self.__ledger.append( self.__Transaction(t.payer, [t.payee], t.amount, None) )
        for member in self.get_members():
            self.__balances[member] = 0

    def show_settle_min_transactions(self) -> List[collections.namedtuple]:
        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

        def best_partition(subset: List[Set[tuple]]) -> List[Set[tuple]]:
            if not subset:
                return []
            else:
                solutions = []
                for s in subset:
                    if sum(balance for _, balance in s) == 0:
                        new_subset = list(ns for ns in subset if not (ns & s))
                        solutions.append(best_partition(new_subset) + [s])
                return max(solutions, key=len)

        balances = [(n, b) for n, b in self.__balances.items() if b != 0]
        seen = {}
        pairs = []
        paired = set()
        for name, b in balances:
            if -b in seen:
                pairs.append((name, seen[-b]))
                paired.add(name)
                paired.add(seen[-b])
                del seen[-b]
            else:
                seen[b] = name
        
        
        transactions = []
        for p in pairs:
            payer, payee = sorted(p, key=self.get_balance)
            amount = self.get_balance(payee)
            tran = self.__Payment(payer, payee, amount)
            transactions.append(tran)

        balances = list((name, b) for name, b in balances if name not in paired)
        subset = list(map(set, islice(powerset(balances), 1, None)))
        partition = best_partition(subset)
        for members_set in partition:
            transactions += self.__min_flow_helper(members_set)
        
        return transactions

    def settle_min_transactions(self):
        transactions = self.show_settle_min_transactions()
        for t in transactions:
            self.__ledger.append( self.__Transaction(t.payer, [t.payee], t.amount, None) )
        for member in self.get_members():
            self.__balances[member] = 0

    def __len__(self) -> int:
        return self.__balances.__len__()
    
    def __iter__(self) -> Iterator:
        return self.__balances.__iter__()

    def __contains__(self, member: str) -> bool:
        return self.__balances.__contains__(member)




    
    