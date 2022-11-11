from .__creatures_and_lairs import creatures, lairs


def test_object_referencing(creatures, lairs):
    assert creatures[1].lair.temperature == "cold"
    creatures[1].lair.temperature = "tepid"
    assert lairs.rows()[1].data().temperature == "tepid"
    lairs["crypt"].temperature = "freezing"
    assert creatures[1].lair.temperature == "freezing"


def test_missing_reference(creatures):
    assert creatures[3].name == "nomad"
    assert creatures[3].lair is None
    assert creatures[3].enemy is None


def test_blueprint(creatures, lairs):
    assert creatures.blueprint() == [
        {
            "type": "dragon",
            "lair": {"name": "volcano", "temperature": "scorching"},
            "enemy": {
                "type": "necromancer",
                "lair": {"name": "crypt", "temperature": "cold"},
                "enemy": {
                    "name": "djinn",
                    "lair": {"name": "desert", "temperature": "hot"},
                    "enemy": {"name": "nomad", "lair": None, "enemy": None},
                },
            },
        },
        {
            "type": "necromancer",
            "lair": {"name": "crypt", "temperature": "cold"},
            "enemy": {
                "name": "djinn",
                "lair": {"name": "desert", "temperature": "hot"},
                "enemy": {"name": "nomad", "lair": None, "enemy": None},
            },
        },
        {
            "name": "djinn",
            "lair": {"name": "desert", "temperature": "hot"},
            "enemy": {"name": "nomad", "lair": None, "enemy": None},
        },
        {"name": "nomad", "lair": None, "enemy": None},
    ]
