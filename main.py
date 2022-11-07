from relatable import RelaTable


def main():
    colors = ["red", "blue", "green"]

    users = RelaTable(
        primary_key_column="id",
        foreign_keys={"color": colors},
        rows=[
            {"id": 123, "name": "Jaakko", "color": 0},
            {"id": 456, "name": "Teppo", "color": 1},
        ],
    )

    users.insert(1, {"id": 789, "name": "Seppo", "color": 2})

    print("----------------")
    print(users[456].data())
    print(users.primary_key_to_index)
    print("----------------")

    for user in users.rows():
        print(user.data(), user.color, user.name)
    print("----------------")

    users[456].name = "Marjatta"
    users[456].color = 0

    for user in users.rows():
        print(user.data(), user.color, user.name)
    print("----------------")

    users[456] = {"id": 999, "name": "Joonas", "color": 2}

    for user in users.rows():
        print(user.data(), user.color, user.name)
    print("----------------")


if __name__ == "__main__":
    main()
