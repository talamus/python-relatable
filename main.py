from relatable import RelaTable


def main():
    """A simple example."""

    colors = ["red", "blue", "green"]
    pet_names = {"dog": "Musti", "cat": "Mirri"}

    persons = RelaTable(
        primary_key_column="id",
        foreign_keys={"color": colors},
        rows=[
            {"id": 123, "name": "Jaakko", "color": 0},
            {"id": 456, "name": "Teppo", "color": 1},
        ],
    )

    # Insert new user in the middle of the table
    persons.insert(1, {"id": 789, "name": "Seppo", "color": 2})

    pets = RelaTable(
        # No primary key defined => index is used
        foreign_keys={"name": pet_names, "owner": persons},
        rows=[
            {"name": "cat", "owner": 123},  # index 0
            {"name": "dog", "owner": 456},  # index 1
        ],
    )

    print(persons)
    # Prints out:
    #   [{'id': 123, 'name': 'Jaakko', 'color': 'red'},
    #    {'id': 789, 'name': 'Seppo', 'color': 'green'},
    #    {'id': 456, 'name': 'Teppo', 'color': 'blue'}]

    print(pets)
    # Prints out:
    #   [{'name': 'Mirri', 'owner': {'id': 123, 'name': 'Jaakko', 'color': 'red'}},
    #    {'name': 'Musti', 'owner': {'id': 456, 'name': 'Teppo', 'color': 'blue'}}]

    print(persons[789].name)
    # Prints out:
    #   Seppo

    print(pets[0].owner.color)
    # Prints out:
    #   red

    print(pets[0].data())
    # Prints out the non-expanded row data:
    #   {'name': 'cat', 'owner': 123}


if __name__ == "__main__":
    main()
