from typing import Iterable
from relatable import RelaTable
from relatable.__imports import *


class RelaRow(MutableMapping):
    """
    ### A thin database table row -like wrapper for data objects
    Supports foreign key -style references to an another `RelaTable` and
    index/key -style references to another containers.
    """

    __table: RelaTable
    __data: Any
    __index: int | None

    def __init__(self, table: RelaTable, data: Any, index: int | None = None) -> None:
        """Wrap data object into a row."""
        self.__table = table
        self.__index = index
        self.__data = data

    def __getattr__(self, column: column_name) -> Any:
        """
        Return the column value.
        If column is a foreign key, return the value from the another table.
        """
        if hasattr(self.__data, column):
            value = getattr(self.__data, column)
        else:
            value = self.__data[column]

        if column in self.__table.foreign_keys:
            return self.__table.foreign_keys[column][value]
        else:
            return value

    def __setattr__(self, column: column_name, value: Any) -> None:
        """Set only columns that already exist in the data object."""

        # When data is not yet present, the object is not ready to use
        if "_RelaRow__data" not in self.__dict__:
            return super().__setattr__(column, value)

        # We have data, and data should have all the columns
        if hasattr(self.__data, column):
            return setattr(self.__data, column, value)
        if column in self.__data:
            self.__data[column] = value
            return

        raise KeyError(
            f"Column {column} does not exist in {self.__data}. "
            f"Add or remove columns by directly manipulating the data object."
        )

    def __delattr__(self, column: column_name) -> None:
        raise NotImplementedError(
            f"Add or remove columns by directly manipulating the data object."
        )

    def __getitem__(self, column: column_name) -> Any:
        """
        Return the column value.
        If column is a foreign key, return the value from the another table.
        """
        return self.__getattr__(column)

    def __setitem__(self, column: column_name, value: Any) -> None:
        """Set only columns that already exist in the data object."""
        return self.__setattr__(column, value)

    def __delitem__(self, column: column_name) -> None:
        raise NotImplementedError(
            f"Add or remove columns by directly manipulating the data object."
        )

    def __repr__(self) -> str:
        """A "true" representation of the row data."""
        return str(self.__data)

    def blueprint(self) -> dict:
        """
        Return a recursively expanded object representation of the row data.
        NOTE: A cyclic references will throw a RecursionError
        """
        if isinstance(self.__data, Iterable):
            data = self.__data
        elif hasattr(self.__data, "__dict__"):
            data = self.__data.__dict__
        else:
            return self.__data

        out = {}
        for column in data:
            if isinstance(self[column], RelaRow):
                out[column] = self[column].blueprint()
            else:
                out[column] = self[column]
        return out

    def __str__(self, raw: bool = False) -> str:
        """Recursively expanded string representation of the row data."""
        return str(self.blueprint())

    def __len__(self) -> int:
        """Return the number of columns."""
        return len(self.__data)

    def __iter__(self) -> Iterator:
        """Iterator for the columns."""
        return iter(self.__data)

    def data(self, data: Any = None) -> Any:
        """
        Get or set the data object of this row.
        #### NOTE: The primary key stays the same!
        """
        if data is not None:
            if self.__table.primary_key_column:
                primary_key = self[self.__table.primary_key_column]
                try:
                    setattr(data, self.__table.primary_key_column, primary_key)
                except AttributeError:
                    data[self.__table.primary_key_column] = primary_key
            super().__setattr__("_RelaRow__data", data)

        return self.__data

    def index(self, index: int | None = None) -> int | None:
        """
        Getter/setter for row index.
        (This is only used when table has no primary key.)
        """
        if index is not None:
            super().__setattr__("_RelaRow__index", index)
        return self.__index

    def primary_key(self) -> Any:
        """Getter for primary key value for this row."""
        if self.__table.primary_key_column is None:
            return self.index()
        else:
            return self.__data[self.__table.primary_key_column]
