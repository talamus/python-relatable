# TODO: Remove when postponed annotations are the standard:
from __future__ import annotations

from collections.abc import MutableMapping, MutableSequence
from typing import (TYPE_CHECKING, Any, Callable, Iterator, Mapping, Sequence,
                    TypeAlias)

column_name: TypeAlias = str
column_value: TypeAlias = Any

# Preventing cyclic idiocies
RelaRow: TypeAlias = Any
