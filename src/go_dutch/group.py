# import libaries
import collections
from heapq import heappop, heappush
from typing import Iterable, Iterator, List, Set, NamedTuple
from itertools import chain, combinations, islice

# Group class, inheriting collections
class Group(collections.abc.Collection):

    # constructor
    def __init__(self, members:Iterable[str]=None) -> None:

        # keys -> member, values -> net balance
        self.__balances = dict()

        # input validation
        if members is not None:
            # add members to group
            if not isinstance(members, str):
                for member in members:
                    if not isinstance(member, str):
                        raise TypeError(f'{member} is not a str')
                    else:
                        self.__balances[member] = 0.0
            else:
                raise TypeError('input should be an iterable, not a string')
            
        # ledger of transactions occurred until now
        self.__ledger = list()
        self.__Transaction = collections.namedtuple("Transaction", "payer payees amount weights")
        # format for ways to settle payments
        self.__Payment = collections.namedtuple("Payment", "payer payee amount")


    # add multiple memebers to the group
    def extend_members(self, new_members:Iterable[str]) -> None:
        # input validation
        if not isinstance(new_members, str):
            tmp = dict()
            for member in new_members:
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
    

    ############################ getters ############################

    def get_members (self) -> list:
        return list(self.__balances.keys())

    def get_balance (self, member: str) -> float:
        try:
            return self.__balances[member]
        except KeyError:
            raise KeyError(f"{member} is not part of group {self}")

    def get_ledger(self) -> list:
        return self.__ledger.copy()

    def get_balances (self) -> dict:
        return self.__balances.copy()

    ###################################################################


    # remove a single member from the group only if the member is settled
    def remove_settled_member (self, member: str) -> None:
        if member not in self.__balances:
            raise KeyError(f"{member} is not part of group {self}")
        if self.__balances[member] != 0:
            raise ValueError(f"{member} is not settled")
        del self.__balances[member]

    
    # add a single transaction to the ledger and update balances accordingly
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


    # return payments for minimum cash flow to settle the group
    def show_settle_min_flow(self) -> List[NamedTuple]:
        return self.__min_flow_helper(self.__balances.items())

    # minimum cash flow calculation
    def __min_flow_helper(self, balances:Iterable[tuple]) -> List[NamedTuple]:
        negatives, positives = [], []
        transactions = []

        # ignoring settled members (balence == 0)
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
        

    # settle up all members by minimum cash flow and update the ledger accordingly
    def settle_min_flow (self):
        transactions = self.show_settle_min_flow()
        for t in transactions:
            self.__ledger.append( self.__Transaction(t.payer, [t.payee], t.amount, None) )
        for member in self.get_members():
            self.__balances[member] = 0


    # return payments for minimum transactions to settle the group
    def show_settle_min_transactions(self) -> List[NamedTuple]:
        # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
        def powerset(iterable) -> Iterable[tuple]:
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

        # zero-sum set packing
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

        # removing 0 balances and equal magnitude +ve/-ve pairs
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


    # settle up all members by minimum transactions and update the ledger accordingly
    def settle_min_transactions(self):
        transactions = self.show_settle_min_transactions()
        for t in transactions:
            self.__ledger.append( self.__Transaction(t.payer, [t.payee], t.amount, None) )
        for member in self.get_members():
            self.__balances[member] = 0


    # clears all information from group
    def clear (self) -> None:
        self.__balances.clear()
        self.__ledger.clear()

        
    # check for existence of a member in the group
    def has_member (self, member: str) -> bool:
        return member in self.__balances


    # implementing collections' methods
    def __len__(self) -> int:
        return self.__balances.__len__()
    
    def __iter__(self) -> Iterator:
        return self.__balances.__iter__()

    def __contains__(self, member: str) -> bool:
        return self.__balances.__contains__(member)
