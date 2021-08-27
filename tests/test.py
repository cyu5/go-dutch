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
    assert Group([]).members.__len__() == 0

    # all members unique
    assert Group(["joe", "nick", "john"]).members.__len__() == 3

    # check unique members
    assert Group(["john", "john"]).members.__len__() == 1


def test_add_member ():

    # sample variables
    group1 = Group()
    member1 = "Nick"

    # function adds new
    group1.add_member (member1)
    assert group1.members.__len__() == 1
    assert group1.balances[member1] == 0

    # function has no effect if member already exists
    group1.add_member (member1)
    assert group1.members.__len__() == 1

    # function raises error on invalid input
    with pytest.raises(TypeError):
        group1.add_member (10)
    with pytest.raises(TypeError):
        group1.add_member ()
    with pytest.raises(TypeError):
        group1.add_member ([member1])