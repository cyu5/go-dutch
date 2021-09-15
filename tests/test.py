import pytest
import collections

import sys
sys.path.append("../")

from src.go_dutch.group import Group

# test Group class init
def test_group_init_validation():
    with pytest.raises(TypeError):
        Group(1)
    with pytest.raises(TypeError):
        Group([1, 1, 1])
    with pytest.raises(TypeError):
        Group([[]])
    with pytest.raises(TypeError):
        Group("a string")

def test_group_init_members():
    # check empty members
    assert Group([]).get_members().__len__() == 0

    # all members unique
    assert Group(["joe", "nick", "john"]).get_members().__len__() == 3

    # check unique members
    assert Group(["john", "john"]).get_members().__len__() == 1


def test_add_member ():

    # sample variables
    group1 = Group()
    member1 = "Nick"

    # function adds new
    group1.add_member (member1)
    assert group1.get_members().__len__() == 1
    assert group1.get_balance(member1) == 0

    # function has no effect if member already exists
    group1.add_member (member1)
    assert group1.get_members().__len__() == 1

    # function raises error on invalid input
    with pytest.raises(TypeError):
        group1.add_member (10)
    with pytest.raises(TypeError):
        group1.add_member ()
    with pytest.raises(TypeError):
        group1.add_member ([member1])

        
def test_extend_members():
    group = Group()
    
    with pytest.raises(TypeError):
        group.extend_members(1)
    with pytest.raises(TypeError):
        group.extend_members([1, 1, 1])
    with pytest.raises(TypeError):
        group.extend_members([[]])
    with pytest.raises(TypeError):
        group.extend_members("a string")
    with pytest.raises(TypeError):
        group.extend_members(['joe','john',1])
    assert group.get_members().__len__() == 0

    # check empty members
    group.extend_members([])
    assert group.get_members().__len__() == 0

    # all members unique
    group.extend_members(["joe", "nick", "john"])
    assert group.get_members().__len__() == 3

    # check unique members
    group.extend_members(["sarah", "sarah"])
    assert group.get_members().__len__() == 4

def test_has_member():
    group = Group(['joe'])
    assert group.has_member('joe')
    assert not group.has_member("john")

def test_remove_settled_member():
    member1, member2 = "Arthur", "Sadie"
    group1 = Group([member1])
    group2 = Group([member1, member2])

    # successful removal of settled member
    group1.remove_settled_member(member1)
    assert group1.get_balances().__len__() == 0

    # non-existent member
    with pytest.raises(KeyError):
        group1.remove_settled_member(member2)

     # member yet to settle
    group2.add_transaction("Arthur", ["Arthur", "Sadie"], 10)
    with pytest.raises(ValueError):
        group2.remove_settled_member("Sadie")


def test_clear():
    member1, member2 = "Micah", "Javier"
    group1 = Group([member1, member2])
    group1.clear()
    assert group1.get_balances().__len__() == 0
    assert not group1.get_ledger()

def test_special_methods():

    group = Group(["joe", "john", "mike"])
    
    # contains
    assert "joe" in group
    assert "jose" not in group
    
    # len
    assert len(group) == 3 
    
    # iter
    assert list(group) == group.get_members()

def test_add_transaction():

    group = Group(["joe", "john", "mike"])

    # invalid payer
    with pytest.raises(ValueError):
        group.add_transaction("x", ["joe"], 1)

    # invalid payee
    with pytest.raises(ValueError):
        group.add_transaction("joe", ["x"], 1)

    # invalid amount
    with pytest.raises(ValueError):
        group.add_transaction("mike", ["joe"], -1)

    # invalid weight
    with pytest.raises(ValueError):
        group.add_transaction("mike", ["joe", "john"], 1, [2, -8])
    with pytest.raises(ValueError):
        group.add_transaction("mike", ["joe", "john"], 1, [2])

    # no weight transaction
    group.add_transaction("mike", ["joe", "john"], 2)
    assert group.get_balance("mike") == 2
    assert group.get_balance("joe") == group.get_balance("john") == -1
    ledger = group.get_ledger()
    assert ledger.__len__() == 1
    transaction = ledger[0]
    assert transaction == ("mike", ["joe", "john"], 2, None)
    assert transaction.payer == "mike"
    assert transaction.payees == ["joe", "john"]
    assert transaction.amount == 2
    assert transaction.weights == None

    # weighted transaction
    group.add_transaction("mike", ["joe", "john", "mike"], 4, [1, 1, 2])
    assert group.get_balance("mike") == 4
    assert group.get_balance("joe") == group.get_balance("john") == -2
    assert group.get_ledger().__len__() == 2


def test_show_settle ():
    group = Group(["A", "B", "C", "D"])
    group.add_transaction("A", ["B", "C"], 10)
    group.add_transaction("D", ["C", "D"], 14, [2, 5])

    Payment = collections.namedtuple("Payment", "payer payee amount")
    transactions = [
        Payment("C", "A", 9),
        Payment("B", "D", 4),
        Payment("B", "A", 1)
    ]
    assert group.show_settle() == transactions

def test_settle ():
    group = Group(["A", "B", "C"])
    group.add_transaction("A", ["B", "C"], 4)
    group.settle()

    assert not any(group.get_balances().values())
    assert group.get_ledger().__len__() == 3

    # settling settled group changes nothing
    group.settle()
    assert not any(group.get_balances().values())
    assert group.get_ledger().__len__() == 3
