import yaml
import pytest
from pathlib import Path
from relatable import RelaTable


class Thing:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class Creature(Thing):
    pass


class Lair(Thing):
    pass


with open(
    Path(__file__).parent.joinpath("resources").joinpath("creatures_and_lairs.yaml"),
    "r",
) as resource_file:
    resources = yaml.safe_load(resource_file)


__lairs = RelaTable(primary_key_column="name")
__creatures = RelaTable()
__creatures.foreign_keys = {"lair": __lairs, "enemy": __creatures}


@pytest.fixture
def lairs():
    global __lairs
    __lairs.clear()
    for lair in resources["lairs"]:
        __lairs.append(Lair(lair))
    return __lairs


@pytest.fixture
def creatures():
    global __creatures
    __creatures.clear()
    for creature in resources["creatures"]:
        __creatures.append(Lair(creature))
    return __creatures
