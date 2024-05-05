from typing import Any, Protocol

class SupportsGetAttr(Protocol):
    def __getattr__(self, key: str) -> Any: ...

class SupportsGetItem(Protocol):
    def __getitem__(self, key: str) -> Any: ...

SupportsKeyIndex = SupportsGetAttr | SupportsGetItem