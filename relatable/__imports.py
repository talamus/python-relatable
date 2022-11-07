# TODO: Remove when postponed annotations are the standard:
from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias, Iterator, Sequence
from collections.abc import MutableSequence, MutableMapping

column_name: TypeAlias = str
column_value: TypeAlias = Any
RelaRow: TypeAlias = Any  # Preventing cyclic idiocies
