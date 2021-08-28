import pytest

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

    # non-existent member
    with pytest.raises(KeyError):
        group1.remove_settled_member(member2)

    # successful removal of settled member
    group1.remove_settled_member(member1)
    assert group1.get_balances().__len__() == 0

    # TODO: member yet to settle
    # with pytest.raises(ValueError):
        # group1.remove_settled_member(<>)

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
