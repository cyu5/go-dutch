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

