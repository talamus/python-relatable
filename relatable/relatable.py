# TODO: Remove when postponed annotations are the standard:
from __future__ import annotations

import relatable
from relatable.__imports import *


class RelaTable(MutableSequence):
    """
    A relational database -like table of rows.

    Supports foreign key -style references to an another `RelaTable` and
    index/key -style references to another containers.
    """

    primary_key_column: column_name | None
    primary_key_to_index: dict[Any, int]  # Primary key value -> self.__rows index
    foreign_keys: dict[column_name, Container]
    __rows: list[RelaRow]

    def __init__(
        self,
        primary_key_column: column_name | None = None,
        foreign_keys: dict[column_name, Container] = {},
        rows: Sequence = [],
    ) -> None:
        """
        Create a new table.

        :param primary_key_column:
            Name of the primary key column. (`None` = Use row index as the primary key.)
        :param foreign_keys:
            Dictionary of references from a local column value to an another Sequence.
        :rows:
            An initial list of rows to be inserted.
        :is_view:
            True if this table is not the
        """
        self.primary_key_column = primary_key_column
        self.primary_key_to_index = dict()
        self.foreign_keys = dict(foreign_keys)
        self.__rows = list()
        for row in rows:
            self.append(row)

    def __getitem__(self, primary_key: column_value) -> RelaRow:
        """
        Get row from the table (using primary key).

        :param primary_key:  Primary key value of the row that we want.
        :returns:  The actual row.
        """
        try:
            return self.__rows[self.primary_key_to_index[primary_key]]
        except KeyError:
            raise KeyError(
                f"{'Primary key' if self.primary_key_column else 'Index'} "
                f"{primary_key} ({type(primary_key).__name__}) not found."
            )

    def __setitem__(self, primary_key: column_value, data: Any) -> None:
        """Replace data object with new data."""
        self.__rows[self.primary_key_to_index[primary_key]].data(data)

    def __delitem__(self, primary_key: column_value) -> None:
        """
        Remove row from the table.
        Removing from the middle is allowed only when using a primary key.

        :param primary_key:  Primary key value of the row that we want to delete.
        """
        index = self.primary_key_to_index[primary_key]
        if self.primary_key_column is None and index != len(self) - 1:
            raise IndexError(
                "Removing from the middle is only supported with primary keys."
            )
        del self.__rows[index]
        del self.primary_key_to_index[primary_key]

    def __iter__(self) -> Iterator:
        """Iterator for the rows."""
        return iter(self.__rows)

    def __repr__(self) -> str:
        """A "true" string representation of the table rows."""
        return repr(self.__rows)

    def __str__(self) -> str:
        """A string representation of table rows with all the foreign keys expanded."""
        out = []
        for row in self.__rows:
            out.append(str(row))
        return f"[{', '.join(out)}]"

    def __len__(self) -> int:
        """Number of rows in the table."""
        return len(self.__rows)

    def insert(self, index: int, data: Any) -> None:
        """
        Add object to the table as a new row.
        :index:  List index position to insert the new row into.
        :data:  The actual data object to be added.
        """
        len_rows = len(self.__rows)

        # Add a thin wrapper around the data.
        row = relatable.RelaRow(self, data, index)

        # Map primary key value to index number.
        if self.primary_key_column:
            primary_key_value = row[self.primary_key_column]
        else:
            if index != len_rows:
                raise IndexError(
                    "Inserting into middle is only supported with primary keys."
                )
            primary_key_value = index
        if primary_key_value in self.primary_key_to_index:
            raise KeyError(f"Primary key {primary_key_value} already exists.")

        # If we are inserting somewhere into middle
        # `primary_key_to_index` has to be updated.
        if index != len(self.__rows):
            for key, old_index in self.primary_key_to_index.items():
                if old_index >= index:
                    self.primary_key_to_index[key] = old_index + 1

        self.primary_key_to_index[primary_key_value] = index
        self.__rows.insert(index, row)

    def sort(self, **kwargs) -> None:
        """
        Sort the table rows. Arguments are the same as for list.sort():
        https://docs.python.org/3/library/stdtypes.html#list.sort
        """
        self.__rows.sort(**kwargs)
        for index, row in enumerate(self.__rows):
            if self.primary_key_column:
                primary_key_value = row[self.primary_key_column]
            else:
                primary_key_value = index
            self.primary_key_to_index[primary_key_value] = index
            if isinstance(row, relatable.RelaRow):
                row.index(index)

    def find(self, criteria: Callable[[RelaRow], bool]) -> list[RelaRow]:
        """
        Finds all the rows that fulfill a criteria.
        :criteria:
            A function that recieves a row and returns True if the criteria is fulfilled.
        :returns:
            A "view" containing all the matching rows.
        """
        rows = list()
        for row in self.__rows:
            if criteria(row):
                rows.append(row)
        return rows

    def find_first(self, criteria: Callable[[RelaRow], bool]) -> RelaRow | None:
        """
        Return the first row that matches the criteria (or None if nothing matches).
        (A shorthand for self.find(...)[0]).
        """
        try:
            return self.find(criteria)[0]
        except IndexError:
            return None

    def clear(self) -> None:
        """Clear the table."""
        self.__rows.clear()
        self.primary_key_to_index.clear()

    def rows(self) -> list:
        """Returns list of the current rows."""
        return self.__rows
