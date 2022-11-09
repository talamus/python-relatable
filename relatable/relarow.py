import relatable
from relatable.__imports import *
from relatable import RelaTable


class RelaRow(MutableMapping):
    """
    A thin database table row -like wrapper for data objects.
    Supports foreign key -style references to an another `RelaTable` and
    index/key -style references to another containers.
    """

    __table: RelaTable
    __data: Any
    __index: int

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

    def __len__(self) -> int:
        """Return the number of columns."""
        return len(self.__data)

    def __iter__(self) -> Iterator:
        """Iterator for the columns."""
        return iter(self.__data)

    def data(self, data: Any = None) -> Any:
        """
        Get or set the data object of this row.
        NOTE: The primary key stays the same!
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
